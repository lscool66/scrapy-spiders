# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import logging

import pymysql
# from scrapy.pipelines.media import MediaPipeline
import scrapy
from redis import Redis
from scrapy.pipelines.images import ImagesPipeline


class ShuqugeMysqlPipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='192.168.2.252', port=3306, user='root', password='123', db='spider',
                                    charset='utf8')
        print(self.conn)

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        if 'chapters' in item:
            sql = r'INSERT INTO books VALUES ("{book_id}","{book_url}","{category}","{book_name}");'.format(
                book_url=item['book_url'], category=item['category'], book_name=item['book_name'],
                book_id=item['book_id'])
            print(sql)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
        if 'chapter_content' in item:
            sql = r'INSERT INTO chapters VALUES ("{book_id}","{category}","{book_name}","{chapter_name}","{chapter_url}","{chapter_id}","{chapter_content}");'.format(
                book_id=item['book_id'], category=item['category'], book_name=item['book_name'],
                chapter_name=item['chapter_name'], chapter_url=item['chapter_url'], chapter_id=item['chapter_id'], chapter_content=item['chapter_content'])
            print(sql)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()


class ShuqugeBookPipeline:
    f = None
    csv_writer = None

    def open_spider(self, spider):
        self.f = open('book_data.csv', mode='a+', encoding='utf-8', newline='')
        self.csv_writer = csv.DictWriter(self.f, fieldnames=['book_url', 'category', 'book_name', 'book_id'])
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        if item['chapters']:
            self.csv_writer.writerow(item)
            logging.warning(item)

    def close_spider(self, spider):
        self.fp.close()


class ShuqugeChapterPipeline:
    fp = None

    # def open_spider(self, spider):
    #     self.fp = open('duanzi.txt', mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        # print(item)
        file_name = item['category'] + '-' + item['book_name'] + '-' + item['chapter_name'].repalce('"', ' ') + '.txt'
        self.fp = open(file_name, mode='a', encoding='utf-8')
        # for chapter in item['chapters']:
        #     self.fp.write(chapter['chapter_name'])
        #     self.fp.write(chapter['chapter_content'])
        self.fp.write(item['chapter_name'])
        self.fp.write('\n')
        self.fp.write(item['chapter_content'])
        print(file_name, "下载完毕")

    def close_spider(self, spider):
        self.fp.close()


class SunPipeline:
    # fp = None
    #
    # def open_spider(self, spider):
    #     self.fp = open('duanzi.txt', mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        # self.fp.write(':'.join(item.values()) + '\n')
        if item.__class__.__name__ == 'SunItem':
            title = item['title']
            state = item['state']
            logging.warning(item)
        else:
            content = item['content']
            logging.warning(item)
        return item

    # def close_spider(self, spider):
    #     self.fp.close()


class SunDetailPipeline:
    fp = None

    def open_spider(self, spider):
        self.fp = open('duanzi.txt', mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(':'.join(item.values()) + '\n')
        logging.warning(item)
        return item

    def close_spider(self, spider):
        self.fp.close()


class MyspiderPipeline:
    fp = None

    def open_spider(self, spider):
        self.fp = open('duanzi.txt', mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(':'.join(item.values()) + '\n')
        logging.warning(item)
        return item

    def close_spider(self, spider):
        self.fp.close()


class TukuPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print(item)
        yield scrapy.Request(url=item['img_src'], meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        print(item)
        file_path = item['img_name']
        return file_path

    def item_completed(self, results, item, info):
        return item


class MoviePipeline:
    fp = None

    def open_spider(self, spider):
        self.fp = open('movie.csv', mode='a', encoding='utf-8', newline='')
        self.csv_writer = csv.DictWriter(self.fp, fieldnames=['title', 'desc'])
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        # self.fp.write(':'.join(item.values()) + '\n')
        self.csv_writer.writerow(dict(item))
        logging.warning(item)
        return item

    def close_spider(self, spider):
        self.fp.close()


class MysqlPipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='192.168.2.252', port=3306, user='root', password='123', db='spider',
                                    charset='utf8')
        print(self.conn)

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        sql = r'INSERT INTO duanzi VALUES ("%s","%s");' % (item['title'], item['content'])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()


class RedisPipeline:
    conn = None

    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1', port=6379)
        print(self.conn)

    def process_item(self, item, spider):
        self.conn.lpush('duanzi', str(item))
        return item
