# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductItem(scrapy.Item):
  title = scrapy.Field()
  price = scrapy.Field()
  availability = scrapy.Field()

class CategoryItem(scrapy.Item):
  name = scrapy.Field()
  url = scrapy.Field()