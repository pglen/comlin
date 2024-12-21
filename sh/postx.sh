#!/bin/sh

# Create a reasonable post X environment

cd /root

export PS1='[\u@\h \W]\$ '
export PS2='> '
export PS4='+ '
export TERM=linux
export colors=/etc/DIR_COLORS

# Added more time as the screen had to com back from mode change

getkey -c 5 -m "About to poweroff / reboot: Press a key within %d seconds to drop to shell ..."

if [ $? -eq 0 ] ; then
	echo		
	echo "Interrupted in reboot phase, dropping to shell."
	echo "Exiting shell will continue the reboot process ..."		
	bash
fi
	echo		


