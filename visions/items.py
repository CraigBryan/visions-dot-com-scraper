# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from visions.custom_fields import NumberField

class ProductItem(scrapy.Item):
  category = scrapy.Field()
  title = scrapy.Field()
  regular_price = scrapy.Field()
  sale_price = scrapy.Field()
  availability = scrapy.Field()

class CategoryItem(scrapy.Item):
  name = scrapy.Field()
  url = scrapy.Field()

