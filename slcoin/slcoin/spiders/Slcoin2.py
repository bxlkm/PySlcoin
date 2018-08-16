__author__ = 'zyx'

import scrapy
import time
import re
from slcoin.items import SlcoinItem


class SlcoinSpider(scrapy.Spider):
    name = "slcoin2"
    allowed_domains = ["coingecko.com"]
    start_urls = [
        "https://www.coingecko.com/en",
    ]

    def parse(self, response):
        new = response.xpath('//*[@id="gecko-table"]/tbody')
        item = SlcoinItem()
        item["coin_type"] = new.xpath(
            '//*[@id="gecko-table"]/tbody/tr[5]/td[2]/div/div[2]/a/span[1]/text()').extract_first()
        item["coin_money"] = re.sub("\$|\s|,", "",
                                    new.xpath('//*[@id="gecko-table"]/tbody/tr[5]/td[3]/a/span/text()').extract_first())
        item["time"] = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        yield item
