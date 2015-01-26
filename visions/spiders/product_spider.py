from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from visions.items import ProductItem
from visions import utils
from visions.selectors import PRODUCT_QUERIES as queries

class ProductSpider(Spider):
    """
    This scraper runs over the urls found by the category scraper and finds
    information for one product in each category.
    """
    name = "product"
    allow_domains = ["visions.ca"]

    def __init__(self, category=None, *args, **kwargs):
        """Initializes the start_urls via a utility function"""
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.start_urls = utils.read_category_urls()

    def parse(self, response):
        """
        Populates the product information for each category. If no product exists in
        a given category, an product without data is returned.
        """
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
        """
        The second parse function that the parse function uses to get information 
        about a product from a second webpage.
        """
        item = response.meta['item']

        item["title"] = self._extract_title(response)
        item["regular_price"] = self._extract_regular_price(response)
        item["sale_price"] = self._extract_sale_price(response)
        item["availability"] = self._extract_availability(response)
        return item

    def _extract_category(self, response):
        """Pulls the title of the category from the category page"""
        query = queries["extract_category"]
        try:
            category = response.css(query).extract()[0]
        except IndexError:
            category = None
        return category

    def _extract_detail_link(self, response):
        """Pulls the url of the product detail from the category page"""
        query = queries["extract_detail_link"]
        
        # categories that have no products listed throw an IndexError
        try:
            link = response.css(query).extract()[0]
        except IndexError:
            link = None

        return link

    def _extract_title(self, response):
        """Pulls the product title from the product details page"""
        query = queries["extract_title"]

        try:
            title = response.css(query).extract()[0]
        except IndexError:
            title = None

        return title

    def _extract_regular_price(self, response):
        """Pulls the regular price from the product details page"""
        query = queries["extract_regular_price"]
        
        try:
            price = response.css(query).extract()[0]
        except IndexError:
            price = None

        return price

    def _extract_sale_price(self, response):
        """Pulls the sale price from the product details page"""
        query = queries["extract_sale_price"]
        
        try:
            price = response.css(query).extract()[0]
        except IndexError:
            price = None

        return price

    def _extract_availability(self, response):
        """
        Pulls the availability information from the product details page.
        First it checks for either web only or store only, either of which gives
        all the necessary information. If neither is found, an 'Add to cart'
        element is searched for. If the 'Add to cart' element is found, then it is
        assumed the product is available on both web and in store. If the 
        'Add to cart' element is not found it is assumed it is not available anywhere.
        """
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