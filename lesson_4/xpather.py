from lxml import html
import requests
import datetime
import re
from pymongo import MongoClient


fav_dict = {
    'lenta.ru': {
        'url': 'https://lenta.ru',
        'news': '//div[@class="b-yellow-box__wrap"]//div[@class="item"]',
        'title': './/a/text()',
        'link': './/a/@href'
    },
    'yandex.ru': {
        'url': 'https://yandex.ru/news',
        'news': '//div[@class="mg-card__text-content"]/*/a',
        'title': './/text()',
        'link': '@href'
    },
    'mail.ru': {
        'url': 'https://news.mail.ru',
        'news': '//div[@class="daynews__item"] | //a[@class="list__text"]',
        'title': './/span[contains(@class,"photo__title")]/text() | .//text()',
        'link': './/@href | .//a[@class="photo"]/@href'
    }
}


def consume_news(source):
    website = fav_dict[source]
    response = requests.get(website['url'],
                            headers={'User-Agent': 'Mozilla/5.0'})
    root = html.fromstring(response.text)
    news = root.xpath(website['news'])
    articles = []

    for article in news:
        title = re.sub('\xa0', ' ', article.xpath(website['title'])[0])
        link = article.xpath(website['link'])[0]
        article_dict = {'title': title,
                        'link': link,
                        'source': source,
                        'date': datetime.date.today().isoformat()}
        articles.append(article_dict)

    return articles


def main():
    client = MongoClient('localhost', 27017)
    db = client['news_db']
    collection = db.articles

    for website in fav_dict.keys():
        collection.insert_many(consume_news(website))


if __name__ == '__main__':
    main()
