# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from refugees.models import Post

import logging


class RefugeeScraperPipeline(object):
    def process_item(self, item, spider):        
        #logging.warning('URL: {}'.format(item['url']))
        if not Post.objects.filter(url=item['url']).exists():
            item.save()
            return item
        return