# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.selector import Selector

def parse_props(value):
    if value:
        r = Selector(text=value)
        sel_list = r.xpath('//div[@class = "def-list__group"]')
        result = {}
        for selector in sel_list:
            k = selector.xpath('.//dt/text()').extract_first()
            v_str = selector.xpath('.//dd/text()').extract_first()
            v_str = ''.join(i.strip().replace(',', '.') for i in v_str.split('\n'))
            try:
                v = float(v_str)
            except ValueError:
                v = v_str
            result[k] = v
        value = result
        return value


def convert(value):
    if value:
        value = value.replace(',', '.').replace(' ', '')
        try:
            result = float(value)
        except:
            result = value
    return result



class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert), output_processor=TakeFirst())
    props = scrapy.Field(input_processor=MapCompose(parse_props), output_processor=TakeFirst())
    photos = scrapy.Field()