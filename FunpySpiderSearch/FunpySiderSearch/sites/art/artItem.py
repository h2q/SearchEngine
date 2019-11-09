import datetime
import re

import scrapy
from elasticsearch_dsl import connections
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

from FunpySpiderSearch.items import MysqlItem, ElasticSearchItem
from FunpySpiderSearch.settings import SQL_DATETIME_FORMAT
from FunpySpiderSearch.sites.art.es_art import artIndex
from FunpySpiderSearch.utils.common import real_time_count
from FunpySpiderSearch.utils.es_utils import generate_suggests
from FunpySpiderSearch.utils.mysql_utils import fun_sql_insert
from FunpySpiderSearch.utils.string_util import return_value, get_nums

# 与ElasticSearch进行连接,生成搜索建议
es_art_blog = connections.create_connection(artIndex)


art_COUNT_INIT = 0



class artItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class artItem(scrapy.Item, MysqlItem, ElasticSearchItem):
    """
    美术学院Item，命名规范: 域名+内容+Item
    """
    field_list = ['title', 'url', 'url_object_id', 'content', 'crawl_time']

    duplicate_key_update = ['crawl_time']

    table_name = 'art'

    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()

    def clean_data(self):
##        if self["front_image_url"]:
##            self["front_image_url"] = self["front_image_url"][0]
        #self["crawl_time"] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        # match_time = re.match("(\d+)-(\d+)-(\d+)", self["crawl_time"])
        # year = int(match_time.group(1))
        # month = int(match_time.group(2))
        # day = int(match_time.group(3))
        # today = datetime.datetime(year, month, day)
        # self["crawl_time"] = today.strftime(SQL_DATETIME_FORMAT)
        # print(self["crawl_time"])
        self["crawl_time"] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
#       date_str = self["create_date"].strip().replace("-", "").strip()
#       self["create_date"] = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
        #value = self["praise_nums"]
##        match_re = re.match(".*?(\d+).*", value)
##        if match_re:
##            nums = int(match_re.group(1))
##        else:
##            nums = 0
        #self["praise_nums"] = nums

    def save_to_mysql(self):
        self.clean_data()
        insert_sql = """insert into art(title,url,url_object_id,content,crawl_time) VALUES(%s,%s,%s,%s,%s)
                                                ON DUPLICATE KEY UPDATE  crawl_time=VALUES(crawl_time)"""
        sql_params = (
            self["title"],
            self["url"],
            self["url_object_id"],
            self["content"],
            self["crawl_time"],
        )
        return insert_sql, sql_params

    def save_to_es(self):
        """保存美术学院文章到es中"""
        self.clean_data()
        blog = artIndex()
        blog.title = self['title']
        blog.content = remove_tags(self["content"])
        blog.url = self["url"]
        blog.meta.id = self["url_object_id"]
        #blog.create_date = self["create_date"]
        # 在保存数据时必须传入suggest
        blog.suggest = generate_suggests(es_art_blog, artIndex,
                                         ((blog.title, 10), (blog.content, 4)))
        # , (blog.tags, 6)
        real_time_count('art_blog_count', art_COUNT_INIT)
        blog.save()

    def help_fields(self):
        for field in self.field_list:
            print(field, "= scrapy.Field()")


if __name__ == '__main__':
    instance = artItem()
    print(instance.help_fields())
    print("*" * 30)
    print("self.data_clean()")
    sql, params = fun_sql_insert(field_list=instance.field_list, duplicate_key_update=instance.duplicate_key_update,
                                 table_name=instance.table_name)
    print(sql)
    print(params)
