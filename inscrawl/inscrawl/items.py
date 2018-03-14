# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    pic_id = scrapy.Field()
    pic_title = scrapy.Field()
    pic_comment = scrapy.Field()
    pic_timestamp = scrapy.Field()
    pic_like_count = scrapy.Field()
    pic_url = scrapy.Field()
