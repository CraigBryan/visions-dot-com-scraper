import scrapy
import scrapy.contrib.loader

class TestResult(scrapy.item.Item):
    """Simple item to hold test results from the test spider"""
    result = scrapy.item.Field()

class SelectorTestSpider(scrapy.spider.Spider):
    """
    Simple spider that applies the given CSS selector to the given URL and returns
    the first text result from the list of Scrapy Selector elements
    """ 
    name = 'selector_test'

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