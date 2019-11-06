import scrapy
from scrapy.http import Request
from urllib import parse

from FunpySpiderSearch.sites.marine.marineItem import marineItem, marineItemLoader

from FunpySpiderSearch.utils.common import get_md5


class marineSpider(scrapy.Spider):
    name = "marine"
    allowed_domains = ["mei.jmu.edu.cn"]
    url="http://mei.jmu.edu.cn/"
    start_urls = ['http://mei.jmu.edu.cn/']
    other_urls=['http://mei.jmu.edu.cn/index/xyxw/xyxw.htm',
                'http://mei.jmu.edu.cn/index/tzgg/tzgg.htm',
                'http://mei.jmu.edu.cn/index/jxgl/jxgl.htm',
                'http://mei.jmu.edu.cn/index/mzhy/mzhy.htm',
                'http://mei.jmu.edu.cn/index/xsgz/xsgz.htm',
                'http://mei.jmu.edu.cn/index/cyjyypx/cyjyypx.htm',
                'http://mei.jmu.edu.cn/index/xzzx/xzzx.htm',
    ]

    def parse(self, response):  # 得到所有的菜单栏链接
        new_menus = []
        selector = scrapy.Selector(response)
        menus = selector.xpath("//div[@class='memuskin1']/a/@href").extract()
        for menu in menus:
            if "http" not in menu:
                menu1 = self.url + menu
                new_menus.append(menu1)
        for other_url in self.other_urls:
            new_menus.append(other_url)
        new_menus = set(new_menus)
        for new_menu in new_menus:
            yield scrapy.Request(url=new_menu, callback=self.parse_info)

    def parse_info(self, response):  # 得到所有的*.html的页面链接
        selector = scrapy.Selector(response)
        infos = selector.xpath("//table[@class='columnStyle']//a/@href").extract()  # 得到每个菜单栏链接页面的所有info/*.html链接
        next = selector.xpath("//a[@class='Next'][1]/@href").extract()
        if next:  # 假如有下一页继续爬取
            next = "".join(next)
            nextUrl = parse.urljoin(response.url,next)
            print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse_info)
        for info in infos:
            if "http" not in info:
                info = parse.urljoin(response.url,info)
                print(info)
            if "mei" in info:
                yield scrapy.Request(url=info, callback=self.parse_content)



    @staticmethod
    def parse_content(response):
        print("11111")
        marine_item = marineItem()
        # 通过item loader加载item
        item_loader = marineItemLoader(item=marine_item, response=response)

        # 将后面的指定规则进行解析。
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/span/text()")
        #item_loader.add_xpath("title", "//td[@class='titlestyle124904']/text()")
       # title = selector.xpath("//title/text()").extract()[0]  # 得到页面的标题
        selector = scrapy.Selector(response)
        title = selector.xpath("//span[@class='disinfo_title']/text()").extract()[0]  # 得到页面的标题
        url = response.url  # 页面链接
        content1 = selector.css("div[id='vsb_content'] *:not(style)::text").extract()  # 得到页面的内容
        content2 = "".join(content1).replace(u'\r\n', '').replace(u'\xa0', u'').replace(' ', '').replace('\'',
                                                                                                        '').replace(
            '\"', '')
        date=selector.xpath("//span[@class='cn_unnamed2']/span[@class='cn_unnamed2']/span[@class='style4']/text()").extract()
        create_date="".join(date).replace('\r\n','')
        print(create_date)
        item_loader._add_value("title", title)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader._add_value("content", content2)
        item_loader._add_value("crawl_time",create_date)



        # 调用这个方法来对规则进行解析生成item对象
        marine_item = item_loader.load_item()
        print("888")
        # 已经填充好了值调用yield传输至pipeline
        yield marine_item

