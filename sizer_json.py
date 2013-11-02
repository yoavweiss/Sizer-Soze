#!/usr/bin/env python

import sys
import os
from sizer import sizer
import json
import requests

if __name__ == "__main__":
    # Check input
    if len(sys.argv) <= 4:
        print >> sys.stderr, "Usage:", sys.argv[0], "<URL> <viewport> <ignore display:none> <postback_url>"
        quit()
    url = sys.argv[1]
    viewport = sys.argv[2]
    ignore = (sys.argv[3] != "0")
    postback = sys.argv[4]

    result = json.dumps(sizer(url, viewport, ignore, False))
    if not postback.startswith("http"):
        postback = "http://" + postback
    
    requests.post(postback, data=result)
    print result
    
