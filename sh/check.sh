#!/bin/sh

echo "Checking filesystem in $ROOTFS"
fsck -y $ROOTFS
echo "Exiting this shell will boot process ... (type exit or CTRL-D)"

