# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
#from scrapy import log
import pymongo
from openpyxl import Workbook

#保存为mongdo
class LagouPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.tab = settings['MONGODB_COLLECTION']
        connection = pymongo.MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.tab]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
#        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.tab), level=log.DEBUG, spider=spider)
        return item

# #保存到xlsx
# class LagouPipeline(object):
#     def __init__(self):
#         self.wb = Workbook()
#         self.ws = self.wb.active
#         self.ws.append(['bookname', 'raleasetime', 'salary', 'experience', 'companyname', 'Education'])
#
#     def process_item(self, item, spider):
#         line = [item['bookname'], item['raleasetime'], item['salary'], item['experience'], item['companyname'], item['Education']]
#         self.ws.append(line)
#         slice.wb.save('lagou.xlsx')
#         return item

