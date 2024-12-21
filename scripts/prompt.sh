#!/bin/bash

. ./config_build

# Pre ask for sudo pass
sudo echo 

if [ x"$2" == x"" ] ; then
 getkey -c 10  -m "Are you sure you want to $1 $DDEV ? y or ctrl-c to abort " y

 if [ $? != 0 ] ; then 
    echo 
	echo Aborting ...
	exit 1;
 fi
 echo
 echo Proceeding ...
 exit 0

fi

