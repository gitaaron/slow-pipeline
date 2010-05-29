import os,random
from scrapy import log
from scrapy.core.manager import scrapymanager


from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web import static

demo_datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data')


from slowpipeline.spiders.test import TestSpider


class DemoPage(Resource):
    def __init__(self,counter):
        Resource.__init__(self)
        self.counter = counter

    def render_GET(self,request):
        next_page = self.counter+1
        random_numbers = ','.join([str(random.randint(0,10000)) for i in xrange(0,100)])
        return '<html><body><a href="/item/%s">Next page</a><div id="numbers">%s</div></body></html>' % (next_page,random_numbers)

class DemoPageGetter(Resource):
    def getChild(self,name,request):
        return DemoPage(int(name))

class DemoIndex(Resource):
    isLeaf = True
    def render_GET(self,request):
        return '<html><body><a href="/item/1">1</a></body></html>'

def start_test_site(port_no=0):
    root = Resource()
    root.putChild('', DemoIndex())
    root.putChild('item',DemoPageGetter())
    factory = Site(root)
    port = reactor.listenTCP(port_no,factory, interface='127.0.0.1')
    return port

class CrawlingSession(object):
    def __init__(self):
        self.domain = "slowpipeline.org"
        self.wasrun = False
        self.spider = TestSpider()
        self.port = None
        self.portno = None

    def run(self):
        print 'all runned up'
        if not self.portno:
            self.port = start_test_site()
            self.portno = self.port.getHost().port
        else:
            self.port = start_test_site(self.portno)

        self.spider.start_urls = [self.geturl('/'),]
        scrapymanager.configure()
        scrapymanager.runonce(self.spider)

    def geturl(self,path):
        return 'http://localhost:%s%s' % (self.portno,path)

crawling_session = CrawlingSession()
