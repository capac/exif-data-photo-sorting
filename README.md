# EXIF data photo sorting

_Python script for photograph sorting based on EXIF data_

This effort is based on a [Stack Overflow thread on sorting photos](https://stackoverflow.com/questions/32062159/how-retrieve-the-creation-date-of-photos-with-a-script) based off of the creation date as recorded in the EXIF data. It derives from the [Bash script posted toward the bottom of the thread](https://stackoverflow.com/a/56896194) that I've used as a template to convert the file in Python.

The script makes use of [ExifTool](https://exiftool.org/) to edit the timestamp metadata to rename the file. It cycles through a number of different date and time tags, specifically 'DateTimeOriginal', 'CreateDate', 'DateCreated', 'Date', 'ModifyDate', 'FileModifyDate', and if they aren't present in the file, the file name remains untouched.
