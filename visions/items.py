# -*- coding: utf-8 -*-

import scrapy


class ProductItem(scrapy.Item):
    """Item to hold product information. The product spider uses this item."""
    category = scrapy.Field()
    title = scrapy.Field()
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    availability = scrapy.Field()


class CategoryItem(scrapy.Item):
    """Item to hold category name and url. The category spider uses this item"""
    name = scrapy.Field()
    url = scrapy.Field()
