__author__ = 'zyx'

import scrapy
import time
from slcoin.items import SlcoinItem


class SlcoinSpider(scrapy.Spider):
    name = "slcoin"
    allowed_domains = ["coingecko.com"]
    start_urls = [
        "https://www.coingecko.com/en?sort_by=price",
    ]

    def parse(self, response):
        list = response.xpath('//*[@id="gecko-table"]/tbody')
        coin_type = list.xpath(
            '//*[@id="gecko-table"]/tbody/tr/td[2]/div/div[1]/span/text()').extract()
        coin_money = list.xpath('//*[@id="gecko-table"]/tbody/tr/td[3]/a/span/text()').extract()
        coin_upDown = list.xpath('//*[@id="gecko-table"]/tbody/tr/td[4]/div/span/text()').extract()
        print(coin_upDown)
        for i in range(0, 100):
            if coin_type[i] == 'BTC' or coin_type[i] == 'PBT' or coin_type[i] == 'YBC' or coin_type[i] == 'BCH' or \
                    coin_type[i] == 'MKR' or coin_type[i] == 'XIN' or coin_type[i] == 'ETH' or coin_type[i] == 'ZEC' or \
                    coin_type[i] == 'DGD' or coin_type[i] == 'DCR' or coin_type[i] == 'VERI' or coin_type[i] == 'AU' or \
                    coin_type[i] == 'NEO' or coin_type[i] == 'MTL' or coin_type[i] == 'CYT' or coin_type[i] == 'TIME' or \
                    coin_type[i] == 'GAS' or coin_type[i] == 'GAM' or coin_type[i] == 'BCAP' or coin_type[i] == 'PLU':
                item = SlcoinItem()
                item['coin_type'] = coin_type[i]
                item['coin_money'] = coin_money[i]
                item["time"] = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
                item["coin_upDown"] = coin_upDown[i]
                yield item
            else:
                print("I do not want it")

        next_page = response.xpath(
            '//*[@id="wrapper"]/div[3]/div[4]/div[2]/div[2]/ul/li[7]/a/@href').extract()
        next_page = ','.join(next_page)
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
