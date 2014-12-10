# -*- coding: utf-8 -*-

# Scrapy settings for activities project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'activities'

SPIDER_MODULES = ['activities.spiders']
NEWSPIDER_MODULE = 'activities.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'activities (+http://www.yourdomain.com)'
#CLOSESPIDER_PAGECOUNT = 1100
#CLOSESPIDER_TIMEOUT = 1000
DOWNLOAD_DELAY = .25

#RETRY_ENABLED = False
#COOKIES_ENABLED = False
#ROBOTSTXT_OBEY = True



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
 
