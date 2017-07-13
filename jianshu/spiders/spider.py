#coding=utf8

from scrapy.spiders import Spider
from scrapy.selector import Selector

from jianshu.items import JianShuItem

class JanshuSpider(Spider):

    name = "jianshu"
    allowed_domains = ["www.jianshu.com"]
    start_urls = [
        "http://www.jianshu.com/"
    ]

    def parse(self, response):
        items = response.xpath('//*[@id="list-container"]/ul')[0].root.find_class('title')
        for item in items:
            record = JianShuItem()
            record['title'] = unicode(item.text)
            record['link'] = 'http://www.jianshu.com{}'.format(item.get('href'))
            print record['title'], record['link']
            yield record
