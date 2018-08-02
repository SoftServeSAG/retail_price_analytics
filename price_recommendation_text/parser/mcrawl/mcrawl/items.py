# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class McrawlItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    condition = scrapy.Field()
    size = scrapy.Field()
    shipping = scrapy.Field()
    categories = scrapy.Field()
    url = scrapy.Field()
    num_cat = scrapy.Field()
    id = scrapy.Field()
