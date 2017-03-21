#!/usr/bin/env python
#-*-coding:utf-8-*-

import json
import scrapy
import logging
import requests
from lxml import etree
from ..items import LanrenItem
from bs4 import BeautifulSoup

def pageinfo(albumurl):
    info = {}
    pagecode = requests.get(albumurl)

    soup = BeautifulSoup(pagecode.content, 'lxml')
    sound_title = soup.findAll('h1', attrs={'class': 'nowrap'})
    o = []
    for i in sound_title:
        for x in i.strings:
            o.append(x)
    AlbumTitle = "".join(o[0])

    authors = soup.findAll('a', attrs={'class': 'g-user'})
    author = []
    for au in authors:
        #print author.string
        author.append(au.string)
    NickName = author[0]

    soundtypes = soup.findAll('ul', attrs={'class': 'd-grid'})
    SoundNumbers = str(soundtypes[2]).split('>')[4].split('<')[0]
    SoundType = str(soundtypes[1]).split('>')[4].split('<')[0]
    UpdateTime = str(soundtypes[2]).split('>')[16].split('<')[0].replace('-', '')

    try:
        playcountss = soup.findAll('a', attrs={'class': 'd-p player-trigger pay-section'})
        PlayCounts = str(playcountss).split('>')[3].replace(' ', '').replace('\\t', '').replace('\\n', '').replace('\\u', '').split('<')[0].replace('4e07', '万')
    except:
        playcountss = soup.findAll('a', attrs={'class': 'd-p player-trigger '})
        PlayCounts = str(playcountss).split('>')[3].replace(' ', '').replace('\\t', '').replace('\\n', '').replace('\\u', '').split('<')[0].replace('4e07', '万').replace('4ebf', '亿')

    info['AlbumTitle'] = AlbumTitle
    info['NickName'] = NickName
    info['SoundType'] = SoundType
    info['SoundNumbers'] = SoundNumbers
    info['UpdateTime'] = UpdateTime
    info['PlayCounts'] = PlayCounts
    return info

class LanrenSpider(scrapy.Spider):
    name = 'lrfree'

    headers = {'User-Agent': 'ting_5.4.39(Samsung+Galaxy+S6+-+5.0.0+-+API+21+-+1440x2560,Android21'}

    cate_id = [1, 78, 4, 3, 6, 7, 80, 3085, 55, 3086, 1019, 79]
    urls = [('http://www.lrts.me/book/category/{}').format(i) for i in cate_id]
    pagenumber = []
    for url in urls:
        pagecode = requests.get(url, headers=headers)
        maxpage = etree.HTML(pagecode.content).xpath('//div[@class="pagination"]/a/text()')[-2]
        pagenumber.append(maxpage)
    start = []
    i = 0
    for id in cate_id:
        if i <= len(pagenumber):
            for page in range(1, int(pagenumber[i])):
                url = 'http://www.lrts.me/book/category/{}/recommend/{}/20'.format(id, page)
                start.append(url)
        i += 1

    start_urls = start

    def parse(self, response):
        item = LanrenItem()
        tree = etree.HTML(response.body)
        albumid = [albumurl for albumurl in tree.xpath("//div[@class='book-item-r']/a/@href")]
        for id in albumid:
            try:
                albumurl = 'http://www.lrts.me{}'.format(id)
                CreateTime = (etree.HTML((requests.get(albumurl)).content)).xpath("//time")[0].text.split(':')[1].replace('-', '')
                item['AlbumUrl'] = albumurl
                code = pageinfo(albumurl)
                item['NickName'] = code['NickName']
                item['PlayCounts'] = code['PlayCounts']
                UpdateTime = code['UpdateTime']
                item['UpdateTime'] = max(CreateTime, UpdateTime)
                item['CreateTime'] = min(CreateTime, UpdateTime)
                item['SoundNumbers'] = code['SoundNumbers']
                item['AlbumTitle'] = code['AlbumTitle']
                item['SoundType'] = code['SoundType']
                yield item

            except Exception as e:
                logging.exception(e)

'''
            #yield scrapy.Request(url=jsonurl, meta={'item': item}, callback=self.parse_album, dont_filter=True)

    def parse_album(scrapy, response):
        item = response.meta['item']
        pagecode = json.loads(response.body)
        item['NickName'] = pagecode['announcer']
        item['PlayCounts'] = pagecode['play']
        item['UpdateTime'] = pagecode['update']
        item['SoundNumbers'] = pagecode['sections']
        item['AlbumTitle'] = pagecode['name']
        item['SoundType'] = pagecode['type']
        yield item
'''
