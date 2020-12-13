from pymongo import MongoClient
from pprint import pprint

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instagramparser import settings
from instagramparser.spiders.account import AccountSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AccountSpider)

    process.start()

    client = MongoClient('localhost', 27017)
    db = client.instagram

    delta_followers = db.followers.find({'linked_username': 'delta'})
    for follower in delta_followers:
        pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


    delta_followings = db.followings.find({'linked_username': 'delta'})
    for following in delta_followings:
        pprint(f"{following.get('username')} |:| {following.get('full_name')}")


    mosgortrans_followers = db.followers.find({'linked_username': 'mosgortrans'})
    for follower in mosgortrans_followers:
        pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


    mosgortrans_followings = db.followings.find({'linked_username': 'mosgortrans'})
    for following in mosgortrans_followings:
        pprint(f"{following.get('username')} |:| {following.get('full_name')}")