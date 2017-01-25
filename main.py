import urllib.request
import re
import html
import time

start = time.time()

class FootnoteNumbers:
    def __init__(self, links):
        self.links = links

    def gen(self):
        for link in self.links:
            yield link

    def __call__(self, match):
        s = self.gen()
        return '[{}] {}'.format(*next(s))


def highlight_links(text):
    data = []

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

#https://lenta.ru/news/2017/01/19/avalanche30/
#https://www.gazeta.ru/politics/2017/01/19_a_10481981.shtml#page1
#http://www.rbc.ru/politics/19/01/2017/58806cec9a7947114330fbbf


newsUrl = 'http://www.rbc.ru/politics/19/01/2017/58806cec9a7947114330fbbf'
request = urllib.request.Request(newsUrl)
request.add_header('User-Agent', 'Mozilla/5.0')

response = urllib.request.urlopen(request)
page_charset = response.headers.get_content_charset()
data = response.read().decode(page_charset)

title = re.search(r'<title>(.*?)</title>', data, re.MULTILINE | re.VERBOSE).group(1)
raw_text = re.findall(r'<p>(.*?)</p>', data, re.MULTILINE | re.VERBOSE)
clear_text = [html.unescape(item) for item in raw_text]

query_clear_link = re.compile(r'(?<=href=\")http[s]?://+(.*?)(?=\")\".+?>(.*?)</a>')
#query = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\">(.*?)</a>')
query_for_links = re.compile(r'<a\b.*?(?:href=\"(.*?)\")[^>]*>(.*?)</a>')#(<a\b[^>]*>(.*?)</a>)

clear_text = highlight_links(clear_text)

#ToDo перенести в ф-цию
#Разделение на заголовки и содержание(параграфы)
article = []
for i in clear_text:
    r = re.search(r'<strong.*>(.*?)</strong>', i)
    if r:
        article.append({'title': r.group(1)})
    else:
        article.append({'text': i})

print(time.time() - start)

print(article)

with open('text.txt', 'w', encoding='utf-8') as file:
    for item in article:
        if 'title' in item:
            file.write(text_wrap(item['title'], 80))
            file.write('\n\n')
        else:
            file.write(text_wrap(item['text'], 80))
            file.write('\n\n')
