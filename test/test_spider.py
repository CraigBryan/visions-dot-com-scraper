import scrapy
import scrapy.contrib.loader

class TestResult(scrapy.item.Item):
  result = scrapy.item.Field()

class SelectorTestSpider(scrapy.spider.Spider):
  name = 'selector_test'

  #TODO pass in query and start_urls with -a foo=bar
  def __init__(self, category=None, start_url=None, 
               query=None, *args, **kwargs):
    super(SelectorTestSpider, self).__init__(*args, **kwargs)
    self.start_urls = [start_url]
    self.query = query

  def parse(self, response):
    result = response.css(self.query).extract()[0]
    l = scrapy.contrib.loader.ItemLoader(TestResult(), result)
    l.add_value('result', result)
    yield l.load_item()