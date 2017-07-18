# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import types , json
from scrapy.exceptions import DropItem

class JsonFileJianshuPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line)
            self.file.flush()
            return item

    def close_spider(self, spider):
        self.file.flush()
        self.file.close()
