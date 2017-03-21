# -*- coding: utf-8 -*-

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LanrenPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="ubuntu", db="lanreninfo", charset="utf8")
        self.curson = self.conn.cursor()
        self.curson.execute("SET NAMES utf8")
        time1 = datetime.datetime.now().strftime('%Y%m%d')
        self.tabname = 'lanreninfo_' + time1
        try:
            #self.curson.execute("DROP TABLE IF EXISTS lanrenfree")
            sql = """CREATE TABLE %s (
                 id INT PRIMARY KEY AUTO_INCREMENT,
                 albumtitle VARCHAR(255),
                 soundtype VARCHAR(255),
                 author VARCHAR(255),
                 createtime VARCHAR(255),
                 updatetime VARCHAR(255),
                 playcounts VARCHAR(255),
                 soundnumbers VARCHAR(255),
                 albumurl VARCHAR(255))""" % self.tabname
            self.curson.execute(sql)
        except Exception as f:
            pass

    def process_item(self, item, spider):
        sql1 = """select * from {} where albumurl='{}'""".format(self.tabname, item['AlbumUrl'])
        num = self.curson.execute(sql1)
        if num == 0:
            sql = ("insert into {} (albumtitle, soundtype, author, createtime, updatetime, playcounts, soundnumbers, albumurl) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %  (item['AlbumTitle'], item['SoundType'], item['NickName'], item['CreateTime'], item['UpdateTime'], item['PlayCounts'], item['SoundNumbers'], item['AlbumUrl'])).format(self.tabname)
            self.curson.execute(sql)
            self.conn.commit()
