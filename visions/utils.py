# utility functions that did not belong elsewhere
import json

from visions.errors import MissingCategoryFileError

def base_url():
    return "http://www.visions.ca"

def base_detail_url():
    return base_url() + "/Catalogue/Category/"

def read_category_urls():
    try:
        category_file = open('data/category.json', 'r')    
    except IOError:
        raise MissingCategoryFileError("Run 'scrapy crawl category' \
            to generate a category file") 

    categories_data = json.load(category_file)
    categories = [base_url() + entry['url'] for entry in categories_data]
    return categories