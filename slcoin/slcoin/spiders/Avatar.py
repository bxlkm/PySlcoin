__author__ = 'zyx'

import scrapy
import time
from slcoin.items import AvatarItem


class AvatarSpider(scrapy.Spider):
    name = "avatar"
    allowed_domains = ["www.baidu.com"]
    start_urls = [
        "https://cn.bing.com/images/search?q=%E6%98%B4%E5%AE%BF%E4%B8%83%E6%98%9F&FORM=ISTRTH&id=24E63DD3DD5D9263213751E11C329F68E8DA06D4&cat=%E5%8A%A8%E6%BC%AB&lpversion=",
    ]

    def parse(self, response):
        list = response.xpath('//*[@id="imgid"]/div[1]/ul')
        url = list.xpath('//*[@id="imgid"]/div[1]/ul/li[1]/div/a/@href').extract()
        item = AvatarItem()
        item["url"] = url
        yield item
