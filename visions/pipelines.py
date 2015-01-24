# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonItemExporter, PprintItemExporter

class VisionsPrettyPipeline(object):

  def __init__(self):
    self.exporter = None

  def open_spider(self, spider):
    if spider.name == "product":
      self.exporter = PprintItemExporter(open('data/products.txt', 'w'))
      self.exporter.start_exporting()

  def process_item(self, item, spider):
    if spider.name == "product":
      self.exporter.export_item(item)
      return item

    else:
      return item

  def close_spider(self, spider):
    if spider.name == "product":
      self.exporter.finish_exporting()

class VisionJsonPipeline(object):

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