import scrapy
from scrapy.http import Request
from urllib import parse
import re
from FunpySpiderSearch.sites.PE.PEItem import PEItem, PEItemLoader

from FunpySpiderSearch.utils.common import get_md5


class PESpider(scrapy.Spider):
    name = "PE"
    allowed_domains = ["phys.jmu.edu.cn"]
    url = 'http://phys.jmu.edu.cn/'
    start_urls = ['http://phys.jmu.edu.cn/']
    other_urls = ['http://phys.jmu.edu.cn/xydt.htm',
                'http://phys.jmu.edu.cn/tztg.htm',
                'http://phys.jmu.edu.cn/index/ywgk.htm',
                'http://phys.jmu.edu.cn/xsgz.htm',
                'http://phys.jmu.edu.cn/djsz.htm',
                'http://phys.jmu.edu.cn/bkjy.htm',
                'http://phys.jmu.edu.cn/yjs.htm',
                'http://phys.jmu.edu.cn/xzzx.htm',

    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//a[@class='topurlstyle']/@href").extract()
        for menu in menus:
            if "http" not in menu:
                menu1 = self.url + menu
                new_menus.append(menu1)
        for other_url in self.other_urls:
            new_menus.append(other_url)
        new_menus = set(new_menus)
        for new_menu in new_menus:
            print(new_menu)
            yield scrapy.Request(url=new_menu, callback=self.parse_info)

    def parse_info(self, response):  # 得到所有的info/*.html的页面链接
        selector = scrapy.Selector(response)
        infos = selector.xpath("//a[@title='']/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//a[@class='Next'][1]/@href").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = parse.urljoin(response.url, next)
        #    print('nexturl')
         #   print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info)
        for info in infos:
         #   print('1:'+info)
            if "http" not in info:
                info = self.url + info
          #      print('2:' + info)
            if "phys" in info:
           #     print('3:' + info)
                yield scrapy.Request(url=info, callback=self.parse_content)



    @staticmethod
    def parse_content(response):
        print("11111")
        PE_item = PEItem()
        # 通过item loader加载item
        item_loader = PEItemLoader(item=PE_item, response=response)
        selector = scrapy.Selector(response)
        title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        time = selector.xpath("//font[@color='#999999']/text()").extract()[0] #得到页面的发布时间
        print("*")
        print(time)
        url = response.url  # 页面链接
        content1 = selector.css("div[id='vsb_content'] *:not(style)::text").extract()   # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                       '').replace(
             '\"', '')
        crawl_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", time)
        print(crawl_time.group(0))
        print(title)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time", crawl_time.group(0))


        # 调用这个方法来对规则进行解析生成item对象
        PE_item = item_loader.load_item()
        print("888")
        print(type(PE_item))
        # 已经填充好了值调用yield传输至pipeline
        yield PE_item
