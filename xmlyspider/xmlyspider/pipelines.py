# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.exceptions import DropItem
#from scrapy import log
import pymongo
import datetime
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# #Mongo
# class XmlyspiderPipeline(object):
#     def __init__(self):
#         self.server = settings['MONGODB_SERVER']
#         self.port = settings['MONGODB_PORT']
#         self.db = settings['MONGODB_DB']
#         self.tab = settings['MONGODB_COLLECTION']
#         connection = pymongo.MongoClient(self.server, self.port)
#         db = connection[self.db]
#         self.collection = db[self.tab]
#
#     def process_item(self, item, spider):
#         self.collection.insert(dict(item))
#         return item

class XmlyMysqlPipeline(object):

    def __init__(self):
        time1 = datetime.datetime.now().strftime('%Y-%m-%d').replace('-','')
        self._tabname = 'sound_' + time1
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="ubuntu", db="spider", charset="utf8")
        self.cursor = self.conn.cursor()
        try:
            sql = """CREATE TABLE %s (
                id int PRIMARY KEY AUTO_INCREMENT, Title varchar (255), Albumtitle varchar(255),
                SinglePlayCount VARCHAR(255), Albumscore VARCHAR(255), LikeCount VARCHAR (255),
                CommentsCount VARCHAR (255), TotalPlayCounts VARCHAR (255), Duration VARCHAR (255),
                CreatedTime VARCHAR (255), displayDiscountedPrice VARCHAR (255),
                Nickname VARCHAR (255), category_title VARCHAR (255), trackId VARCHAR (255)
                 )""" % self._tabname
            self.cursor.execute(sql)
        except:
            pass


    def process_item(self, item, spider):
        sql = ("insert into {} (Title, Albumtitle, SinglePlayCount, Albumscore, LikeCount, CommentsCount, \
                TotalPlayCounts, Duration, CreatedTime, displayDiscountedPrice, Nickname, category_title, trackId) \
                values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (item['Title'], item['Albumtitle'], item['SinglePlayCount'], item['Albumscore'], \
                item['LikeCount'], item['CommentsCount'], item['TotalPlayCounts'], item['Duration'], \
                item['CreatedTime'], item['displayDiscountedPrice'], item['Nickname'], item['category_title'], \
                item['trackId'])).format(self._tabname)

        self.cursor.execute(sql)
        self.conn.commit()

