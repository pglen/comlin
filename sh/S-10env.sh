#!/bin/bash

. /sh/functions.sh

echo -n "Starting system dependences ... "

# Not configured swap, just in case it lingers, we disable it (USB!)
swapoff -a              

/bin/dbus-daemon --system  
/usr/sbin/hald --daemon=yes 
eval `/usr/bin/dbus-launch --sh-syntax --exit-with-session`
/usr/bin/gconftool-2 --spawn

# Start LVM volumes
/sbin/vgchange -a y --sysinit >/dev/null 2>&1

# Stop disk activity on the main usb drive. 
# This way, there is no constant disk activity for USB life preservation

udisks --inhibit-polling  $ROOTFS >/dev/null 2>&1 &

# you may stop all if that is better suited to your needs
#udisks --inhibit-all-polling  >/dev/null 2>&1 &

echo OK



