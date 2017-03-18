# -*- coding: utf-8 -*-
import scrapy
from refugee_scraper.items import RefugeeScraperItem
from datetime import datetime
import locale

class VisirNewsSpider(scrapy.Spider):
    name = "visir_news"
    allowed_domains = ["visir.is"]

    def start_requests(self):
        locale.setlocale(locale.LC_ALL, 'is_IS')
        for i in range(1,1000):
            yield scrapy.Request('http://www.visir.is/section/FRETTIR?page={}'.format(i), self.parse)

    download_delay = 2
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36"


    def parse(self, response):

        for sel in response.xpath('//div[@class="newslists clearfix"]/div[@class="x6 lbf"]/div[@class="x6 ml0"]/div[contains(@class, "newsitem")]'):
            #item['title'] = sel.xpath('h3/a/text()').extract_first()
            url = response.urljoin(sel.xpath('h3/a/@href').extract_first())            
            request = scrapy.Request(url, callback=self.parse_article)
            yield request            
    
    def parse_article(self, response):
        
        self.logger.info('Locale: {}'.format(locale.getlocale()))
        item = RefugeeScraperItem()
        item['title'] = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        item['body'] = ''.join(response.xpath('//div[@itemprop="articleBody"]/p/hardreturn/text()').extract())
        item['url'] = response.url
        try:
            posted = response.xpath('//div[contains(@class, "FRETTIR-cat")]/span[@class="date"]/text()').extract()[1]
        except IndexError:
            item['posted'] = None
        else:
            """
            month = posted.split()[1].title()
            splitted = posted.split()
            splitted[1] = month
            posted = ' '.join(splitted)
            """
            try:
                item['posted'] = datetime.strptime(posted, '%d. %B %Y').date()
            except:
                raise
        #self.logger.info('Date: {}'.format(response.xpath('//meta[@itemProp="datePublished"]/@content').extract()))
        #item['posted'] = datetime.datetime.now().date()
        #request = scrapy.Request(url, callback=self.parse_comments, meta={'item': item})        
        yield item

    def parse_comments(self, response):
        item = response.meta['item']
