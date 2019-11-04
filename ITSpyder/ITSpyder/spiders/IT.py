# -*- coding: utf-8 -*-
import scrapy
from ITSpyder.items import ItspyderItem
from ITSpyder.settings import SQL_DATETIME_FORMAT
import datetime
from ITSpyder.utils.url_id import get_md5
class ItSpider(scrapy.Spider):
    name = 'IT'
    allowed_domains = ['cec.jmu.edu.cn']
    url = 'http://cec.jmu.edu.cn/'
    start_urls = ['http://cec.jmu.edu.cn/']
    other_urls = [
        # 通知公告
        'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1041',
        # 就业工作
        'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1042',
        # 院务工作
        'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1043',
        # 学院新闻
        'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1044',
        # 教学工作
        # 'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1100',
        # 科研信息
        # 'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1103',
        # 学生工作
        # 'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1112',
        # 科研工作
        # 'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1010',
        # 学院风光
        # 'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1004',
    ]

    def parse(self, response):
        all_menus = []
        print(response)
        selector = scrapy.Selector(response)
        menus = selector.xpath("//a[@class='menu0_0_']/@href").extract()
        for menu in menus:
            if "http" not in menu and "index" not in menu:
                menu = self.url+menu
                all_menus.append(menu)

        for other_url in self.other_urls:
            all_menus.append(other_url)

        all_menus = set(all_menus)
        for menu in all_menus:
            yield scrapy.Request(url=menu, callback=self.parse_info)

    def parse_info(self, response):
        selector = scrapy.Selector(response)
        infos = selector.xpath("//a[@class='c124907']/@href").extract()
        next = selector.xpath("//a[@class='Next']/@href").extract()
        if next:
            next = "".join(next)
            nextUrl = "http://cec.jmu.edu.cn/list.jsp"+next
            #yield scrapy.Request(url=nextUrl, callback=self.parse_info, dont_filter=True)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info)
        for info in infos:
            if "http" not in info:
                #print('----')
                info = self.url+info
            if "cec" in info:
                #print('0000')
                yield scrapy.Request(url=info, callback=self.parse_content)


    @staticmethod
    def parse_content(response):
        print(1)
        selector = scrapy.Selector(response)
        item = ItspyderItem()
        print(111)
        title = selector.xpath("//title/text()").extract()[0]
        time = selector.xpath("//span[@class='timestyle124904']/text()").extract()[0]
        url = response.url
        content1 = selector.css("form[name='form124904a'] *:not(style)::text").extract()
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                         '').replace(
            '\"', '')
        time = "".join(time).replace('                 ', '')
        item['title'] = title
        item['time'] = time
        item['content'] = content2
        item['url'] = url
        item['url_object_id'] = get_md5(response.url)
        # item['time'] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        yield item
