#!/usr/bin/python

import os
import sys
from urllib2 import HTTPError, URLError, urlopen, Request
from slugify import slugify
import hashlib
from Queue import Queue
from threading import Thread

def resourceSlug(url, dir):
    hash = hashlib.md5()
    hash.update(url)
    digest = hash.hexdigest()[:2]
    slug = slugify(url)[:128]
    return (os.path.join(dir, digest), os.path.join(dir, digest, slug))

class downloaderThread(Thread):
    def __init__(self, queue, dir):
        Thread.__init__(self)
        self.queue = queue
        self.dir = dir

    def downloadFile(self, url):
        url = url.strip()
        try: 
            filedir, filename = resourceSlug(url, self.dir)
            if os.path.exists(filename):
                return
            if not os.path.exists(filedir):
                os.mkdir(filedir)

            headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36' }
            f = urlopen(Request(url, None, headers))
            buffer = f.read()
            with open(filename, "wb") as local_file:
                local_file.write(buffer)
                local_file.close()
        except HTTPError, e:
            print >>sys.stderr, "HTTPError:", e.code, url
        except URLError, e:
            print >>sys.stderr, "URLError:", url
            #print >>sys.stderr, "URLError:", e.reason, url

    def run(self):
        while True:
            url = self.queue.get()
            self.downloadFile(url)
            self.queue.task_done()

def downloadFiles(urls, dir):
    queue = Queue()
    for i in range(64):
        t = downloaderThread(queue, dir)
        t.setDaemon(True)
        t.start()

    for url in urls:
        queue.put(url)

    queue.join()

