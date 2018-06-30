#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: nemo_chen
# taotu download

import os
import time
import re
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Referer': 'https://www.meitulu.com/item/8767.html'
}

start_url = 'https://www.meitulu.com/t/1111/'
html = requests.get(start_url)
source = etree.HTML(html.text)

def down_pic(dirname, pagenum, pic_nid):
    for i in range(1, int(pagenum)+1):
        url = 'https://mtl.ttsqgs.com/images/img/{}/{}.jpg'.format(pic_nid, i)
        ir = requests.get(url, headers=headers)
        if ir.status_code == 200:
            name = '{}.jpg'.format(i)
            open(name, 'wb').write(ir.content)
            print('{} save ok'.format(name))
            time.sleep(3)
        else:
            print(ir.status_code)

    print('{} download ok!!'.format(dirname))
    os.chdir('/Users/nemo/Pictures/legbaby')

for i in source.xpath('/html/body/div[2]/div[3]/ul/li'):
    dirname = (i.xpath('./p[5]/a/text()')[0]).encode("iso-8859-1").decode('utf8')
    pagenum = i.xpath('./p[1]/text()')[0].split(' ')[1]
    pic_nid = re.search('\d+', i.xpath('./p[5]/a/@href')[0]).group(0)
    os.mkdir(dirname)
    print('{} mkdir ok'.format(dirname))
    os.chdir(os.getcwd() + '/' + dirname)
    print('{} download start.'.format(dirname))
    down_pic(dirname, pagenum, pic_nid)

print('all download ok, please cheak!!')
