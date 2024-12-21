#!/bin/bash

# Executing full development / arcive / un-archive / drive creation cycle.
# This is system specific, DO NOT USE WITHOUT CARE!
# Expects a tmp dir and an already installed ComLin USB drive
# Copyright by Peter Glen. See open source license for details.

. ./config_build

# Configure this dir with al least 6 Gig space avalable.
TTT=/mnt/down/comlin/

HERE=`pwd`
PROJ=`basename $HERE`
TARGET=$1
FF=${TARGET}/$PROJ.tar.gz

if [ `id -u` != 0 ] ; then
    echo "Must be root to run this script."
    exit 1
fi

# Check COMBOOT
LLL=`df | grep "/media/COMBOOT"`

if [ "$LLL" == "" ] ; then
    echo "Expected a COMBOOT drive for cycle"
    exit 1
fi

DDEV=`echo $LLL | awk  {'print $1'} | sed s/[0-9]//`
CDEV=`cat config_drive | awk  -F '=' {'print $2'}`

#echo "Device: '$DDEV' '$CDEV'"

if [ "$DDEV" != "$CDEV" ] ; then
    echo "Config mismatch  $DDEV != $CDEV"
    exit
fi

if [ ! -d $TTT ] ; then
    echo "Target dir '$TTT' must exist."
    exit 1
fi

echo "Packing '$PROJ' to '$TTT' "

# Delete tar and unzipped dir so pack.sh will not complain
rm -rf $TTT/comlin
rm -f  $TTT/$PROJ.tar.gz

./pack.sh $TTT

echo "Extracting $PROJ.tar.gz"

cd $TTT
tar xfz $PROJ.tar.gz

if [ ! -d comlin/$PROJ ] ; then
    echo "Expected comlin dir (archive?)"
    exit
fi

cd comlin/$PROJ
 
# Recreate                                                                       
echo "RDDEV=$DDEV" > config_drive

echo "Building new ComLin USB"

make doall2

echo "Done"



