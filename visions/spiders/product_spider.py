from scrapy.spider import Spider
from scrapy.selector import Selector
from visions.items import ProductItem
from visions import utils
from scrapy.http import Request

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
    query = '#ctl00_tdMainPanel > div > div > div > h1::text'
    return response.css(query).extract()[0]

  def _extract_detail_link(self, response):
    query = "a#ctl00_ContentPlaceHolder1_ProductItemListUC1_ctrlProducts_ctl00_ProductItemUC1_lnkProductDetail::attr(href)"
    
    # categories that have no products listed throw an IndexError
    try:
      link = response.css(query).extract()[0]
    except IndexError:
      link = None

    return link

  def _extract_title(self, response):
    query = "span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblProdTitle::text"
    return response.css(query).extract()[0]

  def _extract_regular_price(self, response):
    query = 'span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblRegprice > font::text'
    
    try:
      price = response.css(query).extract()[0]
    except IndexError:
      price = None

    return price

  def _extract_sale_price(self, response):
    query = 'span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblSaleprice > font::text'
    
    try:
      price = response.css(query).extract()[0]
    except IndexError:
      price = None

    return price

  def _extract_availability(self, response):
    #check for add to cart == available online
      #check for web only == not available in store
    #check for store only == available in store only
    pass