#!/usr/bin/env python
from slugify import slugify
import settings
import sys
import os

if len(sys.argv) <= 1:
    print >> sys.stderr, "Usage:", sys.argv[0], "<URL>"
    quit()
url = sys.argv[1]

slugged_dir = os.path.join(settings.output_dir, slugify(url))

print slugged_dir
