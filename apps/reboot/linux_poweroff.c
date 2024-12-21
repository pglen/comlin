/*
 * We created two excutables, following Linux tradition. In the origianl
 * implementation, these are symlinks to one excutable, but we are keeping it simple.
 *   
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include "linux_reboot.h"

int main(int argc, char *argv[])

{
   struct stat st;

    // Run only if the reboot / shutdown file exist.
    // This prevents accidental reboot if the user types this command by chance
 
   if (stat(poweroff_file, &st) < 0) {
        printf("Exec poweroff condition not met, see README for more info.\n");
        exit(1);
    }

    my_reboot(LINUX_REBOOT_CMD_POWER_OFF);
}

