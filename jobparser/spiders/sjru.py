import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vac_links_on_page = response.xpath('//a[contains (@class, "_6AfZ9")]/@href').extract()
        next_page_link = response.xpath('//span[@class="_3IDf-"]/@href').extract_first()
        for vac_link in vac_links_on_page:
            yield response.follow(vac_link, callback=self.parse_vacancy_page)
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        print()

    def parse_vacancy_page(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        link = response.url
        yield JobparserItem(name=name, salary=salary, link=link, source='superjob.ru')
        print()