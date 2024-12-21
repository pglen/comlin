#!/bin/bash
#
# Scan the PCI bus, and load ALL drivers. Enable this if the other scripts 
# do not find your device. (Possibly being in 'other' categories like 
# SD card reader etc ...)
#
# Disable this script if blind loading interferes with you system.
#

# By uncommenting the exit below, this script is effective disabled.
# exit

. /sh/functions.sh

# Scan ALL mods, so modules that do not fit in any other category will load

scanMods ""

# Load the utf8 codepage. This is needed for CDROMS and Wireless SSID names
# Should be compiled in ... 

#modprobe nls_utf8

# Load user space FS for cryptkeeper

#modprobe fuse

# Load the Webcam Driver. This should fire up when the usb subsystem
# comes up ... but it does not happen. Instaed of re-probing, we 
# start it blindly. Will not hurt (hang) if no camera is present.

modprobe uvcvideo

