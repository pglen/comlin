#!/bin/bash
#
# System initialization script. Part two, called after zombie eater started.
# Will be copied on new install to the target. (note: update it here)
#

#echo "in startup2.sh"

cd /sh
. /sh/functions.sh

# Set terminal to a sane state 
stty `cat /sh/stty.txt`

# Watermark to kill processes above
echo $$ >/sh/startproc2

# Estabilish if we are verbose 
grep -q '\<quiet\>' /proc/cmdline || VERBOSE=1

# Estabilish a session like environment
	
export PS1='[\u@\h \W]\$ '
export PS2='> '
export PS4='+ '
export BASH=/bin/bash
export SHELL=/bin/bash
export HOME=/root
export TERM=linux
export TMP=/tmp
export tmp=/tmp

if test $VERBOSE -eq 1 ; then
	echo "Community Linux startup, final phase, please wait..."
    echo
fi

# ------------------------------------------------------------------------
# Initiate system startup. We are now on real root.

# These directories are needed, create if not there
# This is a shorter list, as mkdir -p option creates parents

# Make var directories

for FF in `cat varlist` ; do
	#echo $FF
	mkdir -p $FF  >/dev/null 2>/dev/null
done

# Clean stale pids and locks

find /var/run -type f -exec rm {} \;
find /var/lock -type f -exec rm {} \;
find /var/log -name Xorg* -type f -exec rm {} \;

# Clean temporary files

chmod a+rwx  /tmp
find /tmp -type f -exec rm {} \;

# Rotate previous logs
./filetmp.sh /var/log/messages
./filetmp.sh /var/log/secure
./filetmp.sh /var/log/maillog
./filetmp.sh /var/log/kern
./filetmp.sh /var/log/cron

# See what is going on, start syslog

rsyslogd  -c 5

# (Re)start some daemons

udevd --daemon >/dev/null 2>&1

# Stale reboot instructions from last shutdown
rm -f xold/reboot
rm -f xold/poweroff

# Spawn the initial terminals Redirect for quiet ?? kill

/sh/forever.sh "agetty 38400 /dev/tty3 linux >/dev/null 2>&1" >/dev/null 2>&1 & 
/sh/forever.sh "agetty 38400 /dev/tty4 linux >/dev/null 2>&1" >/dev/null 2>&1 & 

# Serial line login (enable below if needed for debugging)
#./forever.sh "agetty 38400 /dev/ttyS0 linux >/dev/null 2>&1" >/dev/null 2>&1 & 

cd $HOME

# Prompt if system needs intervention (disabled by PG)

#if test $VERBOSE -eq 1 ; then
#	
#    echo
#	keyget -t 3 "Startup: Press a key within 3 seconds to drop to shell ... "
#
#	if [ $? -eq 0 ] ; then
#		echo		
#		echo "Interrupted boot in device phase, dropping to shell."
#		echo "Exiting shell will continue the boot process ..."		
#		bash
#	fi
#fi

# Start S-* (start) scripts, this should block until X dies

for SSS in /sh/S-* ; do
	$SSS $$
done 

# If we arrived here, X died, and we are rebooting ...

echo  "Preparing for shutdown / reboot  ... "
echo

# Make sure all outstanding data is flushed
sync

# Execute K-* (kill) scripts, 

echo Stopping services ....

for KKK in /sh/K-* ; do
	$KKK $$
done 

sync 

# Falling back to startup.sh ... Symmetry!

