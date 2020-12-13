import scrapy


class InstagramparserItem(scrapy.Item):
    _id = scrapy.Field()
    _collection = scrapy.Field()
    id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    profile_pic_url = scrapy.Field()
    private = scrapy.Field()
    verified = scrapy.Field()
    linked_user_id = scrapy.Field()
    linked_username = scrapy.Field()