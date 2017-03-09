# -*- coding: utf-8 -*-
import scrapy
from refugee_scraper.items import RefugeeScraperItem
import datetime

class GrapevineSpider(scrapy.Spider):

    name = "grapevine"
    allowed_domains = ["grapevine.is"]

    download_delay = 1
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36"
    start_urls = ['https://grapevine.is/news/page/1/']

    def parse(self, response):
        page_list = list(range(1,100))

        url = self.start_urls[0]
        for page in page_list:
            
            url = url.replace(str(page), str(page+1))            
            request = scrapy.Request(url, callback=self.parse_frontpage)
            yield request

    def parse_frontpage(self, response):
        
        for sel in response.xpath('//li[@class="news"]'):                        

            #item['title'] = sel.xpath('h3/a/text()').extract_first()
            url = response.urljoin(sel.xpath('h2/a/@href').extract_first())            
            self.logger.info('URL: %s', url)
            request = scrapy.Request(url, callback=self.parse_article)
            yield request            

    def parse_article(self, response):
        item = RefugeeScraperItem()
        item['title'] = response.xpath('//div[contains(@class, "article-view")]/h1/text()').extract_first()
        item['body'] = ''.join(response.xpath('//article/p/text()').extract())
        #item['posted'] = response.xpath('//span[@class="_5mdd"]/span/text()')
        item['posted'] = datetime.datetime.now().date()
        
        #request = scrapy.Request(url, callback=self.parse_comments, meta={'item': item})        
        yield item