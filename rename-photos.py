#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir('/Users/angelo/Pictures/Lightroom/Mark\'s Pics')

photos = sorted(glob.glob('**/*.*', recursive=True), key=os.path.getctime, reverse=True)
print(f'Number of photos: {len(photos)}\n')
datetime_tags = ['DateTimeOriginal', 'CreateDate', 'DateCreated',
                 'Date', 'ModifyDate', 'FileModifyDate']

for photo in photos:
    photo_name, photo_ext = os.path.splitext(photo)
    for tag in datetime_tags:
        photo_run_output = subprocess.run('exiftool -s -f -time:'+tag+' '+'"'+photo+'"',
                                          shell=True, capture_output=True, text=True)
        if photo_run_output.stdout.split(':')[1] != ' -\n':
            photo_date_time = photo_run_output.stdout.split(': ')[1]
            date_time = photo_date_time.split(' ')
            date_time[1] = date_time[1][0:8]
            new_dt_list = []
            for dt in date_time:
                new_dt_list.append('-'.join(dt.split(':')))
            new_dt = '_'.join(new_dt_list)
            print(f'Photo: {photo}, tag: {tag}, new name: {new_dt}{photo_ext.lower()}\n')
            break
    else:
        print(photo.split('-')[0]+'_NO-CHANGE-IN-FILE-NAME\n')
