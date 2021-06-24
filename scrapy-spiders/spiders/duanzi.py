import scrapy


class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['duanziwang.com']
    start_urls = ['http://www.duanziwang.com/wenzi/5/']
    url = 'http://www.duanziwang.com/wenzi/%d/'
    page_num = 6

    def parse(self, response):
        dl_lsit = response.xpath('/html/body/div[4]/div[1]/div[1]/dl')
        # print(dl_lsit)

        for dl in dl_lsit:
            item = {}

            item['title'] = dl.xpath('./span/dd/a/strong/text()').extract_first()
            conten_list = [data.extract().strip() for data in dl.xpath('./dd//text()')]
            item['content'] = ''.join(conten_list)
            # print(item)
            yield item
        if self.page_num < 10:
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url,callback=self.parse)
