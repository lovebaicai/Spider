#!/usr/bin/env python
#-*- coding:utf-8-*-
import datetime
import logging
import MySQLdb as mdb
from lxml import etree
from gzip import GzipFile
from StringIO import StringIO
import urllib2
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
debug_log = logging.FileHandler(filename='sounddebug.log')
debug_log.setLevel(logging.WARNING)
logging.getLogger('').addHandler(debug_log)

#定义soup解析网页
def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=20)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        pass
#判断link是否存在
def Link_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

#服务器支持gzip/defalte则自动解压缩
class ContentEncodingProcessor(urllib2.BaseHandler):
# add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req

    def http_response(self, req, resp):
        old_resp = resp
# gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile(
            fileobj=StringIO(resp.read()),
            mode="r"
            )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
# deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO( deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp

# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
    try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)

con = mdb.connect('localhost', 'root', 'ubuntu', 'sound', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

try:
    cur.execute("create table albumsound(id int PRIMARY KEY AUTO_INCREMENT, albumtitle varchar(255), music_type VARCHAR (255), "
                "author VARCHAR(255),playcount VARCHAR (255), tag VARCHAR(255), starttime varchar (255), endtime varchar(255), albumurl varchar(255))")
except Exception as e:
    logging.exception(e)

url = 'http://www.ximalaya.com/dq/all/'
pagesource = Soup(url)
sound_tag = pagesource.findAll('a' ,attrs={'class': 'tagBtn'})
host = 'http://www.ximalaya.com'

#获取声音链接
def Spider(var=''):
    for tag in sound_tag:
        urltab = ('%s%s%s') % (host, tag['href'], var)    #urltab是大分类链接
#            print urltab
        numbercode = Soup(urltab)
        pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
        numberlist = [] #获取分类下页面最大数
        for numbers in pagenumber:
            numberlist.append(numbers.string)
        try:
            maxpagenumber = int(numberlist[-2]) + 1
        except Exception as a:
            maxpagenumber = 1
#            print maxpagenumber
#            maxpagenumber = 2
        for i in range(1, maxpagenumber):
            urltab2 = (urltab + '%s') % i
            print '开始抓取%s%s,第%s页数据' % (var, tag.string, i)
            if Link_exists(urltab2) == True:
                code  = Soup(urltab2)
                links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
            for link in links_title:
                args = (link['href'],)
                sql = 'SELECT albumurl FROM albumsound WHERE albumurl = (%s)'
                albumnumber = cur.execute(sql, args)
                if albumnumber == 0:
                    encoding_support = ContentEncodingProcessor
                    opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                    try:
                        html = opener.open(link['href'],timeout=20).read()
                        pagetree = etree.HTML(html)
                        pagenu = pagetree.xpath("//@data-page")        #获取专辑下节目最大页数
                        try:
                            maxpage = pagenu[-2]
                        except Exception as e:
                            maxpage = 1
            #            for link in links_title:
                        aurl = link['href']    #aurl是album链接
                        encoding_support = ContentEncodingProcessor
                        opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                        html = opener.open(aurl).read()
                        tree = etree.HTML(html)
                        albumtitle = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
                        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
                        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
                        tagString = ','.join(i.text for i in tags)
                        updatetime = tree.xpath("//div[@class='detailContent_category']/span")[0].text
                        username = tree.xpath("//div[@class='username']")[0].text
                        username = username.split()[0]
                        try:
                            playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
                        except Exception as b:
                            playcount = 0
                        uploadtimes = tree.xpath("//div[@class='miniPlayer3']/div[@class='operate']/span")
                        try:
                            timelist = [times.text.replace('-', '', 2) for times in uploadtimes]
                            starttime = min(timelist)
                        except Exception as g:
                            starttime = updatetime
                        if maxpage == 1:
                            starttime = starttime
                        else:
                            url2 = link['href'] + '?page=' + str(maxpage)     #aurl是album链接
                            encoding_support = ContentEncodingProcessor
                            opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                            html = opener.open(url2).read()
                            pagetree1 = etree.HTML(html)
                            uploadtimes1 = tree.xpath("//div[@class='miniPlayer3']/div[@class='operate']/span")
                            timelist1 = [times.text.replace('-', '', 2) for times in uploadtimes]
                            starttime1 = min(timelist1)
                            if starttime1 < starttime:
                                starttime = starttime1
            #            print albumtitle, music_type, username, playcount, tagString, starttime, updatetime, aurl
                        try:
                           cur.execute(
                               "insert into albumsound(albumtitle, music_type, author, playcount, tag, starttime, endtime, albumurl)"
                               "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                                % (albumtitle, music_type, username, playcount, tagString, starttime, updatetime, aurl))
                        except Exception as f:
                            logging.exception(f)
                        con.commit()
                        print '爬取%s数据完成' % (link.string)
                    except:
                        pass
                else:
                    print '%s exists' % link.string
            print '%s,第%s页保存完成' % (tag.string, i)
        print '%s%s 保存完成' % (var, tag.string)
    print 'ok!!!!!!!!!!'

if __name__ =='__main__' :
    Spider()
    Spider(var='classic')
    Spider(var='recent')
