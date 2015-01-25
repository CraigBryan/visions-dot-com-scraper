#README
##Craig Bryan

This is my solution to the code challenge presented by 360pi. I learned and used Scrapy to write this solution. 

##Description
This solution contains two main scrapers. The first `category_spider.py` visits the home page of www.visions.ca and gathers the categories and links to each of the category main pages. The second `product_scraper.py` is loaded with the URL's for each category and then selects the first product from each category URL and gets the desired information (title, sale price, regular price, availability).

##Outputs
Each scraper outputs two formats (via Scrapy pipelines). The first is a JSON output. The second is a (more) human-readable format using Scrapy's PprintItemExporter. All outputs are saved to files in the `data` folder.

##Assumptions
Based on the challenge specifications, I had to make two key assumptions. The first was about what counted as a "category", and the other was about the meaning of "availability".

###Category assumption:
I assumed a "category" to be the most specific available link in the "Shop By Department" menu on the www.visions.ca home page. For example, under the "TV & Video" tab, "Televisions" would not count as a category, as I instead used each of the sub-categories (_eg._ "18 - 24" Televisions") as a category. On the other hand, in the same tab, "3D TV Glasses" would count as a category because it had no sub-categories.  

###Availability assumption:
I assumed "Product availability" to mean whether the product was available online, in store, neither, or both.

##Notes:
###Sale price weirdness:
In many cases, my product crawler failed to find a regular price, and instead found only a sale price. When observed, a product that was missing a regular price was actually found to not be on sale, and the website maintainer instead put the regular price where the sale price normally goes and restyled that sale price label to be black (sale prices are red throughout the site). To fix this, I added another pipeline that found any products that were missing a regular price and had a sale price, and manually set the regular price to the claimed sale price (and set the sale price to null).

##Testing:
Coming soon!