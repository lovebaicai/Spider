#!/usr/bin/env python
#-*- coding:utf-8-*-
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
        response = urllib2.urlopen(request, timeout=20)
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
    cur.execute("create table allsound(id int PRIMARY KEY AUTO_INCREMENT, title varchar(255), nickname VARCHAR(255),"
           "play_count VARCHAR(255), sound_time VARCHAR (255), album_title VARCHAR (255), category_title VARCHAR (255),"
           " coumments_count varchar(255), favorites_count varchar(255), soundurl varchar(255), albumurl varchar(255))")
except Exception as e:
    pass

url = 'http://www.ximalaya.com/dq/all/'
pagesource = Soup(url)
sound_tag = pagesource.findAll('a' ,attrs={'class': 'tagBtn'})
host = 'http://www.ximalaya.com'


#获取声音链接
def Spider(var):
    for tag in sound_tag:
        urltab = ('%s%s%s') % (host, tag['href'], var)
        numbercode = Soup(urltab)
        pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
        numberlist = [] #获取分类下页面最大数
        for numbers in pagenumber:
            numberlist.append(numbers.string)
        try:
            maxpagenumber = int(numberlist[-2]) + 1
        except Exception as a:
            maxpagenumber = 1
        for i in range(1, maxpagenumber):
            urltab2 = (urltab + '%s') % i
            print '开始抓取%s,第%s页数据' % (tag.string, i)
    #        print urltab2
            if Link_exists(urltab2) == True:
                try:
                    code  = Soup(urltab2)
                    links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
                except:
                    pass
            for link in links_title:
    #            print link['href']
                args = link['href']
                sql1 = 'SELECT albumurl FROM allsound WHERE albumurl = (%s)'
                albumnumber = cur.execute(sql1, args)
                if albumnumber == 0:
                    encoding_support = ContentEncodingProcessor
                    opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                    try:
                        html = opener.open(link['href'], timeout=20).read()
                    except:
                        pass
                    pagetree = etree.HTML(html)
                    pagenu = pagetree.xpath("//@data-page")        #获取专辑下节目最大页数
                    try:
                        maxpage = pagenu[-2]
                    except Exception as e:
                        logging.exception(e)
                        maxpage = 1
        #            for link in links_title:
                    for p in range(1, int(maxpage)+1):
                        aurl = link['href'] + '?page=' + str(p)     #aurl是album链接
        #                print aurl

                        print '开始爬取%s,第%s页数据' % (link.string, p)
                        encoding_support = ContentEncodingProcessor
                        opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                        # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                        try:
                            html = opener.open(aurl).read()
                        except:
                            pass
                        ttree = etree.HTML(html)
                        sound_id = ttree.xpath("//@sound_ids")       #获取节目id
                        urlid = sound_id[0].split(",")
                        for id in urlid:
                            if id != '':
                                jsonurl = 'http://www.ximalaya.com/tracks/%s.json' %  id
                            #转成json格式,使用xpath获取关键字
                            try:
                                jsonrequest = urllib2.Request(jsonurl)
                                jsonresponse = urllib2.urlopen(jsonrequest,timeout=20)
                                jsonpagecode = jsonresponse.read()
                                jsonpage = json.loads(jsonpagecode)
                                try:
                                    title = jsonpage['title'].encode("utf-8").decode("utf-8")
                                except Exception as e:
                                    title = ' '
                                nickname = jsonpage['nickname'].encode("utf-8").decode("utf-8")
                                try:
                                    play_count = jsonpage['play_count']
                                except Exception as a:
                                    play_count = 0
                                try:
                                    sound_time = jsonpage['duration']
                                except:
                                    sound_time = 0
                                try:
                                    album_title = jsonpage['album_title'].encode("utf-8").decode("utf-8")
                                    category_title = jsonpage['category_title'].encode("utf-8").decode("utf-8")
                                except:
                                    pass
                                try:
                                    duration = jsonpage['duration']
                                except:
                                    duration = 0
                                try:
                                    coumments_count = jsonpage['comments_count']
                                except Exception as b:
                                    coumments_count = 0
                                try:
                                    favorites_count = jsonpage['favorites_count']
                                except Exception as c:
                                    favorites_count = 0
                                try:
                                    soundurl = 'http://www.ximalaya.com/%s/sound/%s' % (jsonpage['uid'], jsonpage['id'])
                                    albumurl = 'http://www.ximalaya.com/%s/album/%s' % (
                                    jsonpage['uid'], jsonpage['album_id'])
                                except:
                                    pass
                                    #                   print title, nickname, play_count, coumments_count, favorites_count, album_title, soundurl, albumurl
                                # 查询db里面是否存在soundurl,存在就pass,soundurl是唯一的
                                args = soundurl
                                sql = 'SELECT soundurl FROM allsound WHERE soundurl = (%s)'
                                soundnumber = cur.execute(sql, args)
                                if soundnumber == 0:
                                    try:
                                        # 写入sql
                                        cur.execute(
                                            "insert into allsound(title, nickname, play_count, sound_time, album_title, category_title, coumments_count, favorites_count, soundurl,albumurl)"
                                            " values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                                            % (title, nickname, play_count, sound_time, album_title, category_title,
                                               coumments_count, favorites_count, soundurl, albumurl))
                                    except Exception as f:
                                        logging.exception(f)
                                else:
                                    print '%s exists' % title
                                    pass
                                con.commit()
                            except:
                                pass
                        print '爬取%s,第%s页数据完成' % (link.string, p)
                else:
                    print '%s exists' % link.string
            print '%s%s第%s保存完成' %(var, tag.string, i)
        print '%s%s 保存完成'  % (var, tag.string)

if __name__ =='__main__' :
    Spider(var='')
    Spider(var='classic')
    Spider(var='recent')
    cur.close()
    con.commit()
    con.close()
    print 'all ok!!'
