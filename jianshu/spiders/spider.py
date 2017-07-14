#coding=utf8

from scrapy.spiders import Spider
from scrapy.selector import Selector

from jianshu.items import JianShuFeatureItem, JianShuArticleItem
import re

class JanshuSpider(Spider):

    name = "jianshu"
    allowed_domains = ["www.jianshu.com"]
    domain_url = 'http://www.jianshu.com'
    start_urls = [
        "http://www.jianshu.com/recommendations/collections?page={}&order_by=hot".format(x) for x in range(1,40)
    ]

    # def parse(self, response):
    #     items = response.xpath('//*[@id="list-container"]/ul')[0].root.find_class('title')
    #     for item in items:
    #         record = JianShuItem()
    #         record['title'] = unicode(item.text)
    #         record['link'] = 'http://www.jianshu.com{}'.format(item.get('href'))
    #         print record['title'], record['link']
    #         yield record

    def parse(self, response):
        container = response.xpath('//*[@id="list-container"]')
        if container:
            features = container[0].root.find_class('col-xs-8')
            if features:
                for feature in features:
                    item = JianShuFeatureItem()
                    name_field = feature.find('.//*[@class="name"]')
                    item['name'] = name_field.text
                    count_field = feature.find('.//*[@class="count"]')
                    if count_field:
                        item['link'] = '{}/{}'.format(self.domain_url, count_field[0].get('href'))
                        content = count_field.text_content()
                        print content
                        #item['article_count'], item['subscribe_count'] = re.findall(r"[\d.]+K?", content)
                        ac, sc = re.findall(r"[\d.]+K?", content)
                        item['article_count'] = int(ac)
                        if 'K' in sc:
                            n = int( float(re.findall(r'[\d.]+', sc)[0]) * 1000)
                            item['subscribe_count'] = n
                        else:
                            n = int(sc)
                    yield item
