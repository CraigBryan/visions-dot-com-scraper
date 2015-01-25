# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonItemExporter, PprintItemExporter
from scrapy.exceptions import DropItem

class VisionsPrettyPipeline(object):

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

  def process_item(self, item, spider):
    if spider.name == "product":
      self._validate_product(item)
      return item

    elif spider.name == "category":
      self._validate_category(item)
      return item

    else:
      return item

  # Because the website uses the sale price id as the regular price sometimes,
  # we swap the sale price to the regular price
  def _validate_product(self, item):
    if not item['regular_price'] and item['sale_price']:
      item['regular_price'] = item['sale_price']
      item['sale_price'] = None

  # There is a link found that is just to expand a menu. It has no real url, so
  # it gets filtered out
  def _validate_category(self, item):
    if item['url'] == '#' or item['url'] == '':
      raise DropItem("Empty url found")
