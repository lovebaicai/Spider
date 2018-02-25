# -*- coding: utf-8 -*-

import sys
import scrapy
import re
import json
import urllib
import datetime
import requests


class TaobaoSpider(scrapy.Spider):

    name = "alibaba"

    start_urls = ['https://www.1688.com/']
    proxies = {'http': 'http://host:port'}
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
               'Accept-Encoding':'gzip, deflate, br',
               'Connection':'close'}

    def parse(self, response):
        items_node = response.xpath('//*[@id="hp_first_screen_left_2015"]/ul/li')
        for item in items_node:
            for url in item.xpath('a/@href').extract():
                if not re.search('http*', url):
                    url = 'https:' + url
                yield scrapy.Request(url, callback=self.category_detail)
    
    def category_detail(self, response):
        if re.search('nvzhuang*', response.url):
            items = response.xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div[4]/div/div[1]/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk')) + '%C5%AE'
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('nanzhuang*', response.url):
            items = response.xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div[1]/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk')) + '%C4%D0'
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('neiyi*', response.url) or re.search('peijian*', response.url) \
                or re.search('home*', response.url) or re.search('food*', response.url) \
                or re.search('mei*', response.url) or re.search('jiadian*', response.url):
            items = response.xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('xie*', response.url) or re.search('sport*', response.url) or re.search('enjoy*', response.url):
            items = response.xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('xiangbao*', response.url) or re.search('auto*', response.url) \
                or re.search('jia*', response.url):
            items = response.xpath('/html/body/div[1]/div[4]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('muying*', response.url) or re.search('bz\.*', response.url) \
                or re.search('smart*', response.url) or re.search('view*', response.url):
            items = response.xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div[1]/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('3c*', response.url):
            items = response.xpath('/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('ee*', response.url) or re.search('light*', response.url):
            items = response.xpath('/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]'
                                   '/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('af*', response.url) or re.search('ec*', response.url) \
                or re.search('jd*', response.url) or re.search('wjgj*', response.url) \
                or re.search('yqyb*', response.url) or re.search('plas*', response.url) \
                or re.search('chem*', response.url) or re.search('steel*', response.url):
            items = response.xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/ul/li')
            for item in items:
                keyword = item.xpath('a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)
        elif re.search('fangzhi*', response.url): 
            items = response.xpath('//*[@id="crazy-box-banner"]/div/div[2]/div/div/div/div/div[2]/div/dl')
            for item in items:
                keyword = item.xpath('dd/a/text()').extract_first().encode('utf-8')
                keyword = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
                yield scrapy.Request(response.url, meta={'keyword': keyword}, callback=self.detail_parse, dont_filter=True)


    def detail_parse(self, response):
        url = ('https://match.p4p.1688.com/b2bad?keyword={}&callback=jQuery18309996473081016044_1510628438193&catid='
                '&dcatid=1031910&pid=819002_1008&outfmt=json&count=500').format(response.meta['keyword'])
        page = requests.get(url, proxies=self.proxies, headers=self.headers).text
        infos = json.loads(re.search('jQuery18309996473081016044_1510628438193(\(.+\))', page).group(1)[1:-1])['resultset']['docset']
        for info in infos:
            product_nid = info['resourceid']
            title = info['creative_title']
            sku_url = info['clickurl']
            img_url = info['offerimgurl']
            company_name = info['company']
            if not re.search('b2b-*', info['memberid']):
                company_url = 'https://{}.1688.com/'.format(info['memberid'])
            else:
                company_url = 'https://m.1688.com/winport/{}.html'.format(info['memberid'])
            price = info['price']
            month_gmv = info['quantity_sum_month']

            item = {}
            item['product_nid'] = product_nid
            item['title'] = title
            item['sku_url'] = sku_url
            item['img_url'] = img_url
            item['company_name'] = company_name
            item['company_url'] = company_url
            item['price'] = price
            item['month_gmv'] = month_gmv
            yield item
