import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):

        li_list = response.xpath("//div[@class='maincon']//li")
        # info = response.xpath("//div[@class='maincon']//h2/text()").extract()
        for li in li_list:
            item = {}
            item["name"] = li.xpath(".//h2/text()").extract_first()
            item["title"] = li.xpath(".//h2/span/text()").extract_first()
            # print(item)
            yield item
        # print(info)

