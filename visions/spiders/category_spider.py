from scrapy.spider import Spider
from scrapy.selector import Selector
from visions.items import CategoryItem
from visions.selectors import CATEGORY_QUERIES as queries

class CategorySpider(Spider):
    """
    This crawler pulls the category data and category-specific links from the main
    menu of the visions.ca website. Since it is looking for the most specific 
    category, it employs a triple level search and backtrack method. It first finds
    all top-level categories (eg. Television), then searches those for sub-categories. 
    If no sub-categories are found, it backtracks and adds the top-level category 
    to the categories to be returned. If sub-categories are found, it searches 
    further within each sub-category element in the same manner, finding 
    sub-sub-categories and backtracking when necessary. 
    """
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
        """
        Grabs the top-level categories, and begins the search for sublinks.
        """
        urls = {}

        container_links = self._get_container_links(selector)

        for link in container_links:
            urls.update(self._get_sublinks(link))

        return urls

    def _get_sublinks(self, selector):
        """
        Searches for sub-categories and backtracks if not found. Begins the search
        for sub-sub-categories when a sub-category is found.
        """
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
        """
        Searches for sub-sub-categories and backtracks if not found.
        """
        inner_links = self._get_inner_links(selector)
        urls = {}
        if inner_links:
            for in_link in inner_links:
                name, url = self._get_link_data(in_link)
                urls[name] = url

        else:
            name, url = self._get_mid_level_link_data(selector)
            urls[name] = url

        return urls

    def _get_container_links(self, selector):
        """Gives a list of the top level category selectors"""
        query = queries["get_container_links"]
        return selector.css(query)

    def _get_header_link_containers(self, selector):
        """Gives a list of sub-category selectors in an expanded menu panel"""
        query = queries["get_header_link_containers"]
        return selector.css(query)

    def _get_inner_links(self, selector):
        """Gives a list of sub-sub-category selectors in an expanded menu panel"""
        query = queries["get_inner_links"]
        return selector.css(query)

    def _get_top_level_link_data(self, container):
        """Pulls name and url data for a top-level category"""
        name_query = queries["get_top_level_link_data_name"]
        url_query = queries["get_top_level_link_data_url"]
        name = container.css(name_query).extract()[0]
        url = container.css(url_query).extract()[0]
        return name, url

    def _get_mid_level_link_data(self, container):
        """Pulls name and url data for a sub-category"""
        name_query = queries["get_mid_level_link_data_name"]
        url_query = queries["get_mid_level_link_data_url"]
        name = container.css(name_query).extract()[0]
        url = container.css(url_query).extract()[0]
        return name, url

    def _get_link_data(self, link):
        """Pulls name and url data for a sub-sub-category"""
        name_query = queries["get_link_data_name"]
        url_query = queries["get_link_data_url"]
        name = link.css(name_query).extract()
        url = link.css(url_query).extract()
        return name[0], url[0]