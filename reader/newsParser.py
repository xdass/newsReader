from reader import wrap
import urllib.request
import re
import html
import os


class NewsParser:

    def __init__(self, link):
        self._link = link

    def start(self):
        print('Парсинг...')
        title, article = self._prepare_data(self._receive_news())
        article = self._generate_text(article)
        self._save_to_file(title, article)
        print('Завершено')

    def _receive_news(self):  # Загрузить страницу с новостью
        request = urllib.request.Request(self._link)
        request.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(request)
        page_charset = response.headers.get_content_charset()
        raw_data = response.read().decode(page_charset)
        return raw_data

    def _prepare_data(self, raw_data):  # Получить заголовки и текст статьи
        article_title = re.search(r'<title>(.*?)</title>', raw_data, re.MULTILINE | re.VERBOSE).group(1)
        article_title = article_title[:article_title.find(':')]
        article_text = re.findall(r'<p>(.*?)</p>', raw_data, re.MULTILINE | re.VERBOSE)
        clear_article = [html.unescape(item) for item in article_text]
        clear_article = self._highlight_links(clear_article)
        return article_title, clear_article

    @staticmethod
    def _generate_text(clear_text):  # Очистка текста от тегов оформления
        article = []
        for i in clear_text:
            r = re.search(r'<strong.*>(.*?)</strong>', i)
            if r:
                article.append({'title': r.group(1)})
            else:
                article.append({'text': i})
        return article

    @staticmethod
    def _highlight_links(text):  # Ссылки в квадратные скобки
        data = []
        query_for_links = re.compile(r'<a\b.*?(?:href=\"(.*?)\")[^>]*>(.*?)</a>')

        for item in text:
            links = re.findall(query_for_links, item)
            if links:
                if len(links) > 1:
                    tmp = item
                    for link in links:
                        tmp = re.sub(r'<a\b[^>]*>.*?</a>', '[{}] {}'.format(link[0], link[1]), tmp, count=1)
                    data.append(tmp)
                else:
                    data.append(re.sub(r'<a\b[^>]*>.*?</a>', Linker(links), item))
            else:
                data.append(item)
        return data

    def _save_to_file(self, title, article):
        path = self._get_path_from_link()
        with open(path, 'w', encoding='utf-8') as file:
            file.write(title + '\n\n')
            for item in article:
                if 'title' in item:
                    file.write(wrap.text_wrap(item['title'], 80))
                    file.write('\n\n')
                else:
                    file.write(wrap.text_wrap(item['text'], 80))
                    file.write('\n\n')

    def _get_path_from_link(self):
        regex = r'(?:^http[s]?://)(.+)(\b.+)\b[\/]?'
        result = re.match(regex, self._link)
        path = os.path.normpath(result.group(1))
        filename = result.group(2)
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('Директория уже создана')
        return os.path.join(path, filename + '.txt')


class Linker:  # Вспомогательный класс для замены ссылок
    def __init__(self, links):
        self.links = links

    def gen(self):
        for link in self.links:
            yield link

    def __call__(self, match):
        s = self.gen()
        return '[{}] {}'.format(*next(s))
