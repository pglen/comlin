#
# These funtions are used by the startup / kill scripts.
# Will be copied on boot to the real root. (note: update it here)
#
# Notes:
#
#  Use ext4 and set commit to a minute for flash drive life presevation
#  or .. Use ext3 if you want to allow journaling  (constant disk activity)
#  or .. Use ext2 you do not want to allow journaling 
#
#

# Define some stuff

TARGET=/mnt/system
VERBOSE=0

# Set this to the desired FS type. See notes above.
MYFST=ext4

# Fudge shell funtion to wait a while (used on testing)
# Arg1 is the amout to count to 

waitSome() {
	CNT=1
	while test $CNT -lt $1  ; do		
		CNT=$(($CNT+1))
	done
}

# Create directory if not there

createIF() {
	[ -d $1 ] || mkdir -p $1
}

# ------------------------------------------------------------------------
# Iterate /dev/sd[a-d][1-4], if we can mount it, test for the 'comlin' file.

mountUSB() {
    mkdir -p /mnt/guest
    for i in /dev/sd[a-d]; do
        for ii in $i[1-4];  do
            #echo try $ii
		    if mount  -t $MYFST $ii /mnt/guest >/dev/null 2>&1 ; then
				#echo "test file on $ii"
      			if test -f /mnt/guest/comboot; then
                    #echo "Found COMLIN root at $ii"
				    umount $ii >/dev/null 2>&1
            		DEVICE=$ii
				    return 0
	        	else
				    umount $ii >/dev/null 2>&1
       			fi
		    fi
        	done
        done
    return 1
}

moveMount() {
	mkdir -p ${TARGET}$1
	mount -n -o move $1  ${TARGET}$1
}

unmoveMount() {
	mkdir -p ${2}$1 
	mount -n -o move $1 ${2}$1 
}

# Scan the PCI bus, and install device. Arg1 is the dev type, emtpy
# for 'all' devices

scanMods() {

    if [ x"" == x"$1" ] ; then
        # All devices, except display (X will take care of it)
        PCIDEV=`lspci | grep -iv "vga"`              
    else
        PCIDEV=`lspci | grep -i $1`
    fi
   
    #echo $1 $PCIDEV

    # To do multiline matches, find device descriptors

    for AA in $PCIDEV ; do
      DEV=`echo $AA | grep "0[0-9]:"`

      if [ x"" != x"$DEV" ] ; then 
	    #echo -n "Device: \"$DEV\" -- "

	    MODNAME=`lspci -v -s $DEV | grep "Kernel modules:" | cut -f 3- -d ' '`
        
        for AAA in $MODNAME ; do
 
           # To do multidevice matches, parse line

            AAA=`echo $AAA | sed s/,//;`

            if [ x"" != x"$AAA" ] ; then 
 	            echo -n "Inserting module: \"$AAA\" ... "
	            modprobe -q $AAA
                echo OK
            fi
        done
       fi
    done
}

# Terminate all pocesses higher than $GOV without suiside / petriside
# termAll(SIG, PAR, GOV, WAI)
# SIG = signal; PAR = parent; 
# $GOV = governor process; (only higher numbers are killed)
# WAI = wait in secods

termAll() {
	#procx=`ps xa | cut -f 2 -d ' '`
	#procx=`ls /proc | grep [0-9]`
	procx=`ps xa | cut -c 1-6 | grep -v " *PID.*" | sort -n -r`
	
	#echo $procx

	for aa in $procx ; do
		if [ $$ -eq $aa ] ; then  
			#echo curr $$
			continue;		# do not terminate this script
		fi
		if [ $2 -eq $aa ] ; then  
			#echo par $ME
			continue;		# do not terminate parent script
		fi
        # Kill everything higher than the first batch job
		if [ $3 -lt $aa ] ; then  
			#echo - "Killing  ($1) $aa  "
			kill $1 $aa	>/dev/null 2>&1
		fi
		if [ $4 -ne 0 ] ; then  
			sleep $4
		fi
		
	done
}


