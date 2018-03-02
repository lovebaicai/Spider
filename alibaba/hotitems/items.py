#-*- coding:utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import datetime
from scrapy import Item, Field

class HotItem(Item):
    title = Field() # 商品名称
    sku_url = Field() # 商品url
    img_url = Field() # 商品图片url
    company_name = Field() # 店铺名称
    company_url = Field() #店铺url
    price = Field() #价格
    month_gmv = Field() # 30天销售额
    membership_years = Field() # 诚信会员年数
