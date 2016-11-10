#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import random
import time
import requests
import pymongo
from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)

conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = conn.zongheng
collection = db.newbook

def Soup(url):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    except Exception as e:
        print e
        pass


headers = {'Accept-Language': 'zh-CN',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Content-Type': 'text/html; charset=utf-8',
           'Host': 'book.zongheng.com',
           'Connection': 'Keep-Alive'}

#获取开始时间和最后更新时间
def Booktime(readurl):
    timess = []
    try:
        code = Soup(readurl)
        times = code.findAll(name='td', attrs={'class': 'chapterBean'})
        timelist = [time['updatetime'] for time in times]
        starttime =  int(min(timelist))/1000
        starttime1 = datetime.fromtimestamp(starttime).strftime('%Y-%m-%d')
        endtime = int(max(timelist))/1000
        endtime1 = datetime.fromtimestamp(endtime).strftime('%Y-%m-%d')
        timess.append(starttime1)
        timess.append(endtime1)
    except Exception as e:
        print e
        pass
    return timess

#获取bookinfo,插入MongoDB
def Bookinfo(bookurl):
    exist = db.newbook.count({'bookurl':bookurl})
    if exist < 1:
        r = requests.get(bookurl, headers=headers, timeout=20)
        tree = etree.HTML(r.content)
        try:
            bookname = tree.xpath("//div[@class='status fl']/h1/a")[0].text
            try:
                authstatus = tree.xpath("//div[@class='status fl']/h1/em[@class='sign']/@title")[0]
            except:
                authstatus = None
            author = tree.xpath("//div[@class='status fl']/div[@class='booksub']/a")[0].text
            genre = tree.xpath("//div[@class='status fl']/div[@class='booksub']/a")[1].text
            wordcount = tree.xpath("//div[@class='status fl']/div[@class='booksub']/span")[0].text
            #description = tree.xpath("//div[@class='status fl']/div[@class='info_con']/p")[0].text.strip()
            readurl = tree.xpath("//span[@class='btn_as list']/a/@href")[0]
            starttime = Booktime(readurl)[1]
            endtime = Booktime(readurl)[0]

            code = Soup(bookurl)
            monthly = code.findAll(name='p', attrs={'class': 'fb'})
            monthlyRecommend = str(monthly[0]).split('>')[3].split('<')[0]
            monthlyClick = str(monthly[1]).split('>')[3].split('<')[0]

            numbers = code.findAll(name='p')[10:15]
            totalClick = str(numbers[0]).split('>')[3].split('<')[0]
            totalCollection = str(numbers[1]).split('>')[3].split('<')[0]
            totalRecommend = str(numbers[2]).split('>')[3].split('<')[0]
            commentnumbers = str(numbers[3]).split('>')[3].split('<')[0]
            try:
                supportnumbers = str(numbers[4]).split('>')[3].split('<')[0]
            except:
                supportnumbers = 0
            info_zongheng = {}
            info_zongheng['bookname'] = bookname
            info_zongheng['author'] = author
            info_zongheng['totalClick'] = totalClick
            info_zongheng['totalRecommed'] = totalRecommend
            info_zongheng['monthClick'] = monthlyClick
            info_zongheng['monthlyRecommend'] = monthlyRecommend
            info_zongheng['updateStatus'] = endtime
            info_zongheng['wordCount'] = wordcount
            info_zongheng['bookurl'] = bookurl
            info_zongheng['genre'] = genre
            info_zongheng['starttime'] = starttime
            info_zongheng['authstatus'] = authstatus
            info_zongheng['commentnumbers'] = commentnumbers
            info_zongheng['totalCollection'] = totalCollection
            info_zongheng['supportnumbers'] = supportnumbers

            collection.insert(info_zongheng)
            print 'Sleep time......'
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
        r = requests.get(url, headers=headers, timeout=20)
        tree = etree.HTML(r.content)
        bookurls = tree.xpath("//a[@class='fs14']/@href")
        for bookurl in bookurls:
            Bookinfo(bookurl)
    except Exception as e:
        print e
        pass

if __name__ == '__main__':
    pool = ThreadPool(3)
    page = []
    for i in range(1, 1000):
        url = 'http://book.zongheng.com/store/c0/c0/b0/u1/p%s/v9/s9/t0/ALL.html' % i
        page.append(url)
    results = pool.map(Spider, page)
    pool.close()
    pool.join()
    print 'all ok!!'
