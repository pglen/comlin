#!/bin/sh

# This script is used to package a new comlin distro.
# Only used by developers of comlin distos. 
# Make sure you execute cleancomlin.sh and checksum.sh before real release.
# Copyright by Peter Glen. See open source license for details.

. ./config_build nocheck

HERE=`pwd`
PROJ=`basename $HERE`
TARGET=$1
FF=${TARGET}/$PROJ.tar.gz

if [ `id -u` != 0 ] ; then
    echo "Must be root to run this script."
    exit 1
fi

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
	echo "Delete it if you want to create a new version."
	exit 1
fi

# Clean distro
#./cleancomlin.sh

# Security measures:
#./gensum.sh

# -----------------------------------------------------------------------

UU=`basename $CURRUSB`

pushd `pwd` >/dev/null

cd ../..

echo "Archiving to $FF (may take a while)"
echo "You may want to disable power save"
echo

tar cfz $FF comlin/$PROJ comlin/$UU comlin/README

popd

# -----------------------------------------------------------------------

echo Done Pack

