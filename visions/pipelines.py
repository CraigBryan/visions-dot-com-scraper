# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonItemExporter

class VisionsPipeline(object):

  def __init__(self):
    self.exporter = None

  def open_spider(self, spider):
    if spider.name == "category"
      self.exporter = JsonItemExporter('categories.json')
      self.exporter.start_exporting()

    elif spider.name == "product":
      pass

  def process_item(self, item, spider):
    if spider.name == "category":
      self.exporter.export_item(item)
      return item

    elif spider.name == "product":
      return item

  def close_spider(self, spider):
    if spider.name == "category"
      self.exporter.stop_exporting()

    elif spider.name == "product":
      pass