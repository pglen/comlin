#!/bin/bash

# By uncommenting the exit below, this script is effective disabled.
# exit

echo -n "Starting Secure Shell ... "
/usr/sbin/sshd >/dev/null 2>&1
echo OK

