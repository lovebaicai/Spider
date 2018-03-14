# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .sql import Sql
from inscrawl.items import InscrawlItem

class InscrawlPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,InscrawlItem):
           pic_id = item['pic_id']
           ret = Sql.select_id(pic_id)
           if ret[0] != 1:
               pic_id = item['pic_id']
               pic_title = item['pic_title']
               pic_comment = item['pic_comment']
               pic_like_count = item['pic_like_count']
               pic_url = item['pic_url']
               pic_timestamp = item['pic_timestamp']
               try:
                  Sql.insert_ins_data(pic_id,pic_title,pic_comment,pic_like_count, pic_url, pic_timestamp)
               except:
                   pic_title = '' # title 会用表情之类的特殊符号，直接过滤, 无法存入sqlite3
                   Sql.insert_ins_data(pic_id,pic_title,pic_comment,pic_like_count, pic_url, pic_timestamp)
               print('start insert {} to db'.format(pic_id))
               return item
