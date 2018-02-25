# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import os
import codecs
import json

class HotitemsPipeline(object):
    def __init__(self):
        self.time_now = datetime.datetime.now()
        self.outdata_dir = os.path.join('out', self.time_now.strftime("%Y%m%d")) 
        try:
            if not os.path.exists(self.outdata_dir):
                os.makedirs(self.outdata_dir)
        except:
            pass

    def open_spider(self, spider):
        self.file = codecs.open(("{}/{}.json").format(self.outdata_dir, spider.name), 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        oitem = {}
        for (k,v) in item.iteritems():
            ov = v
            if isinstance(v, unicode):
                ov = v.encode("utf-8")
            if isinstance(k, unicode):
                oitem[k.encode("utf-8")] = ov
            else:
                oitem[k] = ov
        line = json.dumps(oitem, ensure_ascii=False)
        self.file.write(line.decode("utf-8")) 
        self.file.write("\n")
        return item
