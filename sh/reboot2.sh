#!/bin/bash

echo
keyget -t 5 "Press the ENTER key within 5 seconds to stop the reboot process  " 

if [ $? -eq 0 ] ; then
	echo "Interrupted boot, continuing normal operation."
	exit
fi

# Just set a marker, so the scripts know what to do
echo "Rebooting system."
touch /oldx/reboot

# Wind down the system
/sh/deanim.sh

