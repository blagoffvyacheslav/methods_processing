import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        vac_links_on_page = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()
        next_page_link = response.xpath('//a[@data-qa="pager-next"]/@href').extract_first()
        for vac_link in vac_links_on_page:
            yield response.follow(vac_link, callback=self.parse_vacancy_page)
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        print()

    def parse_vacancy_page(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//p/span[@data-qa="bloko-header-2"]/text()').extract()
        link = response.url
        yield JobparserItem(name=name, salary=salary, link=link, source='hh.ru')
        print()