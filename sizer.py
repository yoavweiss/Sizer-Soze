#!/usr/bin/env python

from slugify import slugify
import sys
import os
from subprocess import Popen, PIPE
from downloadr import downloadFiles
import resizeBenefits
import settings
from threading import Thread
from multiprocessing import Process

class SizerProcess(Process):
    def __init__(self, queue):
        super(SizerProcess, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            print "Started"
            url,filename = self.queue.get()
            print "Got"
            sizer(url, filename)
            self.queue.task_done()

def col(value, length=16):
    return str(value).ljust(length + 1)
def sizer(url, ignore_invisibles):
    # Prepare the output directory
    if not url.startswith("http"):
        url = "http://" + url
    slugged_url = slugify(url)
    slugged_dir = os.path.join(settings.output_dir, slugged_url)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(slugged_dir):
        os.makedirs(slugged_dir)

    print col("url", len(url)), col("viewport"), col("image_data"), col("lossless_savings"), col("lossy_savings"), col("resize_savings")
    for viewport in settings.viewports:
        image_urls = []
        image_results = []
        phantom = Popen([os.path.join(current_dir, "getImageDimensions.js"), url,  str(viewport)],
                        stdout = PIPE);
        container = image_urls
        for line in phantom.stdout.xreadlines():
            # Ignore data URIs

            if line.startswith("---"):
                downloadFiles(image_urls, slugged_dir)
                container = image_results
                continue
            if not line.startswith("http"):
                continue

            container.append(line)

        # Here the process should be dead, and all files should be downloaded
        benefits = resizeBenefits.getBenefits(image_results, slugged_dir, ignore_invisibles)
        benefits_file = open(os.path.join(slugged_dir, "result_" + str(viewport) + ".txt"), "wt")
        image_data = 0
        optimize_savings = 0
        lossy_optimize_savings = 0
        resize_savings = 0
        for benefit in benefits:
            print >>benefits_file, benefit[0],
            print >>benefits_file, "Original_size:",
            print >>benefits_file, benefit[1],
            print >>benefits_file, "optimize_savings:",
            print >>benefits_file, benefit[2],
            print >>benefits_file, benefit[3],
            print >>benefits_file, benefit[4],
            print >>benefits_file, benefit[5]
            image_data += benefit[1]
            optimize_savings += benefit[2]
            lossy_optimize_savings += benefit[3]
            resize_savings += benefit[5]
        benefits_file.close()

        print col(url, len(url)), col(viewport), col(image_data), col(optimize_savings), col(lossy_optimize_savings), col(resize_savings)
    return 

if __name__ == "__main__":
    # Check input
    if len(sys.argv) <= 1:
        print >> sys.stderr, "Usage:", sys.argv[0], "<URL> <ignore display:none>"
        quit()
    url = sys.argv[1]
    if len(sys.argv) > 2:
        ignore = bool(sys.argv[2])
    else:
        ignore = False
    sizer(url, ignore)
