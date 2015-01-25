from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from visions.items import ProductItem
from visions import utils
from visions.selectors import PRODUCT_QUERIES as queries

class ProductSpider(Spider):
  name = "product"
  allow_domains = ["visions.ca"]
  start_urls = []

  def __init__(self, category=None, *args, **kwargs):
    super(ProductSpider, self).__init__(*args, **kwargs)
    self.start_urls = utils.read_category_urls()

  def parse(self, response):
    item = ProductItem()
    item['category'] = self._extract_category(response)

    detail_link = self._extract_detail_link(response)

    if detail_link:
      request = Request(utils.base_detail_url() + detail_link,
                               callback = self.parse_details)
      
      request.meta['item'] = item
      return request
    
    else:
      item["title"] = None
      item["regular_price"] = None
      item["sale_price"] = None
      item["availability"] = None

      return item

  def parse_details(self, response):
    item = response.meta['item']

    item["title"] = self._extract_title(response)
    item["regular_price"] = self._extract_regular_price(response)
    item["sale_price"] = self._extract_sale_price(response)
    item["availability"] = self._extract_availability(response)
    return item

  #pulls the category from the title of the main product panel
  def _extract_category(self, response):
    query = queries["extract_category"]
    return response.css(query).extract()[0]

  def _extract_detail_link(self, response):
    query = queries["extract_detail_link"]
    
    # categories that have no products listed throw an IndexError
    try:
      link = response.css(query).extract()[0]
    except IndexError:
      link = None

    return link

  def _extract_title(self, response):
    query = queries["extract_title"]
    return response.css(query).extract()[0]

  def _extract_regular_price(self, response):
    query = queries["extract_regular_price"]
    
    try:
      price = response.css(query).extract()[0]
    except IndexError:
      price = None

    return price

  def _extract_sale_price(self, response):
    query = queries["extract_sale_price"]
    
    try:
      price = response.css(query).extract()[0]
    except IndexError:
      price = None

    return price

  # Checks for a store only and web only. If neither are found, looks for 
  # 'add to cart' button (and then its assumed its available on both)
  def _extract_availability(self, response):
    web_only_query = queries["extract_availability_web_only"]
    store_only_query = queries["extract_availability_store_only"]
    add_to_cart_query = queries["extract_availability_add_to_cart"]

    #check for web only == not available in store
    if response.css(web_only_query):
      availability = self._set_availability(True, False)

    #check for store only == available in store only
    elif response.css(store_only_query):
      availability = self._set_availability(False, True)

    #check for add to cart == available online and in store
    elif response.css(add_to_cart_query):
      availability = self._set_availability(True, True)

    #not available at either (assumed)
    else:
      availability = self._set_availability(False, False)

    return availability

  def _set_availability(self, web, store):
    return {"web": web, "store": store}