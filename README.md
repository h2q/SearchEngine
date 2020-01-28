学院搜索引擎
===
集美大学学院的搜索引擎。迭代16届版本。

可用功能（截至2019-11-10）
===
```
1.增加了多个学院
2.支持拼音搜索
```
如何开始使用？（截至2019-11-10 ）
===
参考链接：https://blog.csdn.net/qq_23079443/article/details/73920584
1.爬虫端
 ```
  1）安装ElasticSearch6.8.0,配置ElasticSearch-analysis-ik，还有ik拼音插件,安装ElasticSearch-head
  2）执行runMeFirst.py  加载数据
 ```
2.网页端
```
进入目录，命令行执行python manage.py runserver。浏览器进入localhost:8000即可。
```
