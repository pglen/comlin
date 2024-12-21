#
# We created two excutables, following Linux tradition. In the origianl
# implementation, these are symlinks to one excutable, but we are keeping it simple.
#

all: linux_reboot linux_poweroff


linux_reboot: linux_reboot.c
	gcc linux_reboot.c -o linux_reboot

linux_poweroff: linux_poweroff.c
	gcc linux_poweroff.c -o linux_poweroff
    
