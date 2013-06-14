#!/usr/bin/python

import os
import sys
from urllib2 import HTTPError, URLError, urlopen
from slugify import slugify
import hashlib
from Queue import Queue
from threading import Thread

def resourceSlug(url, dir):
    hash = hashlib.md5()
    hash.update(url)
    slug = hash.hexdigest()[:2] + slugify(url)[:128]
    return os.path.join(dir, slug)

class downloaderThread(Thread):
    def __init__(self, queue, dir):
        Thread.__init__(self)
        self.queue = queue
        self.dir = dir

    def downloadFile(self, url):
        url = url.strip()
        try: 
            filename = resourceSlug(url, self.dir)
            if os.path.exists(filename):
                return

            f = urlopen(url)
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

