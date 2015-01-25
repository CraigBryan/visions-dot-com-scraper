from visions import selectors
from test import test_urls
import os
import json

class ScrapySelectorTestCase(object):
  """
  A testcase class that runs the test_spider.py crawler. It uses the given url
  and selector for the spider, and compares the result of the spider
  (which it writes to a temporary file) to a given expected result.
  """

  def __init__(self, name, url, css_query, expected):
    self.name = name
    self.url = url
    self.css_query = css_query
    self.expected = expected

  def run_test(self):
    """
    Runs the test using the test_spider and compares the result to the expected
    result. Returns the success of the test and the reason for failure (if failed)
    """
    open("data/temp.json", 'w').close()
    arg_string = "-a start_url='%s' -a query='%s' -o 'data/temp.json' -t 'json'" %(self.url, self.css_query)
    os.system("scrapy runspider test/test_spider.py " + arg_string)

    try:
      result = self._extract_temp_data()
    except Exception as e:
      return False, "An error was raised: %s" %e

    if result == self.expected:
      return True, ""
    else:
      return False, "Unexpected result"

  def _extract_temp_data(self):
    """Gets the extracted test data from a temporary json file"""

    with open("data/temp.json", 'r') as json_file:
      data = json.load(json_file)

    open("data/temp.json", 'w').close()

    return data[0]["result"][0]

def build_test_result(name, state, reason):
  """Prints the test results somewhat nicely"""

  name += "_Test"

  if state:
    return name + " PASSED"
  else:
    return name + " FAILED " + reason

def run_test_set(results, test_set_queries, test_set_urls):
  """
  Runs the tests for the given input and adds the results of the test to a 
  given result list.
    test_set_queries - the CSS selectors to be tested
    test_set_urls - pairs of test urls and expected results for each CSS selector
  """

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
  selectors.CATEGORY_QUERIES["get_header_link_containers"] = \
    selectors.CATEGORY_QUERIES["get_container_links"] + \
    selectors.CATEGORY_QUERIES["get_header_link_containers"][14::]
  
  selectors.CATEGORY_QUERIES["get_inner_links"] = \
    selectors.CATEGORY_QUERIES["get_header_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_inner_links"][3::]

  selectors.CATEGORY_QUERIES["get_top_level_link_data_name"] = \
    selectors.CATEGORY_QUERIES["get_container_links"] + \
    selectors.CATEGORY_QUERIES["get_top_level_link_data_name"][14::]

  selectors.CATEGORY_QUERIES["get_top_level_link_data_url"] = \
    selectors.CATEGORY_QUERIES["get_container_links"] + \
    selectors.CATEGORY_QUERIES["get_top_level_link_data_url"][14::]

  selectors.CATEGORY_QUERIES["get_mid_level_link_data_name"] = \
    selectors.CATEGORY_QUERIES["get_header_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_mid_level_link_data_name"][3::]

  selectors.CATEGORY_QUERIES["get_mid_level_link_data_url"] = \
    selectors.CATEGORY_QUERIES["get_header_link_containers"] + \
    selectors.CATEGORY_QUERIES["get_mid_level_link_data_url"][3::]

  selectors.CATEGORY_QUERIES["get_link_data_name"] = \
    selectors.CATEGORY_QUERIES["get_inner_links"] + \
    selectors.CATEGORY_QUERIES["get_link_data_name"][1::]

  selectors.CATEGORY_QUERIES["get_link_data_url"] = \
    selectors.CATEGORY_QUERIES["get_inner_links"] + \
    selectors.CATEGORY_QUERIES["get_link_data_url"][1::]

  # also, remove the tests for "get_container_links" and "get_header_link_containers"
  # because they are tested as part of other selectors and because the huge
  # strings they return don't encode to json very well
  del selectors.CATEGORY_QUERIES["get_container_links"]
  del selectors.CATEGORY_QUERIES["get_header_link_containers"]

def cleanup():
  """Removes temporary testing files"""
  os.remove('data/temp.json')
  os.remove('data/selector_test.json')
  os.remove('data/selector_test.txt')

def go():
  """
  Called by the runner file. This runs both sets of tests and prints the results.
  """

  results = []

  # Product crawler tests
  run_test_set(results, selectors.PRODUCT_QUERIES, test_urls.PRODUCT_URLS)

  # Category crawler tests
  rearrange_category_queries()
  run_test_set(results, selectors.CATEGORY_QUERIES, test_urls.CATEGORY_URLS)

  for result in results:
    print(result)

  cleanup()