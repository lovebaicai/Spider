# -*- coding: utf-8 -*-

# Scrapy settings for koreanhot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import datetime

BOT_NAME = 'hotitems'

SPIDER_MODULES = ['hotitems.spiders']
NEWSPIDER_MODULE = 'hotitems.spiders'
ITEM_PIPELINES = {  
    'hotitems.pipelines.HotitemsPipeline':300  
} 

#LOG_LEVEL = 'WARNING'
LOG_LEVEL = 'INFO'
#LOG_LEVEL = 'DEBUG'
LOG_FILE='{}/{}_spider.log'.format('./log', datetime.date.today())
LOG_FORMAT= '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 10
ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
	    'hotitems.middleware.UserAgentMiddleware': 401}
