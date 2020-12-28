#! /usr/bin/env python3

import os
import glob
import subprocess

os.chdir(r'/Users/angelo/Pictures/Lightroom/Allegra Scansetti/2013')

photos = sorted(glob.glob('**/*.*', recursive=True), key=os.path.getctime, reverse=True)
print(f'Number of photos: {len(photos)}\n')
datetime_tags = ['DateTimeOriginal', 'CreateDate', 'DateCreated',
                 'Date', 'ModifyDate', 'FileModifyDate']

for photo in photos:
    photo_name, photo_ext = os.path.splitext(photo)
    for tag in datetime_tags:
        string = 'exiftool -s -f \'-filename<'+tag+'\' -d %Y-%m-%d_%H-%M-%S%%-c.%%e '+'"'+photo+'"'
        photo_run_output = subprocess.run(string, shell=True, capture_output=True, text=True)
        print(photo_run_output)
        if photo_run_output.returncode == 0:
            if photo_run_output.stderr == '':
                print(photo_name)
                break
    else:
        new_photo = f'{photo_name[0:8]}{photo_ext.lower()}'
        os.rename(photo, new_photo)
        print(photo_name)
        break

new_photos = sorted(glob.glob('**/*.*', recursive=True))
for new_photo in new_photos:
    new_photo_name, new_photo_ext = os.path.splitext(new_photo)
    new_photo_with_lower_case_ext = f'{new_photo_name}{new_photo_ext.lower()}'
    os.rename(new_photo, new_photo_with_lower_case_ext)
    print(new_photo_with_lower_case_ext)
