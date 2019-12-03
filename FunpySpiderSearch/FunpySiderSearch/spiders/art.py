import scrapy
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.art.artItem import artItem, artItemLoader

from FunpySpiderSearch.utils.common import get_md5


class artSpider(scrapy.Spider):
    name = "art"
    allowed_domains = ["atrs.jmu.edu.cn"]
    url="http://arts.jmu.edu.cn/"
    start_urls = ['http://arts.jmu.edu.cn/']
    other_urls=['http://arts.jmu.edu.cn/index/tzgg.htm',
                'http://arts.jmu.edu.cn/index/xydt.htm',
                'http://arts.jmu.edu.cn/index/xshd.htm'
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//div[@class='menu']/a/@href").extract()
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
            if "art" in info:
                yield scrapy.Request(url=info, callback=self.parse_content,dont_filter = True)



    @staticmethod
    def parse_content(response):
        print("11111")
        art_item = artItem()
        # 通过item loader加载item
        item_loader = artItemLoader(item=art_item, response=response)

        # 将后面的指定规则进行解析。
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/span/text()")
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/text()")
       # title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        selector = scrapy.Selector(response)
        title = selector.xpath("//div[@class='pop_tit']/text()").extract()[0]  # 得到页面的标题
        url = response.url  # 页面链接
        content1 = selector.css("div[id='vsb_content'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                        '').replace(
            '\"', '')
        date=selector.xpath("//span[@class='style6']/text()").extract()
        create_date="".join(date).replace('\r\n','')
        print(create_date)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time",create_date)
        # 调用这个方法来对规则进行解析生成item对象
        art_item = item_loader.load_item()
        print("-"*30)
        print(art_item)
        print("-" * 30)
        # 已经填充好了值调用yield传输至pipeline
        yield art_item

