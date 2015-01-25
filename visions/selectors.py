# This file contains all the css selector strings

# CSS selectors for the category crawler (category_spider.py)
CATEGORY_QUERIES = {
  "get_container_links": "#mastermenu-dropdown > li.menulevel-0",
  "get_header_link_containers": "li.menulevel-0 > div.mastermenu-bigsub > div > div",
  "get_inner_links": "div > ul > li > a",
  "get_top_level_link_data_name": "li.menulevel-0 > a > span::text",
  "get_top_level_link_data_url": "li.menulevel-0 > a::attr(href)",
  "get_mid_level_link_data_name": "div > a > span::text",
  "get_mid_level_link_data_url": "div > a::attr(href)",
  "get_link_data_name": "a::text",
  "get_link_data_url": "a::attr(href)"
}

# CSS selectors for the product crawler (product_spider.py)
PRODUCT_QUERIES = { 
  "extract_category": "#ctl00_tdMainPanel > div > div > div > h1::text",
  "extract_detail_link": "a#ctl00_ContentPlaceHolder1_ProductItemListUC1_ctrlProducts_ctl00_ProductItemUC1_lnkProductDetail::attr(href)",
  "extract_title": "span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblProdTitle::text",
  "extract_regular_price": "span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblRegprice > font::text",
  "extract_sale_price": "span#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblSaleprice > font::text",
  "extract_availability_web_only": "#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblWebonly",
  "extract_availability_store_only": "#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_imgInstoreonly",
  "extract_availability_add_to_cart": "#ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lnkAddCart"
}