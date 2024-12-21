#!/bin/sh

# This script is used to clean host work / saved files

HERE=`pwd`
PROJ=`basename $HERE`
UU=comlin-usb-000

# Do some cleaning
echo "Cleaning ../$UU"

rm -rf ../$UU/home/user/Download/*  >/dev/null  2>&1
rm -rf ../$UU/tmp/*  >/dev/null  2>&1
rm -rf ../$UU/tmp/.*  >/dev/null  2>&1

# Remove dangling sockets
find ../$UU/var -type s -exec rm -f {} \; > /dev/null 2>&1

echo Done.


