from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import SunItem, SunItemDetail


class PoliticsSpider(CrawlSpider):
    name = 'politics'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=0']

    link = LinkExtractor(allow=r'id=1&page=\d+')
    link_detail = LinkExtractor(allow=r'index\?id=\d+')

    rules = (
        Rule(link, callback='parse_item', follow=False),
        Rule(link_detail, callback='parse_detail', follow=False),
    )

    def parse_item(self, response):
        # print(response)
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            title = li.xpath('./span[3]/a/text()').get().strip()
            url = li.xpath('./span[3]/a/@href').get()
            state = li.xpath('./span[2]/text()').get().strip()
            item = SunItem(title=title, state=state)
            # print(title,state,url)
            yield item

    def parse_detail(self, response):
        # print(response)
        content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').get()
        item = SunItemDetail(content=content)
        # print(content)
        yield item
