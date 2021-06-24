import scrapy
from ..items import MovieItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['douban.com']
    start_urls = ['https://dianying.2345.com/list/-------1.html']
    url = 'https://dianying.2345.com/list/-------{page_num}.html'
    page_num = 2

    def parse(self, response):
        li_list = response.xpath('//*[@id="contentList"]/ul/li')
        for li in li_list:

            title = li.xpath('./div[2]/span[1]/em/a/text()').extract_first()
            detail_url = 'https:' + li.xpath('./div[2]/span[1]/em/a/@href').extract_first()
            item = MovieItem(title=title)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})
        # 手动对其他页面发请求
        if self.page_num < 5:
            new_url = self.url.format(page_num=self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url,callback=self.parse)

    # 解析详情页数据
    def parse_detail(self, response):
        item = response.meta['item']
        try:
            desc = response.xpath('//p[@class="pIntro pShow"]/span/text()').extract_first().strip()
        except Exception as e:
            print(e)
            desc = ''
        # desc = ''.join([i.extract().strip() for i in response.xpath('//*[@id="link-report"]/span[@property="v:summary"]/text()')])
        item['desc']=desc
        # print(item)
        yield item
