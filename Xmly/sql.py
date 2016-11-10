#!/usr/bin/env python
#-*- coding:utf-8-*-

import logging
import MySQLdb as mdb

tabname = 'news'
con = mdb.connect('localhost', 'root', 'ubuntu', 'sound', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

try:
#    cur.execute('create table %s select * from albumsound where 1=2' % (tabname))
    cur.execute('alter table %s add column avgplaycount varchar(255)' % (tabname))
    cur.execute('alter table %s add column soundcount varchar(255)' % (tabname))
    cur.execute('alter table %s add column sumtime varchar(255)' % (tabname))
    cur.execute('alter table %s add column avgtime varchar(255)' % (tabname))
except Exception as e:
    pass


#sql = 'SELECT albumurl FROM %s'
def AlbumSql():
    albumnumber = cur.execute('select albumurl from %s' % (tabname))
    info = cur.fetchall()
    for url in info:
        args =  url[0]
    #    print args
        sql1 = 'select sound_time from allsound where albumurl=%s'
        playcount = cur.execute('select playcount from %s where albumurl="%s"' % (tabname, args))
        try:
            counts = cur.fetchone()
            count = float(counts[0][:-1].encode('utf-8'))
        except:
            count = 0
        sumtime = cur.execute(sql1, args)
        sumtimes = cur.fetchall()
        sumtime=0
        try:
            for sum in sumtimes:
                sumtime = sumtime + int(sum[0].encode('utf-8'))
        except:
            sumtime = 0
        try:
            avgtime = sumtime/len(sumtimes)
        except:
            avgtime = 0
        soundcount = len(sumtimes)
        try:
            avgplaycount = count/soundcount
            avgplaycount = str("%.2f" % avgplaycount) + 'W'
        except:
            avgplaycount = 0
        cur.execute('update %s set soundcount=%s where albumurl="%s"' % (tabname, soundcount, args))
        try:
            cur.execute('update %s set avgplaycount="%s" where albumurl="%s"' % (tabname, avgplaycount.encode('utf-8', 'ignore'), args))
        except:
            pass
        cur.execute('update %s set sumtime=%s where albumurl="%s"' % (tabname, sumtime, args))
        cur.execute('update %s set avgtime=%s where albumurl="%s"' % (tabname, avgtime, args))
        con.commit()
        print '%s write ok' % args

def Csv():
    import csv
    csvFile = open('tabname.csv','w+')
    writer = csv.writer(csvFile)
    writer.writerow(('id', 'albumtitle', 'music_type', 'author', 'playcount', 'tag', 'starttime', 'endtime', 'albumurl', 'avgplaycount', 'soundcount', 'sumtime', 'avgtime'))
    #sql1 = 'select * from newsound'
    excel = cur.execute('select * from %s' % (tabname))
    datas = cur.fetchall()
    for data in datas:
        writer.writerow((data[0], data[1].encode('utf-8', 'ignore'),data[2].encode('utf-8', 'ignore'),
                         data[3].encode('utf-8', 'ignore'),data[4].encode('utf-8', 'ignore'),
                         data[5].encode('utf-8', 'ignore'),data[6].encode('utf-8', 'ignore'),
                         data[7].encode('utf-8', 'ignore'), data[8].encode('utf-8', 'ignore'),
                         data[9].encode('utf-8', 'ignore'), data[10].encode('utf-8', 'ignore'),
                         data[11].encode('utf-8', 'ignore'), data[12].encode('utf-8', 'ignore')))
    csvFile.close()
    print 'Csv wirte ok!!!'

def Email():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    import datetime

    user = 'test@test.com'
    pwd = 'test'
    to = ['test@test.com', 'test@test.com']
    msg = MIMEMultipart()
    msg['Subject']  = '%s' % tabname
    msg['From'] = user
    msg['To'] = ','.join(to)  # 务必加上,smtplib的bug.

    part = MIMEText('%s') % tabname
    msg.attach(part)

    part1 = MIMEApplication(open('tabname.csv','rb').read())
    part1.add_header('Content-Disposition', 'attachment', filename="newsound.csv")
    msg.attach(part1)

    server = smtplib.SMTP('smtp.exmail.qq.com')
    server.login(user, pwd)
    server.sendmail(user, to, msg.as_string())
    server.close()
    print 'Email send ok !!!'

if __name__ =='__main__':
    AlbumSql()
    print 'AlbumSql write ok!!'
    Csv()
    print 'Csv write ok!!'
    Email()
    cur.close()
    con.commit()
    con.close()
    print 'all ok!!'
