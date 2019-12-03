import time
import  datetime
import os
from scrapy import cmdline
def doSth():
    # 把爬虫程序放在这个类里 zhilian_spider 是爬虫的name
    os.system('scrapy crawlall')

# 想几点更新,定时到几点
def time_ti(h=1, m=10):
    while True:
        now = datetime.datetime.now()
        print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            print("我在运行")
            doSth()

        # 每隔60秒检测一次
        time.sleep(60)

time_ti()



