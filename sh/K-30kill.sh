#!/bin/sh
#
# System Termination script. 
#
# It is a /bin/sh as it will be called from initrd too.
#

. /sh/functions.sh

# Get watermark process ID, make sure it is a number
GOV=$((`cat /sh/startproc`+0))
PAR=$(($1+0))

#echo Governing proc=$GOV current proc=$$ parent proc=$PAR

echo -n "Stopping network servers ... "

# Stop NFS
echo -n "NFS "
killall rpc.nfsd >/dev/null 2>&1

# Stop SAMBA
echo -n "SMB "
killall smbd, nmbd >/dev/null 2>&1

echo -n "HTTP "
# Stop WEB services
killall httpd >/dev/null 2>&1
killall nss_pcache >/dev/null 2>&1

echo OK

# Kill everything with a higher PID

echo -n "Stopping all other processes ... "
termAll 15 $PAR $GOV 0
echo OK
 
# Wait for things to settle

echo -n "Waiting for things to settle ... "
sleep 2
echo OK

# Kill everything with a higher PID, use force

echo -n "Killing all processes (force phase) ... "
termAll 9 $PAR $GOV 0
echo OK

# Special treatment for this guy
#killall -9 eatzomb  >/dev/null 2>&1

# Will fall back to startup2 and startup. Symmetry!

