import scrapy


class MiddleSpider(scrapy.Spider):
    name = 'middle'
    # allowed_domains = ['middle.com']
    start_urls = ['http://www.baidu.com/','http://www.baidu.com/']

    def parse(self, response):
        print(response)
