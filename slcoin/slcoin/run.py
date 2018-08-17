# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os


# 每n秒执行一次
def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬取一次")
        os.system("scrapy crawl slcoin")
        time.sleep(n)


# 时间
timer(5)
