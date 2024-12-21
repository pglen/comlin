#!/bin/bash

# Mirror user's home dir

# You may edit this to you drive's label
MPOINT=/media/COMBOOT

# Is the drive here?
GREPX=`df | grep $MPOINT`

if [ "$GREPX" == "" ] ; then 
    echo "Mount (insert) secondary first."
   	exit 1
fi

cd
cp -au * $MPOINT/home/user

