# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from refugees.models import Post
from refugee_app.settings_local import KEYWORDS

import logging


class RefugeeScraperPipeline(object):
    def process_item(self, item, spider):        
        #logging.warning('URL: {}'.format(item['url']))

        words = [w.lower() for w in item['body'].split()]
        results = any(w in KEYWORDS for w in words)
        if results:
            logging.info(results)
            if not Post.objects.filter(url=item['url']).exists():
                item.save()
                return item
        return None