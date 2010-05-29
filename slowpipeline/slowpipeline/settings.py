# Scrapy settings for slowpipeline project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'slowpipeline'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['slowpipeline.spiders']
NEWSPIDER_MODULE = 'slowpipeline.spiders'
DEFAULT_ITEM_CLASS = 'slowpipeline.items.TestItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DOWNLOAD_DELAY = 1.0
ITEM_PIPELINES = ['slowpipeline.pipelines.SlowpipelinePipeline']
TRACK_REFS = True

LOG_LEVEL = 'WARNING'
