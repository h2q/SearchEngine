学院搜索引擎
===
集美大学学院的搜索引擎。

可用功能（2019-11-10）
===
```
1.对计算机工程学院搜索
2.对轮机学院搜索
3.对美术学院搜索
4.对上述学院综合搜索
```
如何开始使用？
===
1.爬虫端
 ```
  1）安装ElasticSearch6.8.0,配置ElasticSearch-analysis-ik插件,安装Redis(可选配置ElasticSearch-head)
  2）新建数据库mtianyan; Navicat导入mysql文件; 
  3）执行 sites/es_* 配置ELasticPipeline
  4）cd FunpySpiderSearchEngine
     pip install -r requi.txt
     scrapy crawl IT
     scrapy crawl marine
     scrapy crawl art
 ```
2.网页端
```
进入目录，命令行执行python manage.py runserver。浏览器进入localhost:8000即可。
```
