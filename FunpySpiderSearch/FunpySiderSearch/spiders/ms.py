import scrapy
from scrapy.http import Request
from urllib import parse
import re
from FunpySpiderSearch.sites.ms.msItem import msItem, msItemLoader

from FunpySpiderSearch.utils.common import get_md5


class msSpider(scrapy.Spider):
    name = "ms"
    allowed_domains = ["ms.jmu.edu.cn"]
    url = "http://ms.jmu.edu.cn/"
    start_urls = ['http://ms.jmu.edu.cn/']
    other_urls =['http://ms.jmu.edu.cn/index/xwdt.htm',
                'http://ms.jmu.edu.cn/index/ywgk.htm',
                'http://ms.jmu.edu.cn/index/xsgz.htm',
                'http://ms.jmu.edu.cn/index/jygz.htm',
                'http://ms.jmu.edu.cn/index/ywgk.htm',
                'http://ms.jmu.edu.cn/ind_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1035',
                'http://ms.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1004'
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//td[@class='flyoutLink']/a/@href").extract()
        for menu in menus:
            # print("$$$")
            # print(menus)
            if "http" not in menu:
                menu1 = self.url + menu
                # print(menu1)
                new_menus.append(menu1)
        for other_url in self.other_urls:
            new_menus.append(other_url)
        new_menus = set(new_menus)
        for new_menu in new_menus:
            # print("new_mune:")
            # print(new_menu)
            yield scrapy.Request(url=new_menu, callback=self.parse_info)

    def parse_info(self, response):  # 得到所有的*.html的页面链接
        selector = scrapy.Selector(response)
        infos = selector.xpath("//a[@class='c124899']/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//a[@class='Next'][1]/@href").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = parse.urljoin(response.url,next)
            # print("nextUrl")
            # print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info)
        for info in infos:
            # print("info:")
            if "http" not in info:
                info = parse.urljoin(response.url,info)
              #  print(info)
            if "ms" in info:
             #   print(info)
                yield scrapy.Request(url=info, callback=self.parse_content)



    @staticmethod
    def parse_content(response):
        print("11111")
        ms_item = msItem()
        # 通过item loader加载item
        item_loader = msItemLoader(item=ms_item, response=response)

        selector = scrapy.Selector(response)
        title = selector.xpath("//td[@class='biaoti3']/text()").extract()[0]  # 得到页面的标题
        time = selector.xpath("//td[@class='huizi']/text()").extract()[0]  # 得到页面的发布时间
      #  print("*")
      #  print(time)
        url = response.url  # 页面链接
        content1 = selector.css("div[id='vsb_content'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                        '').replace(
            '\"', '')
        #crawl_time = "".join(time).replace('\r\n', '')
        print(crawl_time)
        crawl_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time)
        print(crawl_time.group(0))
        print(title)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time", crawl_time.group(0))



        # 调用这个方法来对规则进行解析生成item对象
        ms_item = item_loader.load_item()
        print("888")
        # 已经填充好了值调用yield传输至pipeline
        yield ms_item
