##### instagram 爬虫项目说明

- 运行start.sh开始抓取数据
- 可自定义抓取username
- 抓取数据保存在sqlite3（data.db）
- 抓取字段为：图片id，图片url，图片评论，图片点赞数，图片标题
- 可使用crontab定时执行，已增加重复图片过滤（以pic_id为key）
