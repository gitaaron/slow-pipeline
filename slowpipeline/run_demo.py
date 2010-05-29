#!/usr/bin/env python

import sys,os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'slowpipeline.settings')

from twisted.internet import reactor

from slowpipeline.standalone import crawling_session,start_test_site


if __name__=='__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        port = start_test_site()
        print 'Test server running on http://localhost/%d/ - hit Ctr-C to finish.' % port.getHost().port
        reactor.run()
    else:
        if not crawling_session.wasrun:
            crawling_session.run()
