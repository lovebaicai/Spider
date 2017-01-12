# -*- coding: utf-8 -*-

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.conf import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LanrenPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="ubuntu", db="xmlyalbumdata", charset="utf8")
        self.curson = self.conn.cursor()
        self.curson.execute("SET NAMES utf8")
        try:
            self.curson.execute("DROP TABLE IF EXISTS lanren")
            sql = """CREATE TABLE lanren (
                 id INT PRIMARY KEY AUTO_INCREMENT,
                 albumtitle VARCHAR(255),
                 soundtype VARCHAR(255),
                 author VARCHAR(255),
                 createtime VARCHAR(255),
                 updatetime VARCHAR(255),
                 playcounts VARCHAR(255),
                 soundnumbers VARCHAR(255),
                 albumurl VARCHAR(255))"""
            self.curson.execute(sql)
        except:
            pass

    def process_item(self, item, spider):
        sql1 = """select * from lanren where albumurl='{}'""".format(item['AlbumUrl'])
        num = self.curson.execute(sql1)
        if num == 0:
            sql = ("insert into lanren (albumtitle, soundtype, author, createtime, updatetime, playcounts, soundnumbers, albumurl) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %  (item['AlbumTitle'], item['SoundType'], item['NickName'], item['CreateTime'], item['UpdateTime'], item['PlayCounts'], item['SoundNumbers'], item['AlbumUrl']))
            self.curson.execute(sql)
            self.conn.commit()
