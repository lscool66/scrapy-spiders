import scrapy
import logging

class Doubantop250Spider(scrapy.Spider):
    name = 'doubantop250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        li_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')

        for li in li_list:
            item = {}
            item['title'] = li.xpath('.//div[@class="hd"]//span/text()').get()
            item['link'] = li.xpath('.//div[@class="hd"]//a/@href').get()
            item['rating_num'] = li.xpath('.//span[@class="rating_num"]/text()').get()
            item['num'] = li.xpath('.//div[@class="star"]/span[4]/text()').get()
            yield item
