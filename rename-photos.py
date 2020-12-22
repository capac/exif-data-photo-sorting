#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir('/Users/angelo/Pictures/Lightroom/Dino')

photos = glob.glob('**/*.*', recursive=True)
print(len(photos))

for photo in photos:
    # subprocess.run(['exiftool', '-d', '%Y%m%d_%H%M%S%%-c.%%e', '-testname<${Date;}', photo])
    date_time_all = subprocess.run('exiftool -s -f -time:all '+photo+' | awk \'{print $3 $4}\'',
                                   shell=True, capture_output=True)
    print(str(date_time_all.stdout))
    break
    # date_time = date_time_all.split(':')[1]
    # print(date_time_all)
