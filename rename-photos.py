#! /usr/bin/env python3

import os
import glob

os.chdir(r'/Users/angelo/Pictures/Lightroom')

photos = glob.glob(r'**/*.[JjPpe?E?Gg]', recursive=True)
print(photos)
