# runner python script
import sys
import os

arg_string = "\n  'test' - runs tests \n  'run' - runs crawlers"

if len(sys.argv) < 2:
  print("Requires an argument:" + arg_string)
  exit()

if sys.argv[1] == 'test':
  from test import tests
  tests.go()
elif sys.argv[1] == 'run':
  os.system("scrapy crawl category")
  os.system("scrapy crawl product")
else:
  print("Unknown argument: '" + sys.argv[1] + "'")
  print("Use one of the following arguments:" + arg_string)