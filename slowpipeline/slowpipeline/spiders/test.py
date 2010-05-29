from scrapy.contrib.spiders import CrawlSpider

from slowpipeline.items import TestItem

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from lxml.html import fromstring
from lxml import etree

from scrapy import log

class TestSpider(CrawlSpider):
    def __init__(self):
        super(TestSpider, self).__init__()

    domain_name = "slowpipeline.org"
    extra_domain_names = ["localhost"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('gallery'))),
        Rule(SgmlLinkExtractor(allow=('item')),callback='parse_item',follow=True),
    )

    def parse_item(self,response):
        doc = fromstring(response.body)
        number_path = etree.XPath('/html/body/div[@id="numbers"]/text()')
        numbers = number_path(doc)[0]
        log.msg('parse_item : %s' % numbers)
        return TestItem(random_numbers=numbers)

SPIDER = TestSpider()
