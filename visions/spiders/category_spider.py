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

    container_links = self._get_container_links(selector)

    for link in container_links:
      urls.update(self._get_sublinks(link))

    return urls

  def _get_sublinks(self, selector):
    header_links = self._get_header_link_containers(selector)
    urls = {}
    if header_links:
      for h_link in header_links:
        urls.update(self._get_lowest_level_links(h_link))

    else:
      name, url = self._get_top_level_link_data(selector)
      urls[name] = url

    return urls

  def _get_lowest_level_links(self, selector):
    inner_links = self._get_inner_links(selector)
    urls = {}
    print(inner_links.extract())
    if inner_links:
      for in_link in inner_links:
        name, url = self._get_link_data(in_link)
        urls[name] = url

    else:
      name, url = self._get_mid_level_link_data(selector)
      urls[name] = url

    return urls

  #gives a list of the top level links
  def _get_container_links(self, selector):
    query = queries["get_container_links"]
    return selector.css(query)

  #gives a list of top level links in an expanded menu panel
  def _get_header_link_containers(self, selector):
    query = queries["get_header_link_containers"]
    return selector.css(query)

  #gives a list of inner list of links, and true if any are found
  def _get_inner_links(self, selector):
    query = queries["get_inner_links"]
    return selector.css(query)

  #TODO
  def _get_top_level_link_data(self, container):
    name_query = queries["get_top_level_link_data_name"]
    url_query = queries["get_top_level_link_data_url"]
    name = container.css(name_query).extract()[0]
    url = container.css(url_query).extract()[0]
    return name, url

  #given an anchor with the category in a child span, return the 
  #category name and href
  def _get_mid_level_link_data(self, container):
    name_query = queries["get_mid_level_link_data_name"]
    url_query = queries["get_mid_level_link_data_url"]
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