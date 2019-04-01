# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 电影排名
    movie_rank=scrapy.Field()
    # 电影名字
    movie_name=scrapy.Field()
    # 电影评分
    movie_star=scrapy.Field()
    # 电影简评
    movie_quote=scrapy.Field()
    # 电影评分人数
    movie_number=scrapy.Field()
    # 电影类型
    movie_type=scrapy.Field()
    # 所属国家
    movie_country=scrapy.Field()
    # 年份
    movie_year=scrapy.Field()
    # 电影链接
    movie_link=scrapy.Field()
    
