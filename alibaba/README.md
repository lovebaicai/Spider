#### market-tracker爬虫项目说明
- 项目组成：
  1. 项目开发语言为python2.7。项目部署地址为：10.30.97.143:/opt/codebase/crawler
  2. 爬虫模块（hotitems）：包含18个平台爬虫，使用Scrapy框架爬取，重写Scrapy中间件，通过查询Pg数据库获取需要搜索的品牌Url，爬取平台搜索结果列表页，爬取数据生成本地文件，按日期保存
  3. 数据处理模块（all_data.sh）：整合每日每个平台获取的数据，上传至培公服务器，进行数据筛选整合
  4. 使用start.sh执行

- 项目执行：
  ```
  virtualenv venv && source venv/bin/activate
  git clone git@gitlab.izene.com:search-base/market-tracker_v2_url_library.git
  pip install -r requirements.txt -i https://pypi.douban.com/simple
  cd market-tracker_v2_url_library && ./start.sh
  ```
- Pg数据库说明：
  1. 查询命令：
  ```
  select id,search_url from mtcms.dim_search_url_seed where source_id = (source_id) and is_valid = 1
  ```