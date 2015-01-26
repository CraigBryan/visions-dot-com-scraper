# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import JsonItemExporter, PprintItemExporter
from scrapy.exceptions import DropItem

class VisionsPrettyPipeline(object):
    """
    Pretty-prints category and product data to a file (data/category.txt or
    data/product.txt)
    """
    def __init__(self):
        self.exporter = None

    def open_spider(self, spider):
        self.exporter = PprintItemExporter(open('data/%s.txt' %spider.name, 'w'))
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()

class VisionsJsonPipeline(object):
    """
    Prints category and product data to a JSON file (data/category.json or
    data/product.json)
    """
    def __init__(self):
        self.exporter = None

    def open_spider(self, spider):
        self.exporter = JsonItemExporter(open('data/%s.json' %spider.name, 'w'))
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()

class VisionsValidatorPipeline(object):
    """
    Pipeline to modify any malformed retrieved data.
    """
    def process_item(self, item, spider):
        if spider.name == "product":
            self._validate_product(item)
            return item

        elif spider.name == "category":
            self._validate_category(item)
            return item

        else:
            return item

    def _validate_product(self, item):
        """
        Swaps the sale price for the regular price when a regular price is not 
        present and the sale price is present.
        """
        if not item['regular_price'] and item['sale_price']:
            item['regular_price'] = item['sale_price']
            item['sale_price'] = None

    def _validate_category(self, item):
        """
        Drops any category items that have an empty url.
        """
        if item['url'] == '#' or item['url'] == '':
            raise DropItem("Empty url found")