#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import random
import time
import requests
import pymongo
import urllib2
from lxml import etree
from datetime import datetime
#import threading
#import Queue
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)

headers = {'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Content-Type': 'text/html; charset=utf-8',
           'Host': 'huayu.baidu.com',
           'Connection': 'Keep-Alive'}

def Soup(url):
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    except Exception as e:
        print e

def Bookinfo(bookurl):
    r = requests.get(bookurl)
    tree = etree.HTML(r.content)
    bookname = tree.xpath("//div[@class='lebg']/h1/a")[0].text
    author = tree.xpath("//div[@class='lebg']/h1/span/a")[0].text
    authstatus = tree.xpath("//div[@class='lebg']/h1/b")[0].text
    starttime = tree.xpath("//span[@class='chaptime']")[1].text
    code = Soup(bookurl)
    booknumber = code.findAll(name='div', attrs={'class': 'booknumber'})
    totalClick = str(booknumber[0]).split('<')[3].split('>')[1].strip()
    wordCount = str(booknumber[0]).split('<')[5].split('>')[1].strip()
    vote = str(booknumber[0]).split('<')[7].split('>')[1].strip()
    integral = str(booknumber[0]).split('<')[9].split('>')[1].strip()
    endtime = str(booknumber[0]).split('<')[11].split('>')[1].strip()

    info_zongheng = {}
    info_zongheng['bookname'] = bookname
    info_zongheng['author'] = author
    info_zongheng['totalClick'] = totalClick
    info_zongheng['updateStatus'] = endtime
    info_zongheng['wordCount'] = wordCount
    #    info_zongheng['description'] = description
    info_zongheng['bookurl'] = bookurl
    info_zongheng['starttime'] = starttime
    info_zongheng['endtime'] = endtime
    info_zongheng['authstatus'] = authstatus
    print '%s write ok!!!' % bookname

def Spider(url):
    try:
        r = requests.get(url, headers=headers)
        tree = etree.HTML(r.content)
        bookurls = tree.xpath("//a[@class='fs14']/@href")
        for bookurl in bookurls:
            Bookinfo(bookurl)
            #print bookurl
    except Exception as e:
        print e

if __name__ == '__main__':
    pool = ThreadPool(10)
    page = []
    for i in range(1, 399):
        url = 'http://book.zongheng.com/store/c0/c0/b1/u1/p%s/v9/s9/t0/ALL.html' % i
        page.append(url)
        print 'Sleep time......'
        time.sleep(5)
    results = pool.map(Spider, page)
    pool.close()
    pool.join()
    print 'all ok!!'
