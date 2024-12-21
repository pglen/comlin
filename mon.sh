#!/bin/bash

FF=/mnt/small/comlin/comlin-015.tar.gz
TT=2

if [ "$1" == "" ] ; then
    echo "Use: mon.sh fname timeout"
    exit
fi

if [ ! -f "$1" ] ; then
    echo "File '$1' must exist"
    exit
fi

if [ "$2" != "" ] ; then
    TT=$2
fi

while : ; do 
    ls -l  $1 | awk '{printf "\r%s ", $5}';
    ls -lh $1 | awk '{printf "(%s)  ", $5}';
    sleep $TT
done


