#!/bin/bash

. ./config_build

if [ x"$1" == x"" ] ; then
 getkey -c 5  -m "Are you sure you want to fdisk \"$RDDEV\" ? y or ctrl-c to abort " y

 if [ $? != 0 ] ; then 
	echo
	exit;
 fi
 echo
fi

