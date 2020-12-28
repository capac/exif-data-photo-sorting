#! /usr/bin/env python3

import subprocess
import os
import glob

os.chdir(r'/Users/angelo/Pictures/Lightroom/Allegra Scansetti/2011')
photos = glob.glob('**/*.dng', recursive=True)

quality = 96

for photo in photos:
    base_name, ext_name = os.path.split(photo)
    cmd = '/usr/local/bin/magick convert -quality '+quality+' "'+base_name+'.dng" "'+base_name+'.jpg"'
    conversion_output = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if conversion_output.returncode == 0:
        if conversion_output.stderr == '':
            break
