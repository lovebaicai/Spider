# -*- coding: utf-8 -*-
import scrapy
import logging
import re

class AliSpider(scrapy.Spider):
    name = "aliexp"
    custom_settings = {
        "DOWNLOAD_DELAY": 4
    }

    def start_requests(self):
        for url in self.info:
            keyword = '' # customize
            new_url = 'https://www.aliexpress.com/wholesale?SearchText={}&page=1'.format(keyword)
            yield scrapy.Request(new_url, meta={'page': 1}, callback=self.parse)

    def parse(self, response):
        items_node = response.xpath('//*[@id="hs-list-items"]/ul/li')
        if len(items_node) > 0:
            for item_node in items_node:
                item = {}
                nid = item_node.xpath('./@qrdata').extract_first().split('|')[1]
                if not nid:
                    continue
                url = item_node.xpath('.//div//a/@href').extract_first().split('?')[0].lstrip('//')
                title = item_node.xpath('.//div//a/img/@alt').extract_first()
                pic_url = item_node.xpath('.//div//a/img/@image-src').extract_first()
                if not pic_url:
                    pic_url = item_node.xpath('.//div//a/img/@src').extract_first()
                price = items_node.xpath('.//div[2]/span/span[1]/text()').extract_first()
                if not price:
                    price = items_node.xpath('.//div[3]/span/span[1]/text()').extract_first()
                comments_count = items_node.xpath('.//div[2]/div/a/text()').extract_first().strip('()')
                if not comments_count:
                    comments_count = 0
                orders = items_node.xpath('.//div[2]//span[3]/a/em/text()').extract_first()
                if not orders:
                    orders = 0
                else:
                    orders = re.search('\d+', orders).group()
                item['pic_url'] = "http:%s" % pic_url
                item['nid'] = nid
                item['url'] = url
                item['title'] = title
                item['price'] = price
                item['comments_count'] = comments_count
                item['orders'] = orders
                yield item


                error_f = list(filter(lambda d: d[1] == "", item.items()))
                if len(error_f) > 0:
                    raise Exception("error:%s is NULL,url:%s" % (error_f[0][0], response.url))
            page = response.meta['page']
            if page < 6:
                new_url = response.url.replace("page=%s" % str(page), "page=%s" % str(page+1))
                response.meta["page"] += 1
                yield scrapy.Request(new_url, meta=response.meta, callback=self.parse)
