#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import random
import time
import requests
import pymongo
import urllib2
from lxml import etree
import threading
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)

conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = conn.cmfu
collection = db.book

headers = {'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Content-Type': 'text/html; charset=utf-8',
           'Host': 'a.qidian.com',
           'Connection': 'Keep-Alive'}

#解析url
def Soup(url):
    try:
       # r = requests.get(url, headers=headers)
       # soup = BeautifulSoup(r.content, 'lxml')
       request = urllib2.Request(url)
       response = urllib2.urlopen(request, timeout=20, headers=headers)
       pagecode = response.read()
       soup = BeautifulSoup(pagecode, 'lxml')
       return soup
    except urllib2.URLError, e:
        print e
        pass

#获取starttime
def BookReader(bookurl):
    code = Soup(bookurl)
    books1 = code.findAll(name='a', attrs={'stat-type': 'read'})
    global readurl
    for readurl in books1:
        readurl = readurl['href']
        try:
            request = urllib2.Request(bookurl)
            response = urllib2.urlopen(request, timeout=20, headers=headers).read()
            #response = requests.get(readurl, headers=headers)
            #html = response.content
            tree = etree.HTML(response)
            starttime = tree.xpath("//a[@itemprop='url']/@title")[0].split(' ')[2]
        except Exception as e:
            print e
            pass
        return starttime

#获取bookinfo,插入MongoDb
def Bookinfo(bookurl):
    exist = db.book.count({'bookurl': bookurl})
    if exist < 1:
        try:
            #print bookurl
            request = urllib2.Request(bookurl)
            response = urllib2.urlopen(request, timeout=20, headers=headers).read()
            #response = requests.get(bookurl, headers=headers)
            #html = response.content
            tree = etree.HTML(response)
            starttime = BookReader(bookurl)
            totalClick = tree.xpath("//span[@itemprop='totalClick']")[0].text
            monthClick = tree.xpath("//span[@itemprop='monthlyClick']")[0].text
            weeklyClick = tree.xpath("//span[@itemprop='weeklyClick']")[0].text
            totalRecommend = tree.xpath("//span[@itemprop='totalRecommend']")[0].text
            monthlyRecommend = tree.xpath("//span[@itemprop='monthlyRecommend']")[0].text
            weeklyRecommend = tree.xpath("//span[@itemprop='weeklyRecommend']")[0].text
            wordCount = tree.xpath("//span[@itemprop='wordCount']")[0].text
            author = tree.xpath("//span[@itemprop='name']")[0].text.strip()
            bookname = tree.xpath("//div[@class='title']/h1[@itemprop='name']")[0].text.strip()
            genre = tree.xpath("//span[@itemprop='genre']")[0].text
            updateStatus = tree.xpath("//span[@itemprop='updataStatus']")[0].text
            dateModified = tree.xpath("//span[@itemprop='dateModified']")[0].text
            description = tree.xpath("//span[@itemprop='description']")[0].text.strip()
            authstatus = tree.xpath("//strong")[1].text.strip()
            score = tree.xpath("//b[@id='bzhjshu']")[0].text

            info_cmfu = {}
            info_cmfu['booname'] = bookname
            info_cmfu['author'] = author
            info_cmfu['totalClick'] = totalClick
            info_cmfu['totalRecommed'] = totalRecommend
            info_cmfu['monthClick'] = monthClick
            info_cmfu['monthlyRecommend'] = monthlyRecommend
            info_cmfu['weeklyClick'] = weeklyClick
            info_cmfu['weeklyRecommend'] = weeklyRecommend
            info_cmfu['updateStatus'] = updateStatus
            info_cmfu['wordCount'] = wordCount
            info_cmfu['score'] = score
            info_cmfu['description'] = description
            info_cmfu['bookurl'] = bookurl
            info_cmfu['genre'] = genre
            info_cmfu['dateModified'] = dateModified
            info_cmfu['starttime'] = starttime

            collection.insert(info_cmfu)
            print 'Sleep time....'
            time.sleep(5)
            print '%s write ok!!!' % bookname
        except Exception as e:
            print e
            pass
    else:
        print '%s exists' % bookurl


#获取bookurl
def Spider(url):
    try:
        code = Soup(url)
        books = code.findAll(name='a', attrs={'class': 'name'})
        for book in books:
            if book['href'] != 'javascript:':
                bookurl = book['href']
                Bookinfo(bookurl)
    except Exception as e:
        print e
        pass

if __name__ == '__main__':
    pool = ThreadPool(5)
    page = []
    for i in range(1, 8874):
        url = ('http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=2&page=' +
              str(i) + '&month=-1&style=2&action=-1&vip=-1')
        page.append(url)
    results = pool.map(Spider, page)
    pool.close()
    pool.join()
    print 'all ok!!'
