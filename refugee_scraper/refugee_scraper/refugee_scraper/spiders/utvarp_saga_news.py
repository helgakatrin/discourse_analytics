# -*- coding: utf-8 -*-
import scrapy
from refugee_scraper.items import RefugeeScraperItem
from datetime import datetime
import locale

class UtvarpSagaNewsSpider(scrapy.Spider):
    name = "utvarp_saga_news"
    allowed_domains = ["utvarpsaga.is"]
    download_delay = 2
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36"

    def start_requests(self):
        locale.setlocale(locale.LC_ALL, 'is_IS')
        for i in range(1,1000):
            yield scrapy.Request('http://utvarpsaga.is/frettir/page/{}/'.format(i), self.parse)


    def parse(self, response):

        for sel in response.xpath('//div[@class="entry-list-right"]'):
            #item['title'] = sel.xpath('h3/a/text()').extract_first()
            url = response.urljoin(sel.xpath('h2/a/@href').extract_first())            
            request = scrapy.Request(url, callback=self.parse_article)
            yield request            
    
    def parse_article(self, response):
        
        self.logger.info('Locale: {}'.format(locale.getlocale()))
        item = RefugeeScraperItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        item['body'] = ' '.join(response.xpath('//div[@class="entry-content"]/p/text()').extract())
        item['url'] = response.url
        try:
            posted = response.xpath('//time/text()').extract()[0]
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
