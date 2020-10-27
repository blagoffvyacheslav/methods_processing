from pprint import pprint
from lxml import  html
import requests

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'}

main_link = 'http://ru.ebay.com/b/Sony/bn_21835731'

response = requests.get(main_link, headers=header)

dom = html.fromstring(response.text)


names = dom.xpath("//h3[@class='s-item__title']/text()")
links = dom.xpath("//h3[@class='s-item__title']/../@href")
price = dom.xpath("//span[@class='s-item__price']//text()")

pprint(names)
pprint(links)
pprint(price)
# for item in names:
#     print(item.text)