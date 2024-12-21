#!/bin/bash
#
# Sound probe. We scan the PCI bus, and find the right driver
#

# By uncommenting the exit below, this script is effective disabled.
# exit

. /sh/functions.sh

scanMods "media"

# Start top level sound drivers (obsolete)

#modprobe snd-mixer-oss
#modprobe snd-pcm-oss
#modprobe snd-seq-oss

# Just to let the user know, that there is sound
play /usr/share/sounds/KDE-Sys-App-Error-Serious.ogg


