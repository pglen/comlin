#!/bin/bash

# Create backups of files by pushing down the ladder .1 .2  etc ...
# Hard coded to limit at LIM files

LIM=10

if [ ! -f $1 ] ; then
	#echo "File $1 must exist"
	exit
fi

if [ ! -s $1 ] ; then
	#echo "File $1 must not be empty"
	exit
fi

DIR=`dirname $1`
FILE=`basename $1`
	
CNT=$(($LIM-1))

mkdir -p $DIR/backup

# Push them back
while test $CNT -gt 0  ; do		
	#echo $CNT
	if [ -f $DIR/backup/$FILE.$CNT ] ; then
		#echo rename $$DIR/backup/$FILE.$CNT $$DIR/backup/$FILE.$(($CNT+1))
		mv -f $DIR/backup/$FILE.$CNT $DIR/backup/$FILE.$(($CNT+1))
	fi
	CNT=$(($CNT-1))
done

# Rename final
mv -f $1 $DIR/backup/$FILE.1

