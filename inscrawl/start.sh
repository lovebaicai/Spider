#!/bin/bash

echo "Start crawl"
pip install -r requirements.txt -i https://pypi.douban.com/simple
scrapy crawl inscrawl

