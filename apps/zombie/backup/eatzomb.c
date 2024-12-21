/*
 *  Eat zombies as init is not present in this scenario.
 *  Uses subreaper kernel control. PRCTL
 */

#include <termios.h>
#include <utmp.h>
#include <ctype.h>
#include <stdarg.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <time.h>
#include <fcntl.h>
#include <string.h>
#include <signal.h>
#include <termios.h>

#ifdef __linux__
#include <sys/kd.h>
#endif

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/wait.h>

#include <sys/syslog.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/time.h>

#include <linux/prctl.h>

#define PR_SET_CHILD_SUBREAPER 36
#define PR_GET_CHILD_SUBREAPER 37


/* Set a signal handler. */
#define SETSIG(sa, sig, fun, flags) \
        do { \
                sa.sa_handler = fun; \
                sa.sa_flags = flags; \
                sigemptyset(&sa.sa_mask); \
                sigaction(sig, &sa, NULL); \
        } while(0)

int cnt = 0; int err = 0;
int logflag = 0, qflag = 0;
int pid, pidc = -1;

/* 
 * Empty signal handler 
 */

void    sdummy(int dummy)
{
    return;
}

/*
 *  Set up reaper.
 */

int  main(int argc, char *argv[])

{
    struct sigaction act; char *pname = argv[0];
    int st = 0, opt, status;

    // Set some signals to no action
    sigaction(SIGHUP, NULL, &act);
    act.sa_handler = sdummy;
    sigaction(SIGHUP, &act, NULL);

    sigaction(SIGTERM, NULL, &act);
    act.sa_handler = sdummy;
    sigaction(SIGTERM, &act, NULL);

    //sigaction(SIGINT, NULL, &act);
    //act.sa_handler = sdummy;
    //sigaction(SIGINT, &act, NULL);

    // Get our name 
	char *prog = strrchr(pname, '/'); 
    if(prog == NULL) prog = pname; else prog++;

    while ((opt = getopt(argc,argv,"p:lqh")) != EOF) switch (opt) {
        case '?':
                printf("Invalid option(s) on command line.\n");
                exit(1);

        case 'h':
            printf("usage: %s [options] path_to_exec\n", prog);
                printf("        -l      turn on loggging\n");
                printf("        -q      quiet operation\n");
                printf("        -h      show help\n");
                exit(1);
                break;

        case 'p':
            if ((pidc = atoi(optarg)) < -1) {
                  printf("Illegal pid value (%s)!\n", optarg);
                  closelog();
                  exit(1);
                }
        
        case 'l':
                logflag = 1;
                
        case 'q':
                qflag = 1;

        default:
             /* Nothing */
                break;
        }

    // Big no no, kept it anyway
    argc -= optind;  argv += optind;

    if(logflag)
        openlog("eatzomb", LOG_PID, LOG_USER);

    //printf("%s Ver 1.0 pid = %d\n", prog, pidc);
	
    if(!qflag)
        printf("%s Ver 1.0\n", prog);
	
    if(logflag)	
        syslog(LOG_INFO,"Started eatzomb");
                     
	if(argv[0] == NULL)
	    {
	    printf("%s: Please specify a program to run.\n", prog);
        if(logflag)
	        syslog(LOG_ERR,"No program specified");

        exit(0);
	    }	

    // Make us a session leader and group leader
    setsid(); setpgrp();

    // Make us a reaper
	errno = 0;
	int ret = prctl(PR_SET_CHILD_SUBREAPER, 1);
    if(ret)
        if(logflag)
            syslog(LOG_ERR,"Cannot set reaper flag %d %s", errno, strerror(errno));

	if ((pid = fork()) == 0) {

        // Tried making the child too ... no need
		//ret = prctl(PR_SET_CHILD_SUBREAPER, 1);
	    //if(ret)
        //    if(logflag)
	    //        syslogv(LOG_ERR,"Cannot set reaper flag %d %s", errno, strerror(errno));

        int ret = execv(argv[0], &argv[0]);        

        // Control should not come here
        printf("Cannot execute '%s' (%s)\n", argv[0], strerror(errno));
        printf("Press Ctrl-C to abort ... ");
        err = 1;

        #sigaction(SIGINT, NULL, &act);
        #act.sa_handler = SIG_DFL;
        #sigaction(SIGINT, &act, NULL);

        exit(1);
        }
    else if (pid > 0) {    
        
        //printf("in parent %d\n", pid);

        while(1==1)
            {
		    siginfo_t info;

            if(err) 
                break;

			memset(&info, sizeof(info), 0);

            int ret = waitid(P_ALL, 0,  &info, WEXITED);

            syslog(LOG_WARNING,"Zombie Process Collected %d",  ret);
                  
            //printf("Waited on ret=%d  si_pid=%d errno=%d (%s)\n", 
			//		ret, info.si_pid, errno, strerror(errno));
			
            // We do not expect lot of zombies, let them breathe
            sleep(1);
            }

        if(logflag)
            {
            syslog(LOG_INFO,"Ended eatzomb");
            closelog();
            }

        //printf("in parent after wait %d\n", pid);        
    	}
    else  
		{
        if(logflag)
            syslog(LOG_ERR,"Cannot fork");
        printf("Cannot fork\n");
	    }		

    if(logflag)
        closelog();
    exit (0);
}

