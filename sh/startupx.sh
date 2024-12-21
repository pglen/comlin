#!/bin/bash
#
# System initialization script. Part one (X), called after initrd chrooted.
# Spawns a console for the rest of the work so stdin a stdout are present
# Will be copied on boot to the real root. (note: update it here in initrd)
#
# This will make the current shell a session leader, and wait for
# zombies, and spawn part 2 of the scripts

chvt 2
/apps/zombie/eatzomb -q /sh/startup2.sh

