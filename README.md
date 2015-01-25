#README
##Craig Bryan

This is my solution to the code challenge presented by 360pi. I learned and used Scrapy to write this solution. 

##Running Instructions
Use the running script in the root directory.

`python run.py test` runs the tests
`python run.py run` runs the scrapers

##Description
This solution contains two main scrapers. The first `category_spider.py` visits the home page of [www.visions.ca](http://www.visions.ca) and gathers the categories and links to each of the category main pages. The second `product_scraper.py` is loaded with the URL's for each category and then selects the first product from each category URL and gets the desired information (title, sale price, regular price, availability).

##Outputs
Each scraper outputs two formats (via Scrapy pipelines). The first is a JSON output. The second is a (more) human-readable format using Scrapy's PprintItemExporter. All outputs are saved to files in the `data` folder.

##Assumptions
Based on the challenge specifications, I had to make two key assumptions. The first was about what counted as a _"category"_, and the other was about the meaning of _"availability"_.

###Category assumption:
I assumed a _"category"_ to be the most specific available link in the _"Shop By Department"_ menu on the [www.visions.ca](http://www.visions.ca) home page. For example, under the _"TV & Video"_ tab, _"Televisions"_ would not count as a category, as I instead used each of the sub-categories (_eg._ _"18 - 24" Televisions"_) as a category. On the other hand, in the same tab, _"3D TV Glasses"_ would count as a category because it had no sub-categories.  

###Availability assumption:
I assumed _"Product availability"_ to mean whether the product was available online, in store, neither, or both.

##Notes
###Sale price weirdness:
In many cases, my product crawler failed to find a regular price, and instead found only a sale price. When observed, a product that was missing a regular price was actually found to not be on sale, and the website maintainer instead put the regular price where the sale price normally goes and restyled that sale price label to be black (sale prices are red throughout the site). To fix this, I added another pipeline that found any products that were missing a regular price and had a sale price, and manually set the regular price to the claimed sale price (and set the sale price to null).

##Testing:
I was unsure how to go about testing my scraper in a reliable manner. Scrapy contracts seemed a weak (either that or I don't understand them fully), and I don't know the best practices to test scrapers. 

I decided that the most likely reason for this code to break is that the [www.visions.ca](http://www.visions.ca) would change, and therefore my selectors would stop working. So, I wrote another spider `test_spider.py` and I'm using it to independently test each css selector I used against a known live page. That way, if the tests start failing, I'll be alerted that the site has changed somehow. I also had to add a supporting module `tests.py` to run tests on this new spider. Unfortunately, the tests may also themselves break for innoculous website changes. For example, if the product I'm using to test my 'sale price' selector is no longer on sale, that test will fail, even if the selector still works fine.