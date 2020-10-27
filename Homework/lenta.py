from pymongo import MongoClient
from datetime import datetime
from lxml import html
import requests
client = MongoClient('127.0.0.1', 27017)
collection = client.db['lenta']

news = []

keys = ('title', 'date', 'link')
date_format = '%Y-%m-%dT%H:%M:%S%z'
link_lenta = 'https://lenta.ru/'

request = requests.get(link_lenta)

root = html.fromstring(request.text)
root.make_links_absolute(link_lenta)

# news_links = root.xpath('''//body/div[@id='root']/section[2]/div[1]//div[@class='item']/a/@href''')
# news_text = root.xpath('''//body/div[@id='root']/section[2]/div[1]//div[@class='item']/a/text()''')

news_links = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/@href''')




news_text = root.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/text()''')

for i in range(len(news_text)):
    news_text[i] = news_text[i].replace(u'\xa0', u' ')

news_date = []

for item in news_links:
    request = requests.get(item)
    root = html.fromstring(request.text)
    date = root.xpath('//div[@class="b-topic__info"]/time/@datetime')
    news_date.extend(date)

for i in range(len(news_date)):
    news_date[i] = datetime.strptime(news_date[i], date_format)

# print(news_text, news_links, news_date)
for item in list(zip(news_text, news_date, news_links)):
    news_dict = {}
    for key, value in zip(keys, item):
        news_dict[key] = value

    news_dict['source'] = 'lenta.ru'
    news.append(news_dict)

print('Collected!')
for item in news:
    print(item)