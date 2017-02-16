from reader import newsParser as nP

#https://lenta.ru/news/2017/01/19/avalanche30/
#https://www.gazeta.ru/politics/2017/01/19_a_10481981.shtml#page1
#http://www.rbc.ru/politics/19/01/2017/58806cec9a7947114330fbbf

if __name__ == '__main__':
    news = nP.NewsParser('https://lenta.ru/news/2017/01/19/avalanche30/')
    news.start()
