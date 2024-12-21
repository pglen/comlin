#!/bin/bash

# By uncommenting the exit below, this script is effective disabled.
# exit

echo -n "Starting NFS Servers ... "

modprobe nfsd

# Create public directory (disallow this if you do not want nfs pub dir)
mkdir -p /apps/pub
chmod a+rwx /apps/pub

# Start dependencies
/sbin/rpcbind >/dev/null 2>&1
/usr/sbin/rpc.statd >/dev/null 2>&1
/usr/sbin/rpc.rquotad >/dev/null 2>&1
/usr/sbin/rpc.mountd >/dev/null 2>&1
/usr/sbin/rpc.idmapd >/dev/null 2>&1
/usr/sbin/rpc.nfsd >/dev/null 2>&1

echo OK


