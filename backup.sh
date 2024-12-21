#!/bin/sh

# This is specific to my system, adjust to yours
TARGET=/mnt/data/backup

if [ ! -d $TARGET ] ; then
    echo Target dir $TARGET does not exost
    exit 1
fi

HERE=`pwd`
PROJ=/comlin/`basename $HERE`

mkdir -p ${TARGET}/$PROJ

echo Backing up from \"$HERE\" 
echo "         ... to \"${TARGET}/$PROJ\""
cp -au * ${TARGET}/$PROJ
