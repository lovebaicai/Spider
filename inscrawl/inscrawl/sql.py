#-*- coding:utf-8 -*-

import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS ins_data')
cursor.execute('create table ins_data(pic_id VARCHAR (255) ,pic_comment VARCHAR (255),pic_like_count VARCHAR (255),pic_url VARCHAR (255), pic_timestamp VARCHAR (255), pic_title VARCHAR (255))')

class Sql:
    @classmethod
    def insert_ins_data(cls,pic_id,pic_title,pic_comment,pic_like_count,pic_url,pic_timestamp):
        sql = "insert into ins_data (pic_id,pic_title,pic_comment,pic_like_count, pic_url, pic_timestamp) values ('%s','%s','%s','%s','%s','%s')" % (pic_id,pic_title,pic_comment,pic_like_count, pic_url, pic_timestamp)
        cursor.execute(sql)
        conn.commit()

    @classmethod
    def select_id(cls,pic_id):
        sql = "SELECT EXISTS (select 1 from ins_data where pic_id = '%s')" % pic_id
        cursor.execute(sql)
        return cursor.fetchall()[0]
