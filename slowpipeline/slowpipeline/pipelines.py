# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import time
from scrapy import log
from twisted.python import threadpool
from twisted.internet import threads,reactor

from scrapy.utils.trackref import object_ref


class TrackableObject(object_ref):
    def takes_long_time(self,number,pipeline):
        if pipeline.running:
            time.sleep(15)
        log.msg('took a long to log %s' % number,level=log.ERROR)




class SlowpipelinePipeline(object):
    def __init__(self):
        self.threadpool = threadpool.ThreadPool(3,20)
        self.running = False
        reactor.callWhenRunning(self.start)

    def start(self):
        if not self.running:
            self.threadpool.start()
            reactor.addSystemEventTrigger('during','shutdown',self.finalClose)
            self.running = True

    def finalClose(self):
        self.running = False
        log.msg('final close',level=log.ERROR)
        self.threadpool.stop()

    def process_item(self, domain, item):
        args = dict(item)
        random_numbers = args['random_numbers'].split(',')
        for num in random_numbers:
            #log.msg('dispatching : %s' % num,level=log.ERROR)
            trackable = TrackableObject()
            threads.deferToThreadPool(reactor, self.threadpool, trackable.takes_long_time, num,self)

        return item
