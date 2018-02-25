# -*- encoding:utf-8 -*-

import re
import os
import random
import json
import logging
from user_agents import agents
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware



class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        #ip_pools = {'ip': '172.16.1.99:4321'}
        proxy = {
            'http': 'http://izene-office1.8866.org:4321',
            'https': 'https://izene-office1.8866.org:4321'}
        request.meta['proxy'] = proxy['https']
