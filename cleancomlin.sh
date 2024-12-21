#!/bin/sh

# This script is used to clean distro files
# Copyright by Peter Glen. See open source license for details.

. ./config_build

# Do some cleaning
echo "Cleaning comlin distro at $CURRUSB ..."

rm -rf $CURRUSB/home/user/Download/*  >/dev/null  2>&1
rm -rf $CURRUSB/tmp/*  >/dev/null  2>&1
rm -rf $CURRUSB/tmp/.*  >/dev/null  2>&1

# Remove dangling sockets
find $CURRUSB -type s -exec rm -f {} \;

# Force new host drive detection
rm config_drive >/dev/null 2>&1

echo Done Cleaning.



