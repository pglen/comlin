#!/bin/sh

# This script is used to package a new comlin distro scripts.
# Only used by developers of comlin distos.

HERE=`pwd`
PROJ=`basename $HERE`
TARGET=$1
FF=${TARGET}/${PROJ}-scr.tar.gz

if [ "" == "$TARGET" ] ; then
  echo  "Usage: packscr.sh targetdir"
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


# Security measures:
#./gensum.sh

pushd `pwd` >/dev/null

cd ..


echo "Archiving $PROJ to $FF"

tar cfz $FF $PROJ

popd

echo Done.
