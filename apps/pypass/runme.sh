#!/bin/bash

# run exec, prompt for error

python pypass.py
#echo "Error  $?"
if [ "$?" != "0" ] ; then
	getkey
else
	#sleep 1
	echo "Got OK"
fi
