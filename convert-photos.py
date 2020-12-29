#! /usr/bin/env python3

import subprocess
import os
import glob

os.chdir(r'/Users/angelo/Pictures/Lightroom/Allegra Scansetti/2014')
photos = glob.glob('**/*.dng', recursive=True)
quality = str(92)

for photo in photos:
    base_name, ext_name = os.path.splitext(photo)
    print(f'Photo: {photo}')
    cmd = '/usr/local/bin/magick convert -quality '+quality+' "'+base_name+'.dng" "'+base_name+'.jpg"'
    conversion_output = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if conversion_output.returncode == 0:
        if conversion_output.stderr == '':
            print(f'Photo {photo} successfully converted to JPG.')
