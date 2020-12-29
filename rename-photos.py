#! /usr/bin/env python3

import os
import glob
import subprocess
import logging

logging.basicConfig(filename='rename.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

os.chdir(r'/Users/angelo/Pictures/Lightroom/Allegra Scansetti/2013')

photos = sorted(glob.glob('**/*.*', recursive=True), reverse=True)

print(f'Number of photos: {len(photos)}\n')
# choice of date/time tags to check for photo creation date, best reasonable
# choices, however far from being the optimal solution in some cases...
datetime_tags = ['DateTimeOriginal', 'CreateDate', 'DateCreated',
                 'Date', 'ModifyDate', 'FileModifyDate']

for photo in photos:
    photo_name, photo_ext = os.path.splitext(photo)
    # go through datetime tags to rename file according to first available tag
    for tag in datetime_tags:
        cmd = 'exiftool -s -F -f \'-filename<'+tag+'\' -d %Y-%m-%d_%H-%M-%S%%-c.%%e '+'\"'+photo+'\"'
        photo_run_output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        logging.debug(photo_run_output)
        # use returncode and stderr to determine
        # if file has been properly renamed
        if photo_run_output.returncode == 0:
            if photo_run_output.stderr == '':
                print(photo_name)
                break
    # if none of the tags are found, use
    # then first 8 characters to rename file
    else:
        new_photo = f'{photo_name[0:8]}{photo_ext.lower()}'
        os.rename(photo, new_photo)
        print(photo_name)
        break

# make sure file extension is lowercase, for some camera
# photos are saved with upper case extensions.
new_photos = sorted(glob.glob('**/*.*', recursive=True))
for new_photo in new_photos:
    new_photo_name, new_photo_ext = os.path.splitext(new_photo)
    new_photo_with_lower_case_ext = f'{new_photo_name}{new_photo_ext.lower()}'
    os.rename(new_photo, new_photo_with_lower_case_ext)
    print(new_photo_with_lower_case_ext)
