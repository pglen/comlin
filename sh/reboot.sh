#!/bin/bash

# Just set a marker, so the scripts know what to do
echo "Rebooting system."
touch /oldx/reboot

# Wind down the system
/sh/deanim.sh

