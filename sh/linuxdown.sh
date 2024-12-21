#!/bin/sh
#
# System termination script. Responsible for unmounting everything and
# sending the system to sleep. This file is obsolete.
#

# We still have working execs in oroot
#export PATH=/oroot/sbin:/oroot/bin:/oroot/usr/sbin:/oroot/usr/bin

# Cheating ... without /proc the system is crippled

mount /proc 

# Move the rest of the mounts to our root

mount -n -o move  /oroot/dev /dev
mount -n -o move  /oroot/sys /sys
mount -n -o move  /oroot/tmp /tmp

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
sleep 1

echo -n "Unmounting ... "

/oroot/bin/umount /oroot/proc/fs/nfsd    >/dev/null 2>&1
umount /oroot/var/lib/nfs/rpc_pipfs  >/dev/null 2>&1

umount /oroot/proc 
umount /oroot
umount /tmp

# Virtual FS on our root, ignore it
#umount /sys

# /dev FS does not keep any important dangling open files, but it
# is holding on ... we ignore it
#umount /dev

# This is just in case the user inserted a device, and the GUI 
# did not deal with it. Also unmounts dangling /sys /proc and fuse mounts
# If a depended FS is on, the second / third run will unmount it

umount -a  >/dev/null 2>&1
umount -a  >/dev/null 2>&1
umount -a  >/dev/null 2>&1

echo OK

# Shutdown (below) did not work ... too much baggage in authorization
# shutdown -P now ; poweroff -f
# I had to forge simple versions of shutdown (note the linux_ prefix)
# We are already root anyway ... so no big deal

if [ -f reboot ]; then
	echo -n "Rebooting ... "; sleep 1
	/oroot/apps/linux_reboot
else
	echo -n "Powering off ... "; sleep 1
	/oroot/apps/linux_poweroff 
fi

echo 
echo  "If control reached here, poweroff did not work on this system. "
echo  "However, everything is unmounted, safe to power off by any means."

echo "BUG: linuxdown.sh Control should not reach here"

while test $CNT -lt 100000  ; do		
	CNT=$(($CNT+1))
done

sh

# Control should not reach here ..

./forever.sh sh

# This would panic the kernel
exit

# EOF
