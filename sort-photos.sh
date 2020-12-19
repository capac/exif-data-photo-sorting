#! /bin/bash
# This script is used to sort photos. It uses the EXIFTOOL to
#  1st attempt to extract the photo's "CreateDate". If it is
#  invalid, then the file name is checked to see if it begins
#  with "YYYYMMDD", which is also checked for validity. If the
#  prior two checks fail, then the photo's "FileModifyDate" is
#  used but can be inaccurate.
# If a valid creation date is found and the file name is NOT
#  date-encoded, then the file is renamed with a "YYYYMMDD-"
#  prefix.
#=======================================================================
#   Revision index:
#   2019-0704:  KSV - Created and tested.
#=======================================================================

DEBUG=0     # Debugging
DRYRUN=0    # Do everything but move the files
NOTE=""     # Notes

# ANSI COLORS
CRE="$(echo -e '\r\033[K')"
RED="$(echo -e '\033[1;31m')"
GRN="$(echo -e '\033[1;32m')"
YEL="$(echo -e '\033[1;33m')"
BLU="$(echo -e '\033[1;34m')"
MAG="$(echo -e '\033[1;35m')"
CYN="$(echo -e '\033[1;36m')"
WHT="$(echo -e '\033[1;37m')"
NML="$(echo -e '\033[0;39m')"

#=======================================================================
# Functions
#=======================================================================
# Enter with: YEAR, MONTH and DAY
# Returns: 0=invalid date, 1=valid date
# EX: IsValidDate $YEAR $MONTH $DAY
IsValidDate() {
  #echo "Parm: Y=$1,${#1} M=$2,${#2} D=$3,${#3}" >/dev/stderr
  if ([ "$1" -ge "1950" ] && [ "$1" -le "2050" ]) || \
  ([ "$2" -ge "01" ] && [ "$2" -le "12" ]) || \
  ([ "$3" -ge "01" ] && [ "$3" -le "31" ]) ; then
    echo "1"    # valid date
  else
    echo "0"    # invalid date
  fi
}

# Dump debugging info
# EX: $(DumpDebug $FN $FILE $EXT $FN_WD $DATE $YEAR $MONTH $DAY "$NOTE")
DumpDebug() {
  #echo "1=${#FN}, 2=${#FILE}, 3=${#EXT}, 4=${#FN_WD}, 5=${#DATE}, 6=${#YEAR}, 7=${#MONTH}, 8=${#DAY}, 9=${#NOTE}" >/dev/stderr
  echo "================================"
  echo "FN        = $1"
  echo "FILE      = $2"
  echo "EXT       = $3"
  echo "FN_WD     = $4"
  echo "DATE      = $5"
  echo "YEAR      = $6"
  echo "MONTH     = $7"
  echo "DAY       = $8"
  echo "ValidDate = $(IsValidDate $6 $7 $8)"
  echo "NOTE      = $9"
  echo "================================"
}

#=======================================================================
# Script starts here
#=======================================================================
# Use exiftool to find video and photos
#exiftool -filename *.[JjGg][PpIi][GgFf] *.[Jj][Pp][Ee][Gg] *.[Mm][PpOo][Gg4Vv] 2>/dev/null | awk {'print $4'} | \
find . -maxdepth 1 -type f -iname "*.[JjGg][PpIi][GgFf]" -or \
-iname "*.[Jj][Pp][Ee][Gg]" -or \
-iname "*.[Mm][PpOo][Gg4Vv]" | \
while read FN ; do
  FN=$(basename $FN)                                # strip the leading "./"
  if [ -e $FN ] && [ ${#FN} != 0 ] ; then           # be sure the file exists!
    EXT=${FN##*.}                                   # extract the extension
    FILE=${FN%.*}                                   # extract the base file name

    # First attempt to see if there is a valid date prefix in the file name.
    YEAR=$(echo ${FN:0:4} | egrep -E ^[0-9]+$ )     # insure digits only
    MONTH=$(echo ${FN:4:2} | egrep -E ^[0-9]+$ )    # insure digits only
    DAY=$(echo ${FN:6:2} | egrep -E ^[0-9]+$ )      # insure digits only
    DATE="$YEAR:$MONTH:$DAY"                        # create a DATE string
    # Check the filename's derived date from for validity (not NULL strings)
    #  and that the date falls within the proper range
    if ([ ! -z "${YEAR}" ] && [ ! -z "${MONTH}" ] && [ ! -z "${DAY}" ]) && \
    [ $(IsValidDate $YEAR $MONTH $DAY) == 1 ]  ; then
      if [ $DEBUG == 1 ] ; then echo "ValidDate: $(IsValidDate $YEAR $MONTH $DAY)" ; fi
      FN_WD=0               # date prefix exists, do not append the derived date to the filename.
    else
      FN_WD=1               # append the derived date prefix to the filename.
    fi

    # Next, attempt to find an EXIF CreateDate from the file, if it exists.
    DATE=$(exiftool -s -f -CreateDate $FN | awk '{print $3}')
    # Perform sanity check on correctly extracted EXIF CreateDate
    if [ "${DATE}" != "-" ] && [ "${DATE}" != "0000:00:00" ] ; then
      # Good date extracted, so extract the year, month and day
      # of month from the EXIF info
      echo "A valid ${WHT}CreateDate${NML} was found, using it."
      YEAR=${DATE:0:4}
      MONTH=${DATE:5:2}
      DAY=${DATE:8:2}
      NOTE="(by CreateDate)"

    else
      # EXIF CreateDate invalid or not found, so attempt to derive the
      # date from the file name.
      YEAR=$(echo ${FN:0:4} | egrep -E ^[0-9]+$ )       # insure digits only
      MONTH=$(echo ${FN:4:2} | egrep -E ^[0-9]+$ )  # insure digits only
      DAY=$(echo ${FN:6:2} | egrep -E ^[0-9]+$ )        # insure digits only
      DATE="$YEAR:$MONTH:$DAY"                      # create a DATE string

      # check the extracted date from filename for validity (not NULL strings)
      #  and that the date falls within the proper range
      #if [ -z "${YEAR}" ] || [ -z "${MONTH}" ] || [ -z "${DAY}" ] ; then
      if ([ ! -z "${YEAR}" ] && [ ! -z "${MONTH}" ] && [ ! -z "${DAY}" ]) && \
      [ $(IsValidDate $YEAR $MONTH $DAY) == 1 ]  ; then
        echo "A valid ${WHT}FileNameDate${NML} was found, using it."
        NOTE="(by file name)"

      else
        # EXIF CreateDate and FileNameDate extraction failed, so attempt
        # to extract the EXIF FileModifyDate from the file, if it exists.
        DATE=$(exiftool -s -f -FileModifyDate $FN | awk '{print $3}')
        # Perform sanity check on correctly extracted EXIF FileModifyDate
        if [ "${DATE}" != "-" ] && [ "${DATE}" != "0000:00:00" ] ; then
          # Good FileModifyDate found, extract the year, month and
          # day of month from the EXIF info
          echo "A valid EXIF CreateDate and FileNameDate were not found!"
          echo " The innacurate ${WHT}FileModifyDate${NML} will be used."
          YEAR=${DATE:0:4}
          MONTH=${DATE:5:2}
          DAY=${DATE:8:2}
          NOTE="(!inaccurate! by FileModifyDate)"
          FN_WD=0               # date prefix exists, do not append the derived date to the filename.
        else
          echo "Invalid date retrieved!"
          if [ $DEBUG == 1 ] ; then
            echo "Length = ${#YEAR}-${#MONTH}-${#DAY}"
          fi
          echo "Skipping File: $FN..."
          echo
        fi
      fi
    fi

    # Modify the filename if a valid EXIF CreateDate or FileNameDate was found.
    if [ $FN_WD == 0 ] ; then
      FILE=${FILE}.${EXT}
    else
      FILE=${YEAR}${MONTH}${DAY}-${FILE}.${EXT}
    fi

    # Debug output
    if [ $DEBUG == 1 ] ; then DumpDebug $FN $FILE $EXT $FN_WD $DATE $YEAR $MONTH $DAY "$NOTE" ; fi

    # We have a date, hopefully a good one, move the file
    if [ $DRYRUN == 0 ] ; then
      # create the directory structure. Pipe errors to NULL
      mkdir -p $YEAR/$MONTH/$DAY >/dev/null 2>&1
      # move the file to the appropriate directory
      echo " -> Moving $FN to $YEAR/$MONTH/$DAY/$FILE $NOTE"
      mv $FN $YEAR/$MONTH/$DAY/$FILE
      echo
    else
      echo "Dryrun: Moving $FN to $YEAR/$MONTH/$DAY/$FILE"
      echo
    fi
    # Clear the variables
    FN=""; FILE=""; EXT=""; FN_WD=""; DATE=""; YEAR=""; MONTH=""; DAY=""; NOTE=""
  else
    echo
    echo "File $FN not found!"
    echo
  fi
done
