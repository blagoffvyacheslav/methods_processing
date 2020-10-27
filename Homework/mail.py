from pymongo import MongoClient
from datetime import datetime
from lxml import html
import requests
client = MongoClient('127.0.0.1', 27017)
collection = client.db['mail']

news = []

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
}

keys = ('title', 'date', 'link')
date_format = '%Y-%m-%dT%H:%M:%S%z'

link_mail_ru = 'https://news.mail.ru/'

request = requests.get(link_mail_ru, headers=headers)
root = html.fromstring(request.text)

news_links = root.xpath('''(//li[@class='list__item']//span['@list__text']  |  
                                //div[contains(@class, "daynews__item")])
                                /a[contains(@href, "news.mail.ru")]/@href''')


news_text = root.xpath('''(//li[@class='list__item']//span['@list__text']/a/span  |  
                               //div[contains(@class, "daynews__item")]//a//span[contains(@class, 'photo__title')])
                               /text()''')

for i in range(len(news_text)):
    news_text[i] = news_text[i].replace(u'\xa0', u' ')


news_date = []

for item in news_links:
    request = requests.get(item, headers=headers)
    root = html.fromstring(request.text)
    date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
    news_date.extend(date)

for i in range(len(news_date)):
    news_date[i] = datetime.strptime(news_date[i], date_format)

for item in list(zip(news_text, news_date, news_links)):
    news_dict = {}
    for key, value in zip(keys, item):
        news_dict[key] = value

    news_dict['source'] = 'mail.ru'
    news.append(news_dict)
    collection.insert_one(news_dict)

print('Collected!')
for item in news:
    print(item)