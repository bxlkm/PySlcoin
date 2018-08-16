# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import os

# if __name__ == '__main__':
#     os.system("scrapy crawl slcoin")


# 每n秒执行一次
def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("爬取一次")
        os.system("scrapy crawl slcoin1")
        time.sleep(n)


# 60s
timer(5)
# # os.system("scrapy crawl slcoin1")
# # os.system("scrapy crawl slcoin2")
# # os.system("scrapy crawl slcoin3")
# # os.system("scrapy crawl slcoin4")
# import time
# import os
#
# while True:
#     os.system("scrapy crawl News")
#     time.sleep(300)  #每隔一天运行一次 24*60*60=86400s
