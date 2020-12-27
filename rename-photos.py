#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir('/Users/angelo/Pictures/Lightroom/Angelo\'s Pics/')

photos = sorted(glob.glob('**/*.*', recursive=True), key=os.path.getctime, reverse=True)
print(f'Number of photos: {len(photos)}\n')
datetime_tags = ['DateTimeOriginal', 'CreateDate', 'DateCreated',
                 'Date', 'ModifyDate', 'FileModifyDate']

for photo in photos:
    photo_name, photo_ext = os.path.splitext(photo)
    for tag in datetime_tags:
        photo_run_output = subprocess.run('exiftool -s -f \'-filename<'+tag+'\'\
        -d %Y-%m-%d_%H-%M-%S%%-c.%%e '+'"'+photo+'"', shell=True, capture_output=True, text=True)
        if photo_run_output.returncode == 0:
            new_photo = f'{photo_name}{photo_ext.lower()}'
            print(new_photo)
            os.rename(photo, new_photo)
            break
    else:
        new_photo = f'{photo_name[0:8]}{photo_ext.lower()}'
        print(new_photo)
        os.rename(photo, new_photo)
        break
