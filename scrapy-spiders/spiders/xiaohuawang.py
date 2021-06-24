import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider


class XiaohuawangSpider(CrawlSpider):
    name = 'xiaohuawang'
    allowed_domains = ['www.521609.com']
    start_urls = ['http://www.521609.com/tuku/']
    link = LinkExtractor(allow=r'/tuku/\d+\.html')
    link_page = LinkExtractor(allow=r'/tuku/index_\d+\.html')
    rules = (
        Rule(link, callback='parse_item', follow=True),Rule(link_page, callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        print(response)

    # def parse(self, response):
    #     pass
