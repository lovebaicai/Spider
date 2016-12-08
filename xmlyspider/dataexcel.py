#!/usr/bin python
#-*-coding:utf-8-*-

import datetime
import xlwt
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'ubuntu', 'spider', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

time1 = datetime.datetime.now().strftime('%Y%m%d')
time2 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
time3 = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d')

sqlname1 = 'sound_' + time1
sqlname2 = 'sound_' + time2
sqlname3 = 'sound_' + time3

time1 = datetime.datetime.now().strftime('%Y%m%d')
tabname = 'sound_' + time1


#设置单元格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    style.font = font

    return style

#写excel
def write_excel():
    try:
        f = xlwt.Workbook() #创建工作簿
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) #创建sheet
        row0 = [u'频道',u'专辑数量',u'日专辑增长量',u'日专辑增长率',u'周专辑增长率',u'播放总量', u'日播放增长量', u'日播放增长率',u'周播放增长率',
                u'播客数量',u'日播客增长量', u'日播客增长率', u'周播客增长率', u'总节目数',u'新增节目数', u'日节目增长率', u'周节目增长率',
                u'总评论量', u'评论数均值', u'评分均值']
        column0 = [u'全部',u'有声书',u'教育培训',u'资讯',u'商业财经',u'音乐',u'历史',u'人文',u'外语',u'儿童',u'情感生活',u'娱乐',
                   u'IT科技',u'时尚生活',u'相声评书',u'健康养生',u'戏曲',u'广播剧',u'旅游']
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

        # 生成第一列
        for i in range(0, len(column0)):
            sheet1.write(i + 1, 0, column0[i], set_style('Times New Roman', 220))


        sheet2 = f.add_sheet(u'sheet2', cell_overwrite_ok=True)
        row0 = [u'频道类型', u'专辑名称', u'播客名称', u'上线时间', u'更新时间', u'付费类型', u'价格', u'评分', u'播放总量',
                u'免费节目播放均值', u'付费节目播放均值', u'单集播放均值', u'单集数量']
        # 生成第一行
        for i in range(0, len(row0)):
            sheet2.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    except:
        pass

    i = 2

    column = ['有声书', '教育培训', '资讯', '商业财经', '音乐', '历史', '人文', '外语', '儿童', '情感生活', '娱乐',
                'IT科技', '时尚生活', '相声评书', '健康养生', '戏曲', '广播剧', '旅游']

    #总专辑数量
    sql = """SELECT COUNT(distinct `Albumtitle`) FROM {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 1, info[0])
    #专辑增长量
    sql1 = """SELECT COUNT(distinct `Albumtitle`) FROM {}""".format(sqlname2)
    number1 = cur.execute(sql1)
    info1 = cur.fetchone()
    add = info[0] - info1[0]
    #日专辑增长率
    add1 = (info[0] - info1[0]) / float(info[0])
    add1 = (format(add1, '.2%'))
    sheet1.write(1, 2, add)
    sheet1.write(1, 3, add1)
    #周专辑增长率
    try:
        sql2 = """SELECT COUNT(distinct `Albumtitle`) FROM {}""".format(sqlname3)
        number1 = cur.execute(sql2)
        info1 = cur.fetchone()
        add = (info[0] - info1[0]) / float(info[0])
        add = (format(add, '.2%'))
        sheet1.write(1, 4, add)
    except:
        sheet1.write(1, 4, 'None')


    #播放总量
    sql = """select sum(SinglePlayCount) from {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 5, info[0])
    #总播放每日增长量
    sql1 = """select sum(SinglePlayCount) from {}""".format(sqlname2)
    number1 = cur.execute(sql1)
    info1 = cur.fetchone()
    add = info[0] - info1[0]
    add1 = (info[0] - info1[0]) / float(info[0])
    add1 = (format(add1, '.2%'))
    sheet1.write(1, 6, add)
    sheet1.write(1, 7, add1)
    #总专辑周播放量增长率
    try:
        sql2 = """select sum(SinglePlayCount) from {}""".format(sqlname3)
        number1 = cur.execute(sql2)
        info1 = cur.fetchone()
        add = (info[0] - info1[0]) / float(info[0])
        add = (format(add, '.2%'))
        sheet1.write(1, 8, add)
    except:
        sheet1.write(1, 8, 'None')

    #总节目数
    sql = """select count('Title') from {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 13, info[0])
    #日总新增节目数量,增长率
    sql1 = """select count('Title') from {}""".format(sqlname2)
    number1 = cur.execute(sql1)
    info1 = cur.fetchone()
    add = info[0] - info1[0]
    add1 = (info[0] - info1[0]) / float(info[0])
    add1 = (format(add1, '.2%'))
    sheet1.write(1, 14, add)
    sheet1.write(1, 15, add1)
    #周总节目增长率
    try:
        sql2 = """select count('Title') from {}""".format(sqlname3)
        number1 = cur.execute(sql2)
        info1 = cur.fetchone()
        add = (info[0] - info1[0]) / float(info[0])
        add = (format(add, '.2%'))
        sheet1.write(1, 16, add)
    except:
        sheet1.write(1, 16, 'None')

    #总评论量
    sql = """select sum(CommentsCount) from {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 17, info[0])

    #总评论均值
    sql = """SELECT AVG(CommentsCount) FROM {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 18, format(info[0], '.2f'))

    #总评分均值
    sql = """SELECT AVG(DISTINCT Albumscore) FROM {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 19, format(info[0], '.2f'))

    #总播客数量
    sql = """SELECT COUNT(distinct `Nickname`) FROM {}""".format(sqlname1)
    number = cur.execute(sql)
    info = cur.fetchone()
    sheet1.write(1, 9, info[0])
    #总播客增长量,增长率
    sql1 = """SELECT COUNT(distinct `Nickname`) FROM {}""".format(sqlname2)
    number1 = cur.execute(sql1)
    info1 = cur.fetchone()
    add = info[0] - info1[0]
    add1 = (info[0] - info1[0]) / float(info[0])
    add1 = (format(add1, '.2%'))
    sheet1.write(1, 10, add)
    sheet1.write(1, 11, add1)
    #周总主播量增长率
    try:
        sql1 = """SELECT COUNT(distinct `Nickname`) FROM {}""".format(sqlname3)
        number1 = cur.execute(sql1)
        info1 = cur.fetchone()
        add = (info[0] - info1[0]) / float(info[0])
        add = (format(add, '.2%'))
        sheet1.write(1, 12, add)
    except:
        sheet1.write(1, 12, 'None')



    #数据筛选
    for col in column:

        #专辑数量
        sql = """SELECT COUNT(distinct `Albumtitle`) FROM {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 1, info[0])
        #今日专辑增长量,增长率
        sql1 = """SELECT COUNT(distinct `Albumtitle`) FROM {} where category_title='{}'""".format(sqlname2, col)
        number1 = cur.execute(sql1)
        info1 = cur.fetchone()
        add = info[0] - info1[0]
        add1 = (info[0] - info1[0]) / float(info[0])
        add1 = (format(add1, '.2%'))
        sheet1.write(i, 3, add1)
        sheet1.write(i, 2, add)
        #周专辑增长率
        try:
            sql2 = """SELECT COUNT(distinct `Albumtitle`) FROM {} where category_title='{}'""".format(sqlname3, col)
            number1 = cur.execute(sql2)
            info1 = cur.fetchone()
            add = (info[0] - info1[0]) / float(info[0])
            add = (format(add, '.2%'))
            sheet1.write(i, 4, add)
        except:
            sheet1.write(i, 4, 'None')

        #专辑播放总量
        sql ="""select sum(SinglePlayCount) from {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 5, info[0])
        #专辑今日播放量增长量,增长率
        sql1 ="""select sum(SinglePlayCount) from {} where category_title='{}'""".format(sqlname2, col)
        number1 = cur.execute(sql1)
        info1 = cur.fetchone()
        add = info[0] - info1[0]
        add1 = (info[0] - info1[0]) / float(info[0])
        add1 = (format(add1, '.2%'))
        sheet1.write(i, 7, add1)
        sheet1.write(i, 6, add)
        #专辑周播放量增长率
        try:
            sql2 = """select sum(SinglePlayCount) from {} where category_title='{}'""".format(sqlname3, col)
            number1 = cur.execute(sql2)
            info1 = cur.fetchone()
            add = (info[0] - info1[0]) / float(info[0])
            add = (format(add, '.2%'))
            sheet1.write(i, 8, add)
        except:
            sheet1.write(i, 8, 'None')

        #播客数量
        sql = """SELECT COUNT(distinct `Nickname`) FROM {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 9, info[0])
        sql1 = """SELECT COUNT(distinct `Nickname`) FROM {} where category_title='{}'""".format(sqlname2, col)
        number1 = cur.execute(sql1)
        info1 = cur.fetchone()
        add = info[0] - info1[0]
        add1 = (info[0] - info1[0]) / float(info[0])
        add1 = (format(add1, '.2%'))
        sheet1.write(i, 11, add1)
        sheet1.write(i, 10, add)
        #周主播量增长率
        try:
            sql2 = """SELECT COUNT(distinct `Nickname`) FROM {} where category_title='{}'""".format(sqlname3, col)
            number1 = cur.execute(sql2)
            info1 = cur.fetchone()
            add = (info[0] - info1[0]) / float(info[0])
            add = (format(add, '.2%'))
            sheet1.write(i, 12, add)
        except:
            sheet1.write(i, 12, 'None')

        #专辑总节目数
        sql = """select count('Title') from {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 13, info[0])
        #每日新增单集节目数量
        sql1 = """select count('Title') from {} where category_title='{}'""".format(sqlname2, col)
        number1 = cur.execute(sql1)
        info1 = cur.fetchone()
        add = info[0] - info1[0]
        add1 = (info[0] - info1[0]) / float(info[0])
        add1 = (format(add1, '.2%'))
        sheet1.write(i, 15, add1)
        sheet1.write(i, 14, add)
        #周节目增长率
        try:
            sql2 = """select count('Title') from {} where category_title='{}'""".format(sqlname3, col)
            number1 = cur.execute(sql2)
            info1 = cur.fetchone()
            add = (info[0] - info1[0]) / float(info[0])
            add = (format(add, '.2%'))
            sheet1.write(i, 16, add)
        except:
            sheet1.write(i, 16, 'None')


        #专辑评论量
        sql = """select sum(CommentsCount) from {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 17, info[0])
        #评论数均值
        sql = """SELECT AVG(CommentsCount) FROM {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 18, format(info[0], '.2f'))

        #评分均值
        sql = """SELECT AVG(DISTINCT Albumscore) FROM {} where category_title='{}'""".format(sqlname1, col)
        number = cur.execute(sql)
        info = cur.fetchone()
        sheet1.write(i, 19, format(info[0], '.2f'))

        i += 1

    sql = """select DISTINCT Albumtitle from {}""".format(sqlname1)
    number = cur.execute(sql)
    infos = cur.fetchall()
    k = 1
    for info in infos:
        #print info[0]
        sheet2.write(k, 1, info[0]) #专辑名称
        #上线时间,更新时间
        sql1 = """select * from {} where Albumtitle='{}'""".format(sqlname1, info[0].encode('utf-8'))
        number1 = cur.execute(sql1)
        info1 = cur.fetchall()
        sheet2.write(k, 2, info1[0][11]) #播客名称
        sheet2.write(k, 5, 'None')  #付费类型
        sheet2.write(k, 6, info1[0][10]) #价格
        sheet2.write(k, 7, info1[0][4])  #评分
        sheet2.write(k, 8, info1[0][7])  #播放总量
        sheet2.write(k, 0, info1[0][12]) #专辑类型
        free = []
        paid = []
        timecount = []
        for info2 in info1:
            timecount.append(info2[9])
            if info2[14] == "False":
                paid.append(float(info2[3].encode('utf-8')))
            else:
                free.append(float(info2[3].encode('utf-8')))
        try:
            sheet2.write(k, 9, format((sum(free) / len(free)), '.2f'))  #免费节目播放量均值
        except:
            sheet2.write(k, 9, 0)
        try:
            sheet2.write(k, 10, format((sum(paid) / len(paid)), '.2f')) #付费节目播放量均值
        except:
            sheet2.write(k, 10, 0)
        sheet2.write(k, 11, format((float(info1[0][7]) / len(free+paid)), '.2f'))   #单集播放量均值
        sheet2.write(k, 12, len(free+paid)) #单集数量
        sheet2.write(k, 3, min(timecount)) #上线时间
        sheet2.write(k, 4, max(timecount))  #更新时间

        k += 1


    #tabname = 'sound_' + str(time1) + '.xls'
    f.save(str(tabname) + '.xls')


if __name__ == '__main__':
    write_excel()
    print 'Excel write ok'
