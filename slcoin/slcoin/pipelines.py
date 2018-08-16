# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# import json
# # import MySQLdb
#
# from twisted.enterprise import adbapi
# import pymysql
#
#
# class SlcoinPipeline(object):
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
#         query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
#         return item
#
#     # 写入数据库中
#     def _conditional_insert(self, tx, item):
#         # print item['name']
#         sql = "insert into testpictures(name,url) values(%s,%s)"
#         params = (item["name"], item["url"])
#         tx.execute(sql, params)
#
#     @classmethod
#     def from_settings(cls, settings):
#         '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
#            2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
#            3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
#         dbparams = dict(
#             host=settings['MYSQL_HOST'],  # 读取settings中的配置
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=False,
#         )
#         dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
#         return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到
#
#     # 错误处理方法
#     def _handle_error(self, failue, item, spider):
#         print(failue)
#
#
# class JsonWithEncodingPipeline(object):
#     '''保存到文件中对应的class
#         1、在settings.py文件中配置
#         2、在自己实现的爬虫类中yield item,会自动执行'''
#
#     def __init__(self):
#         self.file = codecs.open('info.json', 'w', encoding='utf-8')  # 保存为json文件
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"  # 转为json的
#         self.file.write(line)  # 写入文件中
#         return item
#
#     def spider_closed(self, spider):  # 爬虫结束时关闭文件
#         self.file.close()
#
#
# ITEM_PIPELINES = {
#     'slcoin.pipelines.SlcoinPipeline': 300,  # 保存到mysql数据库
#     'slcoin.pipelines.JsonWithEncodingPipeline': 300,  # 保存到文件中
# }
from scrapy import log
import pymysql
import pymysql.cursors
import codecs
from twisted.enterprise import adbapi


class SlcoinPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)  # 调用插入的方法
        log.msg("-------------------连接好了-------------------")
        d.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        d.addBoth(lambda _: item)
        return d

    def _conditional_insert(self, conn, item, spider):
        log.msg("-------------------打印-------------------")

        # conn.execute("insert into coin_info (time, coin_type, coin_money ,coin_upDown) values(%s, %s, %s, %s)",
        #              (item['time'], item['coin_type'], item['coin_money'], item['coin_upDown']))
        conn.execute("""
                                update coin_mini set time = %s, coin_type = %s, coin_money = %s, coin_upDown = %s where coin_type = %s
                            """,
                     (item['time'], item['coin_type'], item['coin_money'], item['coin_upDown'], item['coin_type']))
        log.msg("-------------------一轮循环完毕-------------------")

    def _handle_error(self, failue, item, spider):
        print(failue)
