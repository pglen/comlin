#!/bin/bash
#
# System initialization script. Part one, called after initrd chrooted.
# Spawns a console fo the rest of the work so stdin a stdout are present
# Will be copied on boot to the real root. (note: update it here)
#

#echo "In startup.sh"

# Get out of the way
cd /sh

. ./functions.sh

# Create the minimally expected devices (just in case)
[ -e /dev/console ] || mknod -m 0600 /dev/console c 5 1
[ -e /dev/null ] || mknod /dev/null c 1 3

# Estabilish if we are verbose 
grep -q '\<quiet\>' /proc/cmdline || VERBOSE=1

# Mark startup process ID. This is needed so we will not 
# kill it on poweroff (like init pid=1, but dynamic or like killall5)

echo $$ >/sh/startproc

# Allow access to oldx for users. This way any user can set shutdown flag.
mkdir -p /oldx  >/dev/null 2>&1
chmod  a+rwx /oldx  >/dev/null 2>&1

# Stale reboot files from last boot
rm -f /oldx/reboot  >/dev/null 2>&1
rm -f /oldx/poweroff  >/dev/null 2>&1

#echo "In startup.sh before agetty"

# Remount with new commit options (see TECH)
mount / -o remount,commit=60

# Skip to a new terminal for correct redirection
/sbin/agetty -n -l "/sh/startupx.sh" 38400 /dev/tty2 linux 

# ------------------------------------------------------------------------
# If contol comes here, all kill scripts are done, and we are rebooting

# Kill our last killer (if any)
killall K-30kill.sh >/dev/null 2>&1
killall -9 eatzomb >/dev/null 2>&1
killall -9 startup2.sh >/dev/null 2>&1

# Wholesale kill
echo -n "Killing remaining processes ... "

# We kill them in reverse order
procx=`ps xa | cut -c 1-6 | grep -v " *PID.*" | sort -n -r`	
for aa in $procx ; do
	if [ $$ -eq $aa ] ; then  
		#echo curr $$
		continue;		# do not terminate this script (self)
	fi
	kill -9 $aa  >/dev/null 2>&1
done
echo OK; 

echo "Flushing all buffers ... " 
sync
echo OK; 

echo -n "Unmounting al file systems ... "

umount /proc/fs/nfsd    >/dev/null 2>&1
umount /media/COMLIN     >/dev/null 2>&1
umount /tmp  >/dev/null 2>&1

# This is just in case the user inserted a device, and the GUI 
# did not deal with it. Also unmounts dangling /sys /proc and fuse mounts
# If a dependent FS is still on, the second / third run will unmount it

umount -a  >/dev/null 2>&1
umount -a  >/dev/null 2>&1
umount -a  >/dev/null 2>&1

echo OK

# Move away from old root, so this process is not holding dirs
cd /oldx

# Shutdown (below) did not work ... too much baggage in authorization
# shutdown -P now ; poweroff -f
# I had to forge simple versions of shutdown (note the linux_ prefix)
# We are already root anyway ... so no big deal

# Needed for the utility to perform poweroff (access control)
touch "poweroff"      

if [ -f reboot ]; then
	echo -n "Rebooting ... "; sleep 1
	/apps/reboot/linux_reboot
else
	echo -n "Powering off ... "; sleep 1
	/apps/reboot/linux_poweroff 
fi

echo 
echo  "If control reached here, poweroff did not work on this system. "
echo  "However, everything is unmounted, safe to power off by any means."

/sh/forever.sh sh

# This would panic the kernel
exit

