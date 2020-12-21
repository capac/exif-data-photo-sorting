#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir('/Users/angelo/Pictures/Lightroom/Dino')

photos = glob.glob('**/*.*', recursive=True)
print(len(photos))

(subprocess.call(['exiftool', '-d', '%Y%m%d_%H%M%S%%-c.%%e', '-testname<${Date;}', '.']))
