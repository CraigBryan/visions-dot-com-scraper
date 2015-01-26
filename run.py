"""
The main runner file. This is to be run from the command line. It takes
one command argument.
args:
    test - runs the CSS selector tests
    run - runs the two scrapers, in the correct order
"""
import sys
import os

arg_string = "\n  'test' - runs tests \n  'run' - runs crawlers"

if len(sys.argv) < 2:
    print("Requires an argument:" + arg_string)
    exit()

if sys.argv[1] == 'test':

    #create the data directory
    if not os.path.exists("data"):
        os.makedirs("data")

    from test import tests
    tests.go()

elif sys.argv[1] == 'run':

    #create the data directory
    if not os.path.exists("data"):
        os.makedirs("data")

    os.system("scrapy crawl category")
    os.system("scrapy crawl product")
    
else:
    print("Unknown argument: '" + sys.argv[1] + "'")
    print("Use one of the following arguments:" + arg_string)