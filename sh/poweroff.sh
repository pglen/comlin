#!/bin/bash

# Just set a marker, so the scripts know what to do
echo "Powering the system down."
touch /oldx/poweroff

# Wind down the system
/sh/deanim.sh

