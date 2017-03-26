# -*- coding: utf-8 -*-
import scrapy
from refugee_scraper.items import RefugeeScraperItem
from datetime import datetime
import locale
from refugees.models import Post

class DVNewsSpider(scrapy.Spider):
    name = "dv_news"
    allowed_domains = ["dv.is"]
    download_delay = 1
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36"
    post_list = Post.objects.values_list('url', flat=True).filter(url__startswith="http://www.dv.is")

    def start_requests(self):
        locale.setlocale(locale.LC_ALL, 'is_IS')
        
        for year in range(2009, 2018):
            for month in range(1, 13):
                yield scrapy.Request('http://www.dv.is/frettir/{}/{}/'.format(year, month), self.parse)
        
        #yield scrapy.Request('http://www.dv.is/frettir/2017/3/', self.parse)

    def parse(self, response):

        for sel in response.xpath('//ul[@class="archive_day"]/li'):            
            url = response.urljoin(sel.xpath('a/@href').extract_first())
            if not url in self.post_list:
                request = scrapy.Request(url, callback=self.parse_article)            
                yield request
    
    def parse_article(self, response):
        
        self.logger.info('Locale: {}'.format(locale.getlocale()))
        item = RefugeeScraperItem()
        item['title'] = response.xpath('//h1[contains(@class, "headline")]/text()').extract_first()
        item['body'] = ' '.join(response.xpath('//div[@class="text_body"]/p/text()').extract())
        item['url'] = response.url
        try:
            posted = response.xpath('//span[contains(@class, "date")]/text()').extract_first()
        except IndexError:
            item['posted'] = None
        else:
            try:
                item['posted'] = datetime.strptime(posted, '%d. %B %Y').date()
            except:
                raise
        #self.logger.info('Date: {}'.format(response.xpath('//meta[@itemProp="datePublished"]/@content').extract()))
        #item['posted'] = datetime.datetime.now().date()
        #request = scrapy.Request(url, callback=self.parse_comments, meta={'item': item})        
        yield item