#!/bin/bash
#
# Ethernet probe. We scan the PCI bus, and find the right driver
#

. /sh/functions.sh

#echo "Starting ethernet devices ... "

# We may want to activate subsequent busses
scanMods "pcmcia"

scanMods "ether"

# Start network(s), if any. One may want to scan for less NICs
for AA in 0 1 2 3 4 5 6 ; do
    ET=`ip link | grep eth$AA`
    if [ "" != "$ET" ] ; then
        ip link set eth$AA up
    fi
done
    
scanMods "wireless"

# Start wireless, if any
for AA in 0 1 2 3 ; do
    WL=`ip link | grep wlan$AA`    
    if [ "" != "$WL" ] ; then
        ip link set wlan$AA up
    fi

done

echo OK
    
