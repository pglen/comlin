#!/bin/bash
#
# System Termination script.
#

. /sh/functions.sh

# Warn others of impending shutdown

echo -n "Warning all users for immidiate system shutdown ... "
wall "System is going down NOW, please save your work."

# May configure to sleep longer here if your circumstances dictate it
sleep 1

echo "OK"

