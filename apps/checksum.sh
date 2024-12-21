#!/bin/bash

# Verify the integrity of our system

FTMP=/tmp/$$.tmp

if [ `id -u` != 0 ] ; then
    echo "Must be root to run this script."
    exit 1
fi

if [ "$1" == "" ] ; then
    echo "usage: checksum.sh filename_regex"   
    exit 1
fi

echo -n "Checking checksum file ... "
sha1sum --check --quiet SUMFILE
echo OK

echo -n "Generating filename list ... "
grep $1 sha1.sum > $FTMP
echo OK

echo "Checking checksums ... "
sha1sum --check $FTMP
rm -f $FTMP
echo Done


