# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    desc = scrapy.Field()


class TukuItem(scrapy.Item):
    # define the fields for your item here like:
    img_src = scrapy.Field()
    img_name = scrapy.Field()
    img_page_url = scrapy.Field()


class SunItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    state = scrapy.Field()
    # img_page_url = scrapy.Field()


class SunItemDetail(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    # state = scrapy.Field()
    # img_page_url = scrapy.Field()
