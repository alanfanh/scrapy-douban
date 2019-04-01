# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,re

# 将爬取到的数据存储到mysql中

class ScrapyDoubanPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host='127.0.0.1',user='root',password='root',database="douban",charset='utf8')
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
                creat_movie='CREATE TABLE movies (id BIGINT NOT NULL AUTO_INCREMENT,rank VARCHAR(10) NOT NULL,name VARCHAR(100) NOT NULL,score VARCHAR(4) NOT NULL,info VARCHAR(100),num VARCHAR(10),movie_type VARCHAR(20),country VARCHAR(10),year VARCHAR(10),link VARCHAR(100),PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                self.cur.execute(creat_movie)
            # 写入数据库失败时，报错
            try:
                self.cur.execute("""SELECT * FROM movies WHERE name=%s""",item['movie_name'])
                # 检测数据是否重复
                repeat=self.cur.fetchone()
                if repeat:
                    pass
                else:
                    sql="""INSERT INTO movies (rank,name,score,info,num,movie_type,country,year,link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    print(sql)
                    self.cur.execute(sql,(item['movie_rank'],item['movie_name'],item['movie_star'],item['movie_quote'],item['movie_number'],item['movie_type'],item['movie_country'],item['movie_year'],item['movie_link']))
                    self.conn.commit()
            except Exception as e:
                print('ValueError:', e)
            return item

    def close(self):
        self.cur.close()
        self.conn.close()
            
