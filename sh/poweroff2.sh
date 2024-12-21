#!/bin/bash

echo
keyget -t 5 "Press the ENTER key within 5 seconds to stop the poweroff process  " 

if [ $? -eq 0 ] ; then
	echo "Interrupted poweroff, continuing normal operation."
	exit
fi

# Just set a marker, so the scripts know what to do
echo "Powering the system down."
touch /oldx/poweroff

# Wind down the system
/sh/deanim.sh

