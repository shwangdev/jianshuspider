# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianShuFeatureItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    article_count = scrapy.Field()
    subscribe_count = scrapy.Field()

class JianShuArticleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    feature =scrapy.Field()
    words_count = scrapy.Field()
    publish_time = scrapy.Field()
    likes_count = scrapy.Field()
    views_count = scrapy.Field()
    rewards_count = scrapy.Field()
    comments_count = scrapy.Field()
