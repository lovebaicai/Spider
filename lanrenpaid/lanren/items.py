# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LanrenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    AlbumTitle = scrapy.Field()
    NickName = scrapy.Field()
    PlayCounts = scrapy.Field()
    CreateTime = scrapy.Field()
    UpdateTime = scrapy.Field()
    SoundNumbers = scrapy.Field()
    AlbumUrl = scrapy.Field()
    SoundType = scrapy.Field()
