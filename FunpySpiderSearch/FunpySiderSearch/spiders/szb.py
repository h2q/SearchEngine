import scrapy
import re
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.szb.szbItem import szbItem, szbItemLoader

from FunpySpiderSearch.utils.common import get_md5


class szbSpider(scrapy.Spider):
    name = "szb"
    allowed_domains = ["szb.jmu.edu.cn"]
    url="http://szb.jmu.edu.cn/"
    start_urls = ['http://szb.jmu.edu.cn/']
    other_urls=['http://szb.jmu.edu.cn/bmdt/xydt.htm',
                'http://szb.jmu.edu.cn/tztg.htm',
                'http://szb.jmu.edu.cn/yjsgz.htm',
                'http://szb.jmu.edu.cn/djgz.htm',
                'http://szb.jmu.edu.cn/hyap.htm',
                'http://szb.jmu.edu.cn/jxgz.htm',
                'http://szb.jmu.edu.cn/jxck.htm',
                'http://szb.jmu.edu.cn/bwgk.htm'
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//*[@id='t1_1_']//@href").extract()
        for menu in menus:
            if "http" not in menu:
                menu1 = self.url + menu
                new_menus.append(menu1)
        for other_url in self.other_urls:
            new_menus.append(other_url)
        new_menus = set(new_menus)
        for new_menu in new_menus:
            yield scrapy.Request(url=new_menu, callback=self.parse_info,dont_filter = True)

    def parse_info(self, response):  # 得到所有的*.html的页面链接
        selector = scrapy.Selector(response)
        infos = selector.xpath("//a[@target='_blank']/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//span[@class='NextDisabled'][1]").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = parse.urljoin(response.url,next)
            print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info,dont_filter = True)
        for info in infos:
            if "http" not in info:
                info = parse.urljoin(response.url,info)
                print(info)
            if "szb" in info:
                yield scrapy.Request(url=info, callback=self.parse_content,dont_filter = True)



    @staticmethod
    def parse_content(response):
        print("11111")
        szb_item = szbItem()
        # 通过item loader加载item
        item_loader = szbItemLoader(item=szb_item, response=response)

        selector = scrapy.Selector(response)
        title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        time = selector.xpath("//*[@id='infocontent']//div[1]/span/text()").extract()[0]  # 得到页面的发布时间
        url = response.url  # 页面链接
        content1 = selector.css("form[name='_newscontent_fromname'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                        '').replace(
            '\"', '')
        crawl_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time",crawl_time)
        # 调用这个方法来对规则进行解析生成item对象
        szb_item = item_loader.load_item()
        print("-"*30)
        print(szb_item)
        print("-" * 30)
        # 已经填充好了值调用yield传输至pipeline
        yield szb_item

