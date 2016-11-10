#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import pymongo
import urllib2
from lxml import etree
import threading
import Queue
import MySQLdb as mdb
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys
import time
reload(sys)


q = Queue.Queue()
thread_num = 20

conn   = pymongo.MongoClient(host='127.0.0.1',port=27017)
db = conn.cmfu
collection = db.cmfu

headers = {'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Content-Type': 'text/html; charset=utf-8',
           'Host': 'a.qidian.com',
           'Connection': 'Keep-Alive'}

def Soup(url):
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request, timeout=20)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        print e

#获取starttime
def BookReader(bookurl):
    bookurl = 'http://www.qdmm.com/MMWeb/1004049656.aspx'
    # def BookReader(bookurl):
    try:
        html = urllib2.urlopen(bookurl).read()
        tree = etree.HTML(html)
        readurl = tree.xpath("//a[@itemprop='url']/@href")[0]
        readurl = 'http://www.qdmm.com' + readurl
        html = urllib2.urlopen(readurl, timeout=20, headers=headers).read()
        tree = etree.HTML(html)
        starttime = tree.xpath("//a[@itemprop='url']/@title")[0].split(' ')[2]
    except Exception as e:
        print e
        pass
    return starttime

#获取bookinfo,插入MongoDb
def Bookinfo(bookurl):
    exist = db.book.count({'bookurl':bookurl})
    if exist < 1:
        try:
            resopnse = urllib2.Request(bookurl, headers=headers)
            html = urllib2.urlopen(resopnse, timeout=20).read()
            tree = etree.HTML(html)
            starttime = BookReader(bookurl)
#            trialStatus = tree.xpath("//span[@itemprop='trialStatus']")[0].text
            totalClick = tree.xpath("//span[@itemprop='totalClick']")[0].text
            monthClick = tree.xpath("//span[@itemprop='monthlyClick']")[0].text
            weeklyClick = tree.xpath("//span[@itemprop='weeklyClick']")[0].text
            totalRecommend = tree.xpath("//span[@itemprop='totalRecommend']")[0].text
            monthlyRecommend = tree.xpath("//span[@itemprop='monthlyRecommend']")[0].text
            weeklyRecommend = tree.xpath("//span[@itemprop='weeklyRecommend']")[0].text
            wordCount = tree.xpath("//span[@itemprop='wordCount']")[0].text
            author = tree.xpath("//span[@itemprop='name']")[0].text.strip()
            bookname = tree.xpath("//strong[@itemprop='name']")[0].text.strip()
            genre = tree.xpath("//span[@itemprop='genre']")[0].text.strip()
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
        except Exception as e:
            print e
            pass
        print '%s write ok!!!' % bookname
        time.sleep(5)
        print 'Sleep time...'
    else:
        print '%s exist...' % bookurl

#获取bookurl
def Spider(url):
    try:
        html = urllib2.urlopen(url).read()
        tree = etree.HTML(html)
        bookname = tree.xpath("//span[@class='swbt']/a/@href")
        for bookurl in bookname:
            #print bookurl
            Bookinfo(bookurl)
    except Exception as e:
        print e
        pass

if __name__ == '__main__':
    pool = ThreadPool(3)
    page = []
    for i in range(1, 1967):
        url = ('http://all.qdmm.com/MMWeb/BookStore.aspx?ChannelId=41&SubCategoryId=-1&Tag=all&Size=-1&Action=-1&OrderId=13&P=all&PageIndex=' +
              str(i) + '&update=-1&Vip=-1')
        page.append(url)
    results = pool.map(Spider, page)
    pool.close()
    pool.join()
    print 'all ok!!'