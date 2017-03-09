# -*- coding: utf-8 -*-
import scrapy
from refugee_scraper.items import RefugeeScraperItem
import datetime

class VisirNewsSpider(scrapy.Spider):
    name = "visir_news"
    allowed_domains = ["visir.is"]
    start_urls = [
        "http://www.visir.is/section/frettir",
        #"http://www.visir.is/bjarni-utilokar-ekki-breytingar-a-listunum/article/2016160919848"
    ]
    download_delay = 1
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36"


    def parse(self, response):
           
        for sel in response.xpath('//div[@class="newslists clearfix"]/div[@class="x6 lbf"]/div[@class="x6 ml0"]/div[contains(@class, "newsitem")]'):            
            #item['title'] = sel.xpath('h3/a/text()').extract_first()
            url = response.urljoin(sel.xpath('h3/a/@href').extract_first())            
            request = scrapy.Request(url, callback=self.parse_article)
            yield request            
    
    def parse_article(self, response):
        item = RefugeeScraperItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['body'] = ''.join(response.xpath('//div[@itemprop="articleBody"]/p/hardreturn/text()').extract())
        #item['posted'] = response.xpath('//span[@class="_5mdd"]/span/text()')
        item['posted'] = datetime.datetime.now().date()
        #request = scrapy.Request(url, callback=self.parse_comments, meta={'item': item})        
        yield item

    def parse_comments(self, response):
        item = response.meta['item']
