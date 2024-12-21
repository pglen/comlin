#!/bin/bash

# run exec, prompt for error

python pyedit.py
#echo "Error  $?"
if [ "$?" != "0" ] ; then
	getkey
else
	#sleep 1
	echo "Got OK"
fi
