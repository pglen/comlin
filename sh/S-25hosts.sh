#!/bin/bash
#
# Set our hostname. Set to a unique name if not already configured.
# Update our hosts file with the primary IP. 
# This script will not handle multi interface situations gracefully,
# but it will do a great job on creating basic connectivity. 
# Which is in harmony with the personal class linux mission.
# 
# Uses obsolete ifconfig for now.
#

. /sh/functions.sh

# Set expected entities

setHostName() {
    hostname `cat /etc/hostname`
    echo "Set host name to '"`hostname`"'"
}

HH=`ifconfig | grep -i hwaddr | head -1 | awk {'print $5'} | sed s/://g | sed s/0//g`
HHH=`echo "host$HH"`

if [ -f /etc/hostname ] ; then
    # If hostname is incorrect, delete /etc/hostname to force new detection.
    echo Hostname already configured. 
    setHostName
else
	# Create a hostname from the first interface's MAC address
	# Not perfect, but a great balance on creating a unique but simple hostname
	echo $HHH > /etc/hostname
	setHostName
 fi

# ------------------------------------------------------------------------
# Now add this to the hosts line so we are found

# Get ifconfig's first interface's second/third line
IP=`ifconfig | grep -A 2 -i hwaddr | grep -i "inet addr" | head -1 | awk -F ":" {'print $2'} |  awk  {'print $1'} `

if [ "$IP" == "" ] ; then
	echo No IP, deferring configuration.
	exit
fi

# Update hosts file

# Create a blank one, if so needed
if [ ! -f /etc/hosts ] ; then
	touch /etc/hosts
fi

# Always present
echo "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4" > /tmp/hosts
echo "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6" >> /tmp/hosts

# Filter existing entries through
cat /etc/hosts | awk -f /sh/edit.awk var=$IP host=$HHH >> /tmp/hosts

# Make sure we remeber the original file (so no harm can be done)
if [ ! -f /etc/hosts.org ] ; then
    cp /etc/hosts /etc/hosts.org
fi

# Switch in newly edited file
mv /etc/hosts /etc/hosts.old >/dev/null 2>&1
mv /tmp/hosts /etc/hosts

#echo \'$HHH\' -- \'$IP\' 

