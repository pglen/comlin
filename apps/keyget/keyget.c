/*
 * Get return key from stdin with a timeout.
 * 
 *  The motivation for this was to create a timed key getting facitlity
 *  that works with a broken terminal. (like the initial term from the kernel)
 *  I achived this by NOT using terminal controls, but looking at the input 
 *  as a std file.
 *
 *  Revisions:
 *      
 *             Added Ctrl-C to shortcut uninterrupted flow
*/

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/stat.h>

int retalarm = 0, secleft = 5;

char chh[12] = "";
char* message = "To intercept current flow, press Enter in: ";
char help[]   = "usage: keyget [-t timeout] [message]\n";

// -----------------------------------------------------------------------
// Execute timeout routine

void timedout(int sig) 

{
    retalarm = 1;   

    printf("\b\b\b\b\b\b\b\b\b[%2d sec] ", secleft); 
    fflush(stdout);                             // System needs it
 
    if(secleft == 0)
        {
        // Done
        printf("\n");  exit(1);
        }

    secleft--;

    // Re - issue timer alarm
    signal(SIGALRM, timedout);
    alarm(1);     
}

void ctrl_c(int sig)

{
    printf("Ctrl-C pressed\n");
    exit (0);
}

// -----------------------------------------------------------------------


int main(int argc, char *argv[])    

{
    int ret = 0; char ch;

    // Parse options
    while ((ch = getopt(argc, argv, "t:m:")) != -1)
      switch (ch) {
        case 't':
            secleft  = atoi(optarg);
            break;

        // Compatibility for old scripts, last arg overrides
        case 'm':
            message  = strdup(optarg);
            break;

        case 'h':  case '?':
        default:
            fprintf(stderr, help);
            exit(1);
            break;
        }

    // This is dirty .. but I left it in
    argc -= optind;  argv += optind;

    // If message passed, use it
    if (*argv != NULL) {
           message = *argv;
        }

    printf("%s", message);              // Show message
    printf("          ");               // Placeholder for seconds message

    //signal(SIGINT, SIG_IGN);           // Disable ctrl-c
    //signal(SIGINT, ctrl_c);              // 
    //signal(SIGQUIT, ctrl_c);             // 

    signal(SIGALRM, timedout);  
    alarm((unsigned int)1);             // Start alarms

    fgets(&chh[0], 12, stdin);          // Get Sting

    exit (0);
}


