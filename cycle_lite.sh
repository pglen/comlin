#!/bin/bash

# Executing full development / arcive / un-archive / drive creation cycle.
# This is system specific, DO NOT USE WITHOUT CARE!
# Expects a tmp dir and an already installed ComLin USB drive

# This is the LITE creation script.


TTT=/mnt/small/comlin/

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

#echo "Device: '$DDEV'"

# Current version number
DD=`pwd`
VER=`basename $DD | awk -F '-' {'print $2'} |  sort -n | tail -1`
#echo "Version: '$VER'"

if [ ! -d $TTT ] ; then
    echo "Target dir '$TTT' must exist."
    exit 1
fi

echo "Packing to: '$TTT' "

XXX=comlin-${VER}_lite.tar.gz

rm -rf $TTT/comlin
rm -f $TTT/$XXX

./pack_lite.sh $TTT

echo "Extracting $XXX"

cd $TTT
tar xfz $XXX

if [ ! -d comlin/comlin-$VER ] ; then
    echo "Expected comlin dir (archive?)"
    exit
fi

# Repair lite exception
cd comlin/
mv  comlin-lite-000 comlin-usb-000
cd comlin-$VER
                                    
echo "RDDEV=$DDEV" > config_drive

echo "Building new ComLin USB"

make doall2

echo "Done"

