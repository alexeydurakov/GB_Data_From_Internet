# 1. Написать приложение, которое собирает основные новости с сайтов
# https://news.mail.ru,
# https://lenta.ru,
# https://yandex.ru/news.
# Для парсинга использовать XPath. Структура данных должна содержать:
#  название источника;
#  наименование новости;
#  ссылку на новость;
#  дата публикации.
# 2. Сложить собранные данные в БД
from pprint import pprint

from lxml import html
import requests
from pymongo import MongoClient


def get_news_from_lenta():
    news_list = []
    host = 'https://lenta.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    response = requests.get(host, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath("//section[contains(@class,'js-top-seven')]//div[@class='item']")
    for item in items:
        news = {
            'source': 'LENTA_RU',
            'title': str(item.xpath("./a/text()")[0]).replace(u'\xa0', u''),
            'url': host + str(item.xpath("./a/@href")[0]),
            'publication_date': str(item.xpath("./a/time/@title")[0])
        }
        news_list.append(news)
    return news_list


def get_news_from_yandex():
    news_list = []
    host = 'https://yandex.ru/news'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    response = requests.get(host, headers=headers)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[contains(@class,'news-top-flexible-stories')]/div")
    for item in items:
        news = {
            'source': str(item.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]),
            'title': str(item.xpath(".//h2/text()")[0]),
            'url': str(item.xpath(".//a[@class='mg-card__source-link']/@href")[0]),
            'publication_date': str(item.xpath(".//span[@class='mg-card-source__time']/text()")[0]),
        }
        news_list.append(news)
    return news_list


all_news = get_news_from_lenta()
all_news += get_news_from_yandex()

client = MongoClient('127.0.0.1', 27017)
db = client['news']

db.news.insert_many(all_news)

