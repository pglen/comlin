#!/bin/bash

#echo  $1
#echo \"$2\"


# Patch out snd- prefix
DEV=`echo  $1 | sed  s/snd-//;`

echo $DEV
echo

RES=`echo  "$2" | grep -i $DEV`

#echo $RES
    
if [ x"$RES" != x"" ] ; then

    echo -n "Found: "
    #echo $RES
    #echo
    echo $1
    #echo $2
        
fi

    
