from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from visions.items import CategoryItem
from scrapy.http import Request

class CategorySpider(BaseSpider):
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
    query = "#mastermenu-dropdown > .menulevel-0 > div.mastermenu-bigsub"
    return selector.css(query)

  #gives a list of top level links in an expanded menu panel
  def _get_link_containers(self, expander):
    query = "div > div > div"
    return expander.css(query)

  #gives a list of inner list of links, and true if any are found
  def _get_inner_links(self, container):
    query = 'div > ul > li > a'
    return container.css(query)

  #given an anchor with the category in a child span, return the 
  #category name and href
  def _get_top_level_link_data(self, container):
    name = container.css('div > a > span::text').extract()
    url = container.css('div > a::attr(href)').extract()
    return name[0], url[0]

  #given an anchor with the category name contained within, return the
  #category name and href
  def _get_link_data(self, link):
    name = link.css('a::text').extract()
    url = link.css('a::attr(href)').extract()
    return name[0], url[0]