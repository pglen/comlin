#!/bin/bash

# Create a new sum for the project

START=../comlin-usb-000
TMPFILE=sha1.tmp
HFILE=sha1.sum

pushd `pwd` >/dev/null

cd $START

echo -n "Checksuming system... "
#cp sha1.sum sha1.sum.old >/dev/null 2>&1
touch "SUMFILE"
#find . -maxdepth 1 -type f -exec shasum {} >$TMPFILE \;
find .  -type f -exec shasum {} >$TMPFILE \;
echo OK

echo -n "Cleaning tmp files ... "
# Remove SUMFILE and sha* files from the check
cat $TMPFILE | grep -E -v "(SUMFILE)|(sha1.tmp)|(sha1.sum)" > $HFILE
rm $TMPFILE
echo OK

# The sumfile should also be checked against auxiliarry sources
echo -n "Generating SUMFILE ... "
shasum HFILE > SUMFILE
echo OK

popd

