# -*- coding: utf-8 -*-
import scrapy,sys,os
print(os.path.dirname(__file__))
sys.path.append('/Users/fanhao/project/scrapy_douban/')
from scrapy_douban.items import ScrapyDoubanItem


class MovieSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['http://movie.douban.com/top250/']

    def parse(self, response):
        item=ScrapyDoubanItem()
        movies=response.xpath("//ol[@class='grid_view']/li")
        # 遍历电影列表
        for movie in movies:
            item['movie_rank']=movie.xpath(".//div[@class='pic']/em/text()").extract()[0]
            item['movie_name']=movie.xpath(".//div[@class='hd']/a/span[@class='title']/text()").extract()[0]
            item['movie_star']=movie.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract()[0]
            movie_quote=movie.xpath(".//span[@class='inq']/text()").extract()
            if movie_quote:
                item['movie_quote']=movie_quote[0]
            item['movie_number']=movie.xpath(".//div[@class='star']/span/text()").re(r'(\d+)人评价')[0]
            item['movie_link']=movie.xpath(".//div[@class='hd']/a/@href").extract()[0]
            dict=movie.xpath(".//div[@class='bd']/p/text()").extract()
            # 对爬取到数据进行处理，得到我们想要的数据
            
            movie_info=dict[1].strip().split('\xa0')
            for i in movie_info:
                if i == '/':
                    movie_info.remove('/')
            # 处理得到list
            item['movie_year']=movie_info[0]
            item['movie_country']=movie_info[1]
            item['movie_type']=movie_info[2]

            yield item
        # 获取下一页连接
        next_url=response.xpath("//span[@class='next']/a/@href").extract()
        if next_url:
            next_url='http://movie.douban.com/top250'+next_url[0]
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

