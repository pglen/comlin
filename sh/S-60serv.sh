#!/bin/bash
#
# System initialization script.
#

# By uncommenting the exit below, this script is effective disabled.
# exit

echo -n "Starting system services ... "

atd
anacron
rpcbind
NetworkManager
xinetd -stayalive

# Just in case there is a printer
cupsd

# And we want to reoprt errors (optional)
abrtd

# We start one instance as init is not active
/usr/libexec/polkit-1/polkitd  >/dev/null 2>&1 &

echo OK
