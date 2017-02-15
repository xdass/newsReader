import urllib.request
import re
import html
from urllib.parse import urlparse
import os

#https://lenta.ru/news/2017/01/19/avalanche30/
#https://www.gazeta.ru/politics/2017/01/19_a_10481981.shtml#page1
#http://www.rbc.ru/politics/19/01/2017/58806cec9a7947114330fbbf

#query_clear_link = re.compile(r'(?<=href=\")http[s]?://+(.*?)(?=\")\".+?>(.*?)</a>')
#query_for_links = re.compile(r'<a\b.*?(?:href=\"(.*?)\")[^>]*>(.*?)</a>')#(<a\b[^>]*>(.*?)</a>)


class NewsParser:

    def __init__(self, link):
        self._link = link
        self._ready_text = None

    def start(self):
        title, article = self.prepare_data(self.receive_news())
        article = self.generate_text(article)
        self.save_to_file(title, article)

    def receive_news(self):  # Загрузить страницу с новостью
        request = urllib.request.Request(self._link)
        request.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(request)
        page_charset = response.headers.get_content_charset()
        raw_data = response.read().decode(page_charset)
        return raw_data

    def prepare_data(self, raw_data):  # Получить заголовки и текст статьи
        article_title = re.search(r'<title>(.*?)</title>', raw_data, re.MULTILINE | re.VERBOSE).group(1)
        article_text = re.findall(r'<p>(.*?)</p>', raw_data, re.MULTILINE | re.VERBOSE)
        clear_article = [html.unescape(item) for item in article_text]
        clear_article = highlight_links(clear_article)

        return article_title, clear_article

    def generate_text(self, clear_text):  # Очистка текста от тегов оформления
        article = []
        for i in clear_text:
            r = re.search(r'<strong.*>(.*?)</strong>', i)
            if r:
                article.append({'title': r.group(1)})
            else:
                article.append({'text': i})
        return article

    def save_to_file(self, title, article):
        path = self.get_path_from_link()
        with open(path, 'w', encoding='utf-8') as file:
            file.write(title)
            for item in article:
                if 'title' in item:
                    file.write(text_wrap(item['title'], 80))
                    file.write('\n\n')
                else:
                    file.write(text_wrap(item['text'], 80))
                    file.write('\n\n')

    def get_path_from_link(self):
        link = self._link
        if self._link.endswith('/'):
            link = link[:-1]
        link = urlparse(link)
        link = link.netloc + link.path
        path = link.split('/')
        filename = path[-1]
        path = path[:-1]
        path = os.path.join(os.getcwd(), *path)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('Директория уже создана')
        return os.path.join(path, filename)


class FootnoteNumbers:  # Вспомогательный класс для замены ссылок
    def __init__(self, links):
        self.links = links

    def gen(self):
        for link in self.links:
            yield link

    def __call__(self, match):
        s = self.gen()
        return '[{}] {}'.format(*next(s))


def highlight_links(text):  # Ссылки в квадратные скобки
    data = []
    query_for_links = re.compile(r'<a\b.*?(?:href=\"(.*?)\")[^>]*>(.*?)</a>')

    for item in text:
        links = re.findall(query_for_links, item)
        if links:
            if len(links) > 1:
                tmp = item
                for j in links:
                    tmp = re.sub(r'<a\b[^>]*>.*?</a>', '[{}] {}'.format(j[0], j[1]), tmp, count=1)
                data.append(tmp)
            else:
                data.append(re.sub(r'<a\b[^>]*>.*?</a>', FootnoteNumbers(links), item))
        else:
            data.append(item)
    return data


def text_wrap(text, width):
    clear = text.split()
    count = 0
    s = []
    newline = False
    prev = None

    for word in clear:
        if count + len(word) + 1 <= width:
            if newline:
                count += len(prev) + 1
                newline = False
            count += len(word) + 1
            s.append(word + ' ')
        else:
            s.append('\n')
            s.append(word + ' ')
            count = 0
            prev = word
            newline = True

    return ''.join(s)

news = NewsParser('https://lenta.ru/news/2017/01/19/avalanche30/')
news.start()
