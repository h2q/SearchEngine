# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class ItspyderPipeline(object):

    def process_item(self, item, spider):
        '''
        with open('test.txt', 'a', encoding='utf-8') as fp:
            fp.write(item['title']+'  ' + item['time']+'\n'
                     + item['url']+' '+item['content']+'\n')
            fp.close()
        '''
        return item



class MysqlTwistedPipeline(object):
    # 采用异步机制写入mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # cls实际就是本类MysqlTwistedPipeline
        param = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        # adbapi将一些操作编程异步化操作
        dbpool = adbapi.ConnectionPool("MySQLdb", **param)

        # 实例化一个pipeline
        return cls(dbpool)

    def process_item(self, item, spider):
        # 指定操作的方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 异常处理
        query.addErrback(self.handle_error, item, spider)

    @staticmethod
    def handle_error(failure, item, spider):
        print("错误信息提示")
        print(failure)

    @staticmethod
    def do_insert(cursor, item):
        insert_sql = 'insert into it VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE crawl_time=VALUES(crawl_time)'
        #try:
        print("开始插入数据")
        print(item['title'])
        print(item['time'])
        print(item['url'])
        print(item['url_object_id'])
        print(item['content'])
        cursor.execute(insert_sql, (item['title'], item['url'], item['url_object_id'],
                                    item['content'], item['time'],))
        print("插入成功")
