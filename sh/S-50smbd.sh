#!/bin/bash

# By uncommenting the exit below, this script is effective disabled.
# exit

echo -n "Starting Samba Servers ... "
/usr/sbin/nmbd >/dev/null 2>&1
/usr/sbin/smbd >/dev/null 2>&1
echo OK


