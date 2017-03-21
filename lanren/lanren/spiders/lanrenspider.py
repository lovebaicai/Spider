#!/usr/bin/env python
#-*-coding:utf-8-*-

import json
import scrapy
import logging
import requests
from lxml import etree
from ..items import LanrenItem
from bs4 import BeautifulSoup

debug_log = logging.FileHandler(filename='lanrendebug.log')
debug_log.setLevel(logging.WARNING)
logging.getLogger('').addHandler(debug_log)
#from scrapy.downloadmiddlewares.useragent import UserAgentMiddleware

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
    name = 'lrpaid'
#    start_urls = ['http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2230234%22%2C%2228194%22%2C%2230425%22%2C%2229307%22%2C%2231545%22%2C%226130%22%2C%2227592%22%2C%2229085%22%2C%2229315%22%2C%2231681%22%2C%2231549%22%2C%2218253%22%2C%2231563%22%2C%2227208%22%2C%2228278%22%2C%2229949%22%2C%2229390%22%2C%2231280%22%2C%224958%22%2C%2231534%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3627&sc=2f355e35401f050520d3597973c69e2d&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3626&returnIds=1&sc=1e769f8033e6c7da9deac8cdcf36db93&size=20&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1&typeId=0',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2230234%22%2C%2228194%22%2C%2230425%22%2C%2229307%22%2C%2231545%22%2C%226130%22%2C%2227592%22%2C%2229085%22%2C%2229315%22%2C%2231681%22%2C%2231549%22%2C%2218253%22%2C%2231563%22%2C%2227208%22%2C%2228278%22%2C%2229949%22%2C%2229390%22%2C%2231280%22%2C%224958%22%2C%2231534%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3627&sc=2f355e35401f050520d3597973c69e2d&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2229386%22%2C%225559%22%2C%2230481%22%2C%2231519%22%2C%2228389%22%2C%2228380%22%2C%224034%22%2C%2231567%22%2C%2231524%22%2C%2229326%22%2C%2229681%22%2C%2231550%22%2C%2231568%22%2C%2231472%22%2C%2229376%22%2C%2228365%22%2C%2230978%22%2C%2229339%22%2C%2230882%22%2C%2227228%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3628&sc=842ddd3c6cdccea5db506aee1b0d1c7d&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2231552%22%2C%2229247%22%2C%2229389%22%2C%2231565%22%2C%2229343%22%2C%226608%22%2C%226477%22%2C%2231679%22%2C%221370%22%2C%2231533%22%2C%2227952%22%2C%2231602%22%2C%2231554%22%2C%2231583%22%2C%2231525%22%2C%2231637%22%2C%2231597%22%2C%2231587%22%2C%2231541%22%2C%2231258%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3629&sc=353b7c11191db18670bc56b7d7723986&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2231527%22%2C%2231570%22%2C%2231635%22%2C%2231668%22%2C%2231538%22%2C%2231666%22%2C%2231537%22%2C%2231547%22%2C%2231580%22%2C%2231578%22%2C%2231571%22%2C%2231531%22%2C%2231535%22%2C%2231574%22%2C%2231529%22%2C%2231557%22%2C%2231626%22%2C%2231633%22%2C%2231630%22%2C%2231539%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3630&sc=e4f2d402dab2a162acc807a3091c4b33&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2231474%22%2C%2231518%22%2C%2231628%22%2C%2231581%22%2C%2231641%22%2C%2231543%22%2C%2231594%22%2C%2231540%22%2C%2231542%22%2C%2231484%22%2C%2231478%22%2C%2231658%22%2C%2231588%22%2C%2231551%22%2C%2231603%22%2C%2231598%22%2C%2231589%22%2C%2231573%22%2C%2231560%22%2C%226479%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3631&sc=345cf7e17e46ae864c6f0b44d6cfb406&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2218311%22%2C%2218304%22%2C%2229374%22%2C%2229316%22%2C%2229822%22%2C%2229375%22%2C%222722%22%2C%2231740%22%2C%2228366%22%2C%2230523%22%2C%2230521%22%2C%2230444%22%2C%2228072%22%2C%223492%22%2C%2229587%22%2C%2231964%22%2C%2227986%22%2C%2230044%22%2C%2228227%22%2C%2227936%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3632&sc=e13f3dd02de1e6afa646f076595306db&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2228714%22%2C%2230241%22%2C%225861%22%2C%2227250%22%2C%226504%22%2C%2228193%22%2C%225844%22%2C%225866%22%2C%2228707%22%2C%2228708%22%2C%2228747%22%2C%2228399%22%2C%2228704%22%2C%2228712%22%2C%2230209%22%2C%2228387%22%2C%2228485%22%2C%2229842%22%2C%2222162%22%2C%2222077%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3633&sc=1ea6573b51e3a096b10a3edcb0ee5055&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%2228186%22%2C%2231714%22%2C%2231724%22%2C%2230206%22%2C%2231780%22%2C%2227861%22%2C%2223399%22%2C%2223623%22%2C%2223627%22%2C%2229870%22%2C%2228189%22%2C%2222147%22%2C%2222112%22%2C%2231336%22%2C%2231793%22%2C%2231627%22%2C%2231532%22%2C%2231522%22%2C%2228784%22%2C%2231887%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3634&sc=e605a7a1981c4d366b7e84646a380ca7&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1',
#                   'http://43.243.130.55/yyting/bookclient/bookRecommendList.action?ids=%5B%221761%22%5D&imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&q=3635&sc=8d745645f4ca9e248937672ca02626ef&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*&type=1']

    headers = {'User-Agent': 'Android5.0/yyting/unknown/Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560/ch_wandoujia/138/AndroidHD'}
    start_urls = [
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3729&s=20&sc=f98444f40403348abf96bc16dd814974&sort=2&tId=5175&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3731&s=20&sc=9ab0d07190a75355041751a4b16cb1a2&sort=2&tId=5243&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3733&s=20&sc=ac9b215bc1c71d22ea6a557bfe40844c&sort=2&tId=5245&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3737&s=20&sc=c956a561e9da4a37c3d424c30b4e5ec2&sort=2&tId=5184&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3739&s=20&sc=b3600c8106ca7e16c0883e392d8607d5&sort=2&tId=5244&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3741&s=20&sc=b1e5ee10b34b2572483fdb711bdb1bd9&sort=2&tId=5242&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*'
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3743&s=20&sc=b63b64c8f0de92f2f4830aee78ea9cce&sort=2&tId=5214&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3745&s=20&sc=a357602b733734f91af30e1ba545f9df&sort=2&tId=5185&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*', 
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3747&s=20&sc=7bd18aa0a5fb835d75665958d6a4178f&sort=2&tId=5176&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3749&s=20&sc=82c121eff5a08c783b6da978d404ae87&sort=2&tId=5246&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3751&s=20&sc=6fe0404295df3b679df8cd27374a873a&sort=2&tId=5177&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3753&s=20&sc=ee3ba6c3f434ca583b8e2f7e2e87dc74&sort=2&tId=5178&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3755&s=20&sc=a827ce632c9f200bfccb2275f40d4b75&sort=2&tId=5180&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*',
            'http://43.243.130.55/yyting/tradeclient/chargeTypeBookList.action?imei=MDAwMDAwMDAwMDAwMDAw&nwt=1&p=1&q=3757&s=20&sc=1ba00237dd5fb524f865e133cebf82f7&sort=2&tId=5212&token=-kPx1dJy6AaQ64xAZevz0-Br5a2z63QiIXd55tBxgoE*']


    def parse(self, response):
        item = LanrenItem()
        page = (json.loads(response.body))['ids']
        for id in page:
            try:
                albumurl = 'http://www.lrts.me/book/{}'.format(id)
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
