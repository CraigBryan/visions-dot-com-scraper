# This file contains all the test urls for each selector to test

# test URLS and responses for the category crawler (category_spider.py)
CATEGORY_URLS = {
  "get_container_links": [], 
  "get_header_link_containers": [],
  "get_inner_links": ['http://www.visions.ca', '<a href="/Catalogue/Category/Default.aspx?categoryId=8&amp;menu=11">18 - 24" Televisions</a>'],
  "get_top_level_link_data_name": ['http://www.visions.ca', 'TV & VIDEO'],
  "get_top_level_link_data_url": ['http://www.visions.ca', '/Catalogue/Category/Default.aspx?categoryId=2&menu=2'],
  "get_mid_level_link_data_name": ['http://www.visions.ca', 'Televisions'],
  "get_mid_level_link_data_url": ['http://www.visions.ca', '/Catalogue/Category/Default.aspx?categoryId=5&menu=9'],
  "get_link_data_name": ['http://www.visions.ca', '18 - 24" Televisions'],
  "get_link_data_url": ['http://www.visions.ca', '/Catalogue/Category/Default.aspx?categoryId=8&menu=11']
}

# test URLS for the product crawler (product_spider.py)
PRODUCT_URLS = {
  "extract_category": ['http://www.visions.ca/Catalogue/Category/ProductResults.aspx?categoryId=8&menu=11', '18 - 24" Televisions'],
  "extract_detail_link": ['http://www.visions.ca/Catalogue/Category/ProductResults.aspx?categoryId=8&menu=11', 'Details.aspx?categoryId=8&productId=22661&sku=PLED1960A'],
  "extract_title": ['http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=8&productId=22661&sku=PLED1960A', 'Proscan 19" 720P 60Hz LED TV With ATSC'],
  "extract_regular_price": ['http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=8&productId=22661&sku=PLED1960A', '$139.99'],
  "extract_sale_price": ['http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=8&productId=22661&sku=PLED1960A', '$98.00'],
  "extract_availability_web_only": ['http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=668&productId=26919&sku=LIFT70OB', '<span id="ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lblWebonly">Web Available Only</span>'],
  "extract_availability_store_only": ['http://www.visions.ca/catalogue/category/Details.aspx?categoryId=433&productId=6594&sku=HD1H', '<img id="ctl00_ContentPlaceHolder1_ctrlProdDetailUC_imgInstoreonly" src="../../Images/ProductList/in_store_only.gif" border="0">'],
  "extract_availability_add_to_cart": ['http://www.visions.ca/Catalogue/Category/Details.aspx?categoryId=8&productId=22661&sku=PLED1960A', '<a id="ctl00_ContentPlaceHolder1_ctrlProdDetailUC_lnkAddCart" class="addToCart" href="javascript:addToCart(\'22661\');" style="min-width:140px;">ADD TO CART</a>']
}