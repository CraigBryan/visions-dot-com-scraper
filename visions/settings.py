# -*- coding: utf-8 -*-

# Scrapy settings for visions project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'visions'

SPIDER_MODULES = ['visions.spiders']
NEWSPIDER_MODULE = 'visions.spiders'

ITEM_PIPELINES = { 'visions.pipelines.VisionsValidatorPipeline' :99,
                   'visions.pipelines.VisionsJsonPipeline': 100,
                   'visions.pipelines.VisionsPrettyPipeline': 101}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'visions (+http://www.yourdomain.com)'
