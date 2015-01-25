from scrapy.spider import Spider
from scrapy.selector import Selector
from visions.items import CategoryItem
from visions.selectors import CATEGORY_QUERIES as queries

class CategorySpider(Spider):
  name = "category"
  allow_domains = ["visions.ca"]
  start_urls = ["http://www.visions.ca"]

  def parse(self, response):
    sel = Selector(response=response)

    links = self._extract_links(sel)

    for name, url in links.items():
      category = CategoryItem()
      category["name"] = name
      category["url"] = url 
      yield category

  def _extract_links(self, selector):
    urls = {}

    #first get the menu expander elements
    expanders = self._get_expanders(selector)

    #then for each one, get a list of link containers 
    for expander in expanders:
      link_containers = self._get_link_containers(expander)

      #then for each one, get the inner links, or if there are none, add the top-level link
      for div in link_containers:
        inner_links = self._get_inner_links(div)

        if not inner_links:
          name, url = self._get_top_level_link_data(div)
          urls[name] = url

        else:
          for in_link in inner_links:
            name, url = self._get_link_data(in_link)
            urls[name] = url

    return urls

  #gives a list of the top level expander divs
  def _get_expanders(self, selector):
    query = queries["get_expanders"]
    return selector.css(query)

  #gives a list of top level links in an expanded menu panel
  def _get_link_containers(self, expander):
    query = queries["get_link_containers"]
    return expander.css(query)

  #gives a list of inner list of links, and true if any are found
  def _get_inner_links(self, container):
    query = queries["get_inner_links"]
    return container.css(query)

  #given an anchor with the category in a child span, return the 
  #category name and href
  def _get_top_level_link_data(self, container):
    name_query = queries["get_top_level_link_data_name"]
    url_query = queries["get_top_level_link_data_url"]
    name = container.css(name_query).extract()[0]
    url = container.css(url_query).extract()[0]
    return name, url

  #given an anchor with the category name contained within, return the
  #category name and href
  def _get_link_data(self, link):
    name_query = queries["get_link_data_name"]
    url_query = queries["get_link_data_url"]
    name = link.css(name_query).extract()
    url = link.css(url_query).extract()
    return name[0], url[0]