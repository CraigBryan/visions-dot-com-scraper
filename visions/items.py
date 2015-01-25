# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from visions.custom_fields import NumberField

# A Scrapy Item to hold product information
class ProductItem(scrapy.Item):
  category = scrapy.Field()
  title = scrapy.Field()
  regular_price = scrapy.Field()
  sale_price = scrapy.Field()
  availability = scrapy.Field()

# A Scrapy Item to hold category information
class CategoryItem(scrapy.Item):
  name = scrapy.Field()
  url = scrapy.Field()