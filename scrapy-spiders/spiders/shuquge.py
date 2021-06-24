import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ShuqugeSpider(CrawlSpider):
    name = 'shuquge'
    allowed_domains = ['www.shuquge.com']
    start_urls = ['http://www.shuquge.com/category/{}_1.html'.format(i) for i in range(1, 8)]
    # print(start_urls)

    rules = (
        Rule(LinkExtractor(allow=r'/category/\d_\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[4]/div[2]/div[1]/ul/li')
        for li in li_list:
            item = {}
            book_url = li.xpath('./span[2]/a/@href').get()
            category = li.xpath('./span[1]/text()').get()
            book_name = li.xpath('./span[2]/a/text()').get()

            item['book_url'] = book_url
            item['category'] = category
            item['book_name'] = book_name
            yield scrapy.Request(url=item['book_url'], callback=self.parse_book_item, meta={'item': item})
            # print(item)

        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()

        # return item

    def parse_book_item(self, response):

        chapter_list = response.xpath('/html/body/div[5]/dl/dd')
        item = response.meta['item']
        #http://www.shuquge.com/txt/136743/index.html
        item_url_list = item['book_url'].rsplit('/', 2)
        #http://www.shuquge.com/txt/74742
        item_url_with_id = '/'.join(item_url_list[0:2])
        book_id = item_url_list[1]
        book_name = item['book_name']
        category = item['category']

        chapters = []
        # for chapter in chapter_list:
        #     chapter_name = chapter.xpath('./a/text()').get()
        #     print(chapter_name)
        #     chapter_url = item_url_tmp + '/' + chapter.xpath('./a/@href').get()
        #     response = requests.get(url=chapter_url)
        #     response.encoding = 'utf-8'
        #     response = Selector(response.text)
        #     chapter_content = ''.join([i.strip() for i in response.xpath('//*[@id="content"]/text()').getall()])
        #     print(chapter_content)
        #     chapters.append({"chapter_name": chapter_name, "chapter_url": chapter_url,'chapter_content':chapter_content})

        for chapter in chapter_list:
            chapter_name = chapter.xpath('./a/text()').get()
            #25061633.html
            chapter_id = chapter.xpath('./a/@href').get().split('.')[0]
            chapter_url = item_url_with_id + '/' + chapter_id + '.html'
            # print(chapter_url)
            chapter_item = {"category": category,"book_name": book_name, "book_id": book_id, "chapter_name": chapter_name, "chapter_url": chapter_url,
                            'chapter_id': chapter_id}
            chapters.append(chapter_item)
            yield scrapy.Request(url=chapter_url, callback=self.parse_chapter_item, meta={'chapter_item': chapter_item})

        item['book_id'] = book_id
        item['chapters'] = chapters

        # print(item)
        yield item

    def parse_chapter_item(self, response):
        chapter_item = response.meta['chapter_item']
        chapter_content = '\n'.join([i.strip().replace('\xa0','') for i in response.xpath('//*[@id="content"]/text()').getall()])
        chapter_item['chapter_content'] = chapter_content
        # print(chapter_item)
        yield chapter_item
