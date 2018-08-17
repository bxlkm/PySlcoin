from urllib import response

__author__ = 'zyx'
#
import scrapy
import time
import re
from slcoin.items import SlcoinItem


class SlcoinSpider(scrapy.Spider):
    name = "slcoin"
    allowed_domains = ["www.feixiaohao.com"]
    start_urls = [
        "https://www.feixiaohao.com/#USD",
    ]

    def parse(self, response):
        item = SlcoinItem()
        list = response.xpath('//*[@id="table"]/tbody')
        coin_type = list.xpath('//tr/td[2]/a/img/@alt').extract()
        coin_money = list.xpath('//tr/td[4]/a/@data-usd').extract()
        coin_upDown = list.xpath('//tr/td[7]/span/text()').extract()
        for i in range(0, 100):
            if coin_type[i] == 'BTC-比特币' or coin_type[i] == 'ETH-以太坊' or coin_type[i] == 'EOS-柚子' or coin_type[
                i] == 'LTC-莱特币' or \
                    coin_type[i] == 'XMR-门罗币' or coin_type[i] == 'NEO-小蚁' or coin_type[i] == 'ETC-以太经典' or coin_type[
                i] == 'OMG-嫩模币' or \
                    coin_type[i] == 'BNB-币安币' or \
                    coin_type[i] == 'HT-火币积分' or coin_type[i] == 'ZEC-大零币' or coin_type[i] == 'DCR' or coin_type[
                i] == 'MKR' or \
                    coin_type[i] == 'REP' or coin_type[i] == 'GXS-公信宝' or coin_type[i] == 'EMC-崛起币' or coin_type[
                i] == 'ZEN' or \
                    coin_type[i] == 'VERI' or coin_type[i] == 'XZC-小零币' or coin_type[i] == 'FCT-公证通':
                item = SlcoinItem()
                item['coin_type'] = re.sub("[\u4e00-\u9fa5]|-", "", coin_type[i])
                item['coin_money'] = coin_money[i]
                item["time"] = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
                item["coin_upDown"] = coin_upDown[i]
                yield item
            else:
                print("I do not want it")

                next_page = ['list_2.html#USD']
                next_page = ','.join(next_page)
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
