#!/bin/bash
#
# System Termination animation script. Heuristically determine
# gui programs and kill them
#


# Forget it ... just kill

killall X
killall Xorg
exit

# Not reached ....

# Get watermark process as XORG, make sure it is a number
XID=`ps -C  Xorg -o pid | tail -1`
XIDN=$(($XID+0))

PAR=$(($1+0))

termGUI() {
	#procx=`ps xa | cut -f 2 -d ' '`
	#procx=`ls /proc | grep [0-9]`
	procx=`ps xa | cut -c 1-6 | grep -v " *PID.*" | sort -n -r`
	
	#echo $procx

	for aa in $procx ; do
		if [ $$ -eq $aa ] ; then  
			#echo current $$
			continue;		# do not terminate this script
		fi
		if [ $2 -eq $aa ] ; then  
			#echo parent: $2
			continue;		# do not terminate parent script
		fi
        # Kill everything higher than the first batch job
        # Some exceptions apply

        KKK=1
		if [ $3 -lt $aa ] ; then  
            # Decide if kill is OK
			#NN=`ps -p $aa -o command | grep -v libexec`
			NN=`ps -p $aa -o command | tail -1 | grep -v libexec`
			if [ "$NN" != "" ] ; then
                KKK=0
			fi
            NN=`ps -p $aa -o command | tail -1 | grep gnote`			
			if [ "$NN" != "" ] ; then
                KKK=0
			fi

            NN=`ps -p $aa -o command | tail -1 | grep gnote`			
			if [ "$NN" != "" ] ; then
                KKK=0
			fi

            # Exec kill	if so desired
            if [ $KKK == 1 ; then 
                #echo - "Killing  ($1) $aa  $NN"
			    #echo $NN
			    kill $1 $aa	>/dev/null 2>&1

                if [ $4 -ne 0 ] ; then  
        			sleep $4
        		fi
            fi
		fi		
	done
}

# Animate terminate all GUI programs. Just for show, very effective
# However, well written programs may use this as a save file opportunity

termGUI "" $PAR $XIDN 0

echo "OK"

# And kill the GUI itself
killall X
killall Xorg

