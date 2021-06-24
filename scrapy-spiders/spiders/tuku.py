import scrapy

from ..items import TukuItem


class TukuSpider(scrapy.Spider):
    name = 'tuku'
    allowed_domains = ['521609.com']
    start_urls = ['http://www.521609.com/tuku/']

    def parse(self, response):
        li_list = response.xpath('/html/body/div[4]/div[3]/ul/li')

        for li in li_list:
            img_src = 'http://www.521609.com' + li.xpath('./a/img/@src').get()
            img_name = (li.xpath('./a/img/@alt').get() + '.jpg').replace('?', '')
            img_page_url = 'http://www.521609.com/' + li.xpath('./a/@href').get()
            item = TukuItem(img_src=img_src, img_name=img_name,img_page_url = img_page_url)
            # print(item)

            yield item



