#!/bin/bash

# X Windows apps expect this, X will override if different
export DISPLAY=:0.0

# Change this variable if you need a different default user
USER=user

USERHOME=/home/$USER

# Make sure this user exist
if [ ! -d $USERHOME ] ; then
  useradd -m $USER >/dev/null 2>&1
fi

# Monitor power button for the restart dialog
/usr/bin/python /apps/power/powbutt.py >/dev/null 2>&1 &

# Unmount boot drive, so user's cannot destroy it
umount /media/COMLIN

echo
keyget -t 3 "About to start X: Press a key within 3 seconds to drop to shell ... " 

if [ $? -eq 0 ] ; then
	echo
	echo "Interrupted boot in X(org) startup phase, dropping to shell."
	echo "Exiting shell will continue to start X(org) ..."		
	/bin/bash
fi
	echo

# Change the following line if you want to start a different session

SESS="xinit /usr/bin/gnome-session"

# Cycle X until poweroff requested

while [ 1 == 1 ] ; do

    # Change dir, Set user, Start session ...
    cd $USERHOME; su - user -m -c "$SESS"

    # Alternatively execute X as root (simpler, no access control)
    #xinit "$SESS"

    # See if reboot or poweroff requested
    if [ -e /oldx/reboot ] ; then
        #echo "Reboot requested."
        break 2
    fi

    if [ -e /oldx/poweroff ] ; then
        #echo "Poweroff requested."
        break 2
    fi

    keyget -t 5 "About to restart X: Press Enter within 5 seconds to powerdown instead ... "

    if [ $? -eq 0 ] ; then
	    echo		
	    echo "Dropping to Shutdown / Reboot "
        echo	    
        break
    fi
    echo
done

# Added more time as the screen had to come back from mode change

keyget -t 5 "About to shutdown: Hit Enter within 5 seconds to drop to shell ... "

if [ $? -eq 0 ] ; then
	echo		
	echo "Interrupted in reboot phase, dropping to shell."
	echo "Exiting shell will continue the reboot process ..."		
	bash
fi

	echo		

# This returns to startup2.sh which returns to startup.sh (symmetry!)
    
