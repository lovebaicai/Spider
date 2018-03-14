#-*- coding:utf-8 -*-

import re
import json
import scrapy
from urllib.parse import quote

from inscrawl.items import InscrawlItem
from inscrawl.sql import Sql

class InsSpider(scrapy.Spider):
    name = 'inscrawl'

    start_urls = ['https://www.instagram.com/ahmad_monk/',]
    
    def parse(self, response):
        page = json.loads(re.search('window._sharedData = (.+);', 
                            response.body.decode('utf-8')).group(1))
        query_id = page['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        detail_url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=' + quote('{"id":"22543622","first":50,"after":"%s"}' % query_id)
        infos = page['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for info in infos:
            item = InscrawlItem()
            item['pic_id'] = info['node']['id']
            item['pic_comment'] = info['node']['edge_media_to_comment']['count']
            item['pic_timestamp'] = info['node']['taken_at_timestamp']
            item['pic_like_count'] = info['node']['edge_media_preview_like']['count']
            item['pic_url'] = info['node']['display_url']
            try:
                item['pic_title'] = info['node']['edge_media_to_caption']['edges'][0]['node']['text'] 
            except IndexError as f:
                item['pic_title'] = ''
            yield item
        yield scrapy.Request(detail_url, callback=self.detail_parse)

    def detail_parse(self, response):
        page = json.loads(response.body.decode('utf-8'))
        infos = page['data']['user']['edge_owner_to_timeline_media']['edges']
        next_page_status = page['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        next_query_id = page['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        for info in infos:
            item = InscrawlItem()
            item['pic_id'] = info['node']['id']
            item['pic_comment'] = info['node']['edge_media_to_comment']['count']
            item['pic_timestamp'] = info['node']['taken_at_timestamp']
            item['pic_like_count'] = info['node']['edge_media_preview_like']['count']
            item['pic_url'] = info['node']['display_url']
            try:
                item['pic_title'] = info['node']['edge_media_to_caption']['edges'][0]['node']['text'] 
            except IndexError as f:
                item['pic_title'] = ''

            rets = Sql.select_id(item['pic_id'])
            if rets != 1:
                yield item

        if next_page_status:
            detail_url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=' + quote('{"id":"22543622","first":50,"after":"%s"}' % next_query_id)
            yield scrapy.Request(detail_url, callback=self.detail_parse)
