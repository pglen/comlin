#!/bin/sh

# This script is used to package a new comlin distro.
# Only used by developers of comlin distos.

# This incarnation builds the lite version

HERE=`pwd`
PROJ=`basename $HERE`
TARGET=$1

FF=${TARGET}/${PROJ}_lite.tar.gz
UU=comlin-lite-000

if [ "" == "$TARGET" ] ; then
  echo  "Usage: pack.sh targetdir"
  exit 1
fi

if [ ! -d $TARGET ] ; then
    echo "Target  '$TARGET'  must be a directory"
    exit 1
fi

if [ -f $FF ] ; then
	echo "Refuse to overwrite archive '$FF' "
	echo "Delete it if you want to create a new version"
	exit 1
fi

# Do some cleaning
echo "Cleaning ../$UU"

rm -rf ../$UU/home/user/Download/*  >/dev/null  2>&1
rm -rf ../$UU/tmp/*  >/dev/null  2>&1
rm -rf ../$UU/tmp/.*  >/dev/null  2>&1

# Remove dangling sockets
find ../$UU -type s -exec rm -f {} \;

# Security measures:  (disabled for lite)
#./gensum.sh

# Force new detection
rm config_drive >/dev/null 2>&1

pushd `pwd` >/dev/null

cd ../..

echo "Archiving $ROJ to $FF (may take a while)"
tar cfz $FF comlin/$PROJ comlin/$UU comlin/README

popd

echo Done.
