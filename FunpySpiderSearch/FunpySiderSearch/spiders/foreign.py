import scrapy
import re
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.foreign.foreignItem import foreignItem, foreignItemLoader

from FunpySpiderSearch.utils.common import get_md5


class foreignSpider(scrapy.Spider):
    name = "foreign"
    allowed_domains = ["sfl.jmu.edu.cn"]
    url="http://sfl.jmu.edu.cn/"
    start_urls = ['http://sfl.jmu.edu.cn/']
    other_urls=['http://sfl.jmu.edu.cn/xydt1/tztg.htm',
                'http://sfl.jmu.edu.cn/xydt1/xyxw.htm',
                'http://sfl.jmu.edu.cn/jxky1/wjtz.htm',
                'http://sfl.jmu.edu.cn/ywgk/ywgk.htm',
                'http://sfl.jmu.edu.cn/txgz1/txdt.htm'
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//a[@class='wlink']/a/@href").extract()
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
        infos = selector.xpath("//table[@class='columnStyle']//a/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//a[@class='Next'][1]/@href").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = parse.urljoin(response.url,next)
            print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info,dont_filter = True)
        for info in infos:
            if "http" not in info:
                info = parse.urljoin(response.url,info)
                print(info)
            if "sfl" in info:
                yield scrapy.Request(url=info, callback=self.parse_content,dont_filter = True)



    @staticmethod
    def parse_content(response):
        print("11111")
        foreign_item = foreignItem()
        # 通过item loader加载item
        item_loader = foreignItemLoader(item=foreign_item, response=response)

        # 将后面的指定规则进行解析。
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/span/text()")
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/text()")
       # title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        selector = scrapy.Selector(response)
        title = selector.xpath("//td[@class='biaoti3']/text()").extract()[0]  # 得到页面的标题
        time=selector.xpath("//td[@class='huizi']/text()").extract()[0]
        url = response.url  # 页面链接
        content1 = selector.css("div[id='vsb_content'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                         '').replace(
            '\"', '')
        crawl_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",time)
        print(crawl_time.group(0))
        print(title)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time",crawl_time.group(0))
        # 调用这个方法来对规则进行解析生成item对象
        foreign_item = item_loader.load_item()
        print("-"*30)
        print(foreign_item)
        print("-" * 30)
        # 已经填充好了值调用yield传输至pipeline
        yield foreign_item

