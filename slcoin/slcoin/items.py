# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SlcoinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    coin_type = scrapy.Field()
    coin_money = scrapy.Field()
    time = scrapy.Field()
    coin_upDown = scrapy.Field()

