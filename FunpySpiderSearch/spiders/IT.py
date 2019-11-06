import scrapy
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.IT.ITItem import ITItem, ITItemLoader

from FunpySpiderSearch.utils.common import get_md5


class ITSpider(scrapy.Spider):
    name = "IT"
    allowed_domains = ["cec.jmu.edu.cn"]
    url="http://cec.jmu.edu.cn/"
    start_urls = ['http://cec.jmu.edu.cn/']
    other_urls=['http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1044',
                'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1043',
                'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1042',
                'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1041'
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//a[@class='menu0_1_']/@href").extract()
        for menu in menus:
            if "http" not in menu and "index" not in menu:
                menu1 = self.url + menu
                new_menus.append(menu1)
        for other_url in self.other_urls:
            new_menus.append(other_url)
        new_menus = set(new_menus)
        for new_menu in new_menus:
            yield scrapy.Request(url=new_menu, callback=self.parse_info)

    def parse_info(self, response):  # 得到所有的info/*.html的页面链接
        selector = scrapy.Selector(response)
        infos = selector.xpath("//a[@class='c124907']/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//a[@class='Next']/@href").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = "http://cec.jmu.edu.cn/list.jsp" + next
            yield scrapy.Request(url=nextUrl, callback=self.parse_info)
        for info in infos:
            if "http" not in info:
                info = self.url + info
            if "cec" in info:
                yield scrapy.Request(url=info, callback=self.parse_content)



    @staticmethod
    def parse_content(response):
        print("11111")
        IT_item = ITItem()
        # 通过item loader加载item
        item_loader = ITItemLoader(item=IT_item, response=response)

        # 将后面的指定规则进行解析。
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/span/text()")
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/text()")
       # title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        selector = scrapy.Selector(response)
        title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        crawl_time=selector.xpath("//span[@class='timestyle124904']/text()").extract()[0] #得到页面的发布时间
        url = response.url  # 页面链接
        content1 = selector.css("form[name='form124904a'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                        '').replace(
            '\"', '')
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time",crawl_time)


        # 调用这个方法来对规则进行解析生成item对象
        IT_item = item_loader.load_item()
        print("888")
        # 已经填充好了值调用yield传输至pipeline
        yield IT_item

