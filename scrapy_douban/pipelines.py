# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,re

# 将爬取到的数据存储到mysql中

class ScrapyDoubanPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host='127.0.0.1',user='root',password='root',database="Douban",charset='utf8')
        self.cur=self.conn.cursor()


    def process_item(self, item, spider):
        if spider.name == 'spider':
            self.cur.execute('SHOW TABLES;')
            tables=[self.cur.fetchall()]
            table_list=re.findall('(\'.*?\')',str(tables))
            table_list=[re.sub("'",'',each) for each in table_list]
            if 'movies' in table_list:
                pass
            # test库中没有movies表，则创建。
            else:
                creat_movie='CREATE TABLE movies (id BIGINT NOT NULL AUTO_INCREMENT,rank VARCHAR(10) NOT NULL,name VARCHAR(100) NOT NULL,info VARCHAR(100) NOT NULL,score VARCHAR(10) NOT NULL,num VARCHAR(10),PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                self.cur.execute(creat_movie)
            try:
                self.cur.execute("SELECT name FROM movies WHERE ")
                repeat=self.cur.fetchone()
                if repeat:
                    pass
                else:
                    sql="""INSERT INTO movies (rank,name,info,score,num) VALUES (%s,%s,%s,%s,%s)"""
                    self.cur.execute(sql,(item['rank'],item['name'],item['info'],item['star'],item['number']))
                    self.conn.commit()
            except Exception as e:
                print('write mysql error')

    def close(self):
        self.cur.close()
        self.conn.close()
            
