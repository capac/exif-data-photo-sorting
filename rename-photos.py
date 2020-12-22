#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir('/Users/angelo/Pictures/Lightroom/Angelo\'s Pics')

photos = glob.glob('**/*.*', recursive=True)
print(len(photos))
time_tags = ['DateTimeOriginal', 'CreateDate', 'DateCreated', 'Date']
counter = 0
for photo in photos:
    # subprocess.run(['exiftool', '-d', '%Y%m%d_%H%M%S%%-c.%%e', '-testname<${Date;}', photo])
    date_time_all = subprocess.run('exiftool -s -f -time:all '+photo, shell=True, capture_output=True, text=True)
    # date_time_all = subprocess.run('exiftool -s -f -time:all '+photo+' | awk \'{print $3, $4}\'',
    #                                shell=True, capture_output=True, text=True)
    print(str(date_time_all.stdout))
    counter += 1
    if counter % 3 == 0:
        break
    # date_time = date_time_all.split(':')[1]
    # print(date_time_all)
