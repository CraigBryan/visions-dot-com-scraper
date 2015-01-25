from visions import selectors
from test import test_urls
import os
import json

class ScrapySelectorTestCase(object):
  
  def __init__(self, name, url, css_query, expected):
    self.name = name
    self.url = url
    self.css_query = css_query
    self.expected = expected

  def run_test(self):
    arg_string = "-a start_url='%s' -a query='%s' -o 'data/temp.json' -t 'json'" %(self.url, self.css_query)
    os.system("scrapy runspider test/test_spider.py " + arg_string)

    result = self._extract_temp_data()

    if result == self.expected:
      return True, ""
    else:
      return False, "Unexpected result"

  def _extract_temp_data(self):
    with open("data/temp.json", 'r') as json_file:
      data = json.load(json_file)

    open("data/temp.json", 'w').close()

    return data[0]["result"][0]

def build_test_result(name, state, reason):
  name += "_Test"

  if state:
    return name + " PASSED"
  else:
    return name + " FAILED " + reason

def run_test_set(results, test_set_queries, test_set_urls):
  for name, css_query in test_set_queries.items():
    try:
      test_url = test_set_urls[name][0]
      expected = test_set_urls[name][1]

    except IndexError:
      state = False
      reason = "Missing test URL"

    else:
      test = ScrapySelectorTestCase(name + "TEST", test_url, css_query, expected)
      state, reason = test.run_test()

    results.append(build_test_result(name, state, reason))

# This is a hack because of the way the selectors are used sequentially in
# the category spider. This builds the selectors into selectors that can be 
# used atomically in the tests
def rearrange_category_queries():
  selectors.CATEGORY_QUERIES["get_link_containers"] = \
    selectors.CATEGORY_QUERIES["get_expanders"] + \
    selectors.CATEGORY_QUERIES["get_link_containers"][3::]
  
  selectors.CATEGORY_QUERIES["get_inner_links"] = \
    selectors.CATEGORY_QUERIES["get_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_inner_links"][3::]

  selectors.CATEGORY_QUERIES["get_top_level_link_data_name"] = \
    selectors.CATEGORY_QUERIES["get_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_top_level_link_data_name"][3::]

  selectors.CATEGORY_QUERIES["get_top_level_link_data_url"] = \
    selectors.CATEGORY_QUERIES["get_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_top_level_link_data_url"][3::]

  selectors.CATEGORY_QUERIES["get_link_data_name"] = \
    selectors.CATEGORY_QUERIES["get_inner_links"] + \
    selectors.CATEGORY_QUERIES["get_link_data_name"][1::]

  selectors.CATEGORY_QUERIES["get_link_data_url"] = \
    selectors.CATEGORY_QUERIES["get_inner_links"] + \
    selectors.CATEGORY_QUERIES["get_link_data_url"][1::]

  # also, remove both the tests for "get_expanders" and "get_link_containers"
  # because they are tested as part of other selectors and because the huge
  # strings they return don't decode and encode to json very well
  del selectors.CATEGORY_QUERIES["get_expanders"]
  del selectors.CATEGORY_QUERIES["get_link_containers"]

def cleanup():
  os.remove('data/temp.json')
  os.remove('data/selector_test.json')
  os.remove('data/selector_test.txt')

def go():
  results = []

  # Product crawler tests
  run_test_set(results, selectors.PRODUCT_QUERIES, test_urls.PRODUCT_URLS)

  # Category crawler tests
  rearrange_category_queries()
  run_test_set(results, selectors.CATEGORY_QUERIES, test_urls.CATEGORY_URLS)

  for result in results:
    print(result)

  cleanup()