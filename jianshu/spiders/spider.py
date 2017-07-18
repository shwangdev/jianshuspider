#coding=utf8

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import logging

from jianshu.items import JianShuFeatureItem, JianShuArticleItem
import re
import urlparse

class JanshuSpider(Spider):

    name = "jianshu"
    allowed_domains = ["www.jianshu.com"]
    domain_url = 'http://www.jianshu.com'
    start_urls = [
        "http://www.jianshu.com/recommendations/collections?page={}&order_by=hot".format(x) for x in range(1, 2)
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
                    feature_name = name_field.text
                    item['name'] = name_field.text
                    count_field = feature.find('.//*[@class="count"]')
                    if count_field:
                        link  = '{}/{}'.format(self.domain_url, count_field[0].get('href'))
                        item['link'] = link
                        content = count_field.text_content()
                        ac, sc = re.findall(r"[\d.]+K?", content)
                        item['article_count'] = int(ac)
                        if 'K' in sc:
                            n = int( float(re.findall(r'[\d.]+', sc)[0]) * 1000)
                            item['subscribe_count'] = n
                        else:
                            n = int(sc)
                    yield item
                    for i in range(1, 2):
                        yield Request(urlparse.urljoin(link, '?order_by=top&pages={}'.format(i)), dont_filter=True, meta={'feature': feature_name}, callback=self.parse_features)

    def parse_features(self, response):
        #parse jianshu features
        logging.debug(response.url)
        container = response.xpath('//*[@id="list-container"]/ul')
        feature = response.meta['feature']
        if container:
            contents = container[0].root.find_class('content')
            logging.debug('found {} jianshu features'.format(len(contents)))
            for ar in contents:
                article_item = JianShuArticleItem()
                title = ar.find('.//*[@class="title"]')
                url = urlparse.urljoin(self.domain_url, title.get('href'))
                author = ar.find('.//*[@class="name"]').text_content().strip()
                article_item['link'] = url
                article_item['title'] = title.text
                article_item['author'] = author
                meta = re.findall(r'\d+', ar.find('.//*[@class="meta"]').text_content())
                if len(meta) == 3:
                    article_item['views_count'], article_item['comments_count'], article_item['likes_count'] = meta
                    article_item['rewards_count'] = 0
                elif len(meta) == 4:
                    article_item['views_count'], article_item['comments_count'], article_item['likes_count'], article_item['rewards_count'] = meta
                else:
                    logging.error('Invalid meta information')
                yield Request(url=url, method='GET', dont_filter=True, meta={'item': article_item}, callback=self.parse_articles)

    def parse_articles(self, response):
        logging.debug('parsing article url: {}'.format(response.url))
        container = response.xpath('//*[@class="author"]')
        article_item = response.meta['item']
        if container :
            meta = container[0].root.find('.//*[@class="meta"]').text_content().strip().split('\n')
            #print meta
            article_item['publish_time'] = meta[0][:-1]
            article_item['words_count'] = int(re.findall(r'(\d+)', meta[1].strip())[0])
        yield article_item
