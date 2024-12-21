

# Scan the PCI bus, and install device. Arg1 is the dev type, emtpy
# for 'all' devices

MODALIAS=/lib/modules/`uname -r`/modules.alias

#echo $MODALIAS

scanMods2() {

    if [ x"" == x"$1" ] ; then
        # All devices, except display (X will take care of it)
        PCIDEV=`lspci | grep -iv "vga"`              
    else
        PCIDEV=`lspci | grep -i $1`
    fi
   
    #echo "$1  ->  $PCIDEV"
    
    # To do multiline matches, find device descriptors

    for AA in $PCIDEV ; do
      DEV=`echo $AA | grep "0[0-9]:"`

      if [ "" != "$DEV" ] ; then 

	    #echo -n "Device: \"$DEV\" -- "
        DNUM=`lspci -n -s $DEV | awk '{print $3'}`
        #echo "Dnum '$DNUM'"
        NUM1=`echo $DNUM |  awk -F ":" '{print $1'}`
        #echo "num1 '$NUM1'"
        NUM2=`echo $DNUM |  awk -F ":" '{print $2'}`
        #echo "num1 '$NUM2'"
  
        MODNAME=`grep $NUM1 $MODALIAS | grep $NUM2 $MODALIAS | awk {'print $3'}`

        #echo "Modname '$MODNAME'"

	    #MODNAME=`lspci -v -s $DEV | grep "Kernel modules:" | cut -f 3- -d ' '`
     
        for AAA in $MODNAME ; do
 
           # To do multidevice matches, parse line

            AAA=`echo $AAA | sed s/,//;`

            if [ "" != "$AAA" ] ; then 
 	            echo -n "Inserting module: '$AAA' ... "
	            #modprobe -q $AAA
                echo OK
            fi
        done
       fi
    done
}

scanMods2 "audio"


