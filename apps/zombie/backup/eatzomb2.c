/*
 *  Eat zombies as init is not present in this scenario.
 *  Uses subreaper kernel control.
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

#define CONSOLE		"/dev/console"
#define VT_MASTER	"/dev/tty0"

#define DEBUG_ZOMBIE

/* Set a signal handler. */
#define SETSIG(sa, sig, fun, flags) \
        do { \
                sa.sa_handler = fun; \
                sa.sa_flags = flags; \
                sigemptyset(&sa.sa_mask); \
                sigaction(sig, &sa, NULL); \
        } while(0)

int cnt = 0;
int sigcnt = 0;
int allcnt = 0;
char *console_dev;              /* Console device. */
char *user_console = NULL;      /* User console device */
int opt, pidc = -1;

/*
 *   Set console_dev to a working console.
 */

void console_init(void)
{
        int fd;
        int tried_devcons = 0;
        int tried_vtmaster = 0;
        char *s;

        if (user_console) {
                console_dev = user_console;
        } else if ((s = getenv("CONSOLE")) != NULL)
                console_dev = s;
        else {
                console_dev = CONSOLE;
                tried_devcons++;
        }
           
       while ((fd = open(console_dev, O_RDONLY|O_NONBLOCK)) < 0) {
         if (!tried_devcons) {
                        tried_devcons++;
                        console_dev = CONSOLE;
                        continue;
                }
                if (!tried_vtmaster) {
                        tried_vtmaster++;
                        console_dev = VT_MASTER;
                        continue;
                }
                break;
        }
        if (fd < 0)
                console_dev = "/dev/null";
        else
                close(fd);
}


/*
 *      Open the console with retries.
 */

int console_open(int mode)

{
        int f, fd = -1;
        int m;

        /*
         *      Open device in nonblocking mode.
         */
        m = mode | O_NONBLOCK;

        /*
         *      Retry the open five times.
         */
        for(f = 0; f < 5; f++) {
                if ((fd = open(console_dev, m)) >= 0) break;
                usleep(100);
        }

   if (fd < 0) return fd;

        /*
         *      Set original flags.
         */
        if (m != mode)
                fcntl(fd, F_SETFL, mode);

        return fd;
}

/* SIGCHLD handler - discards completion status of children */

void    release_zombie(int dummy)

{
  int status;
  pid_t pid;
  siginfo_t info;

  printf("in release_zombie %d\n", pidc);

   //while ((pid = waitid(P_ALL, 0, &info, WNOHANG)) > 0) 
 
    while ((pid = waitpid(pidc, &status, 0)) > 0) 
    {
        printf("release_zombie in waitpid %d status %d\n", pid, status);

        if (WIFEXITED(status))
           cnt++;
        else if (WIFSIGNALED(status))
           sigcnt++;
        else
            allcnt++;

#ifdef DEBUG_ZOMBIE

    if (WIFEXITED(status))
      syslog(LOG_INFO, "pid %ld exited with status %d.", pid, WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
      syslog(LOG_NOTICE, "pid %ld killed with signal %d.", pid, WTERMSIG(status));
    else if (WIFSTOPPED(status))
      syslog(LOG_NOTICE, "pid %ld stopped with signal %d.", pid, WSTOPSIG(status));
    else
      syslog(LOG_WARNING, "pid %ld unknown reason for SIGCHLD", pid);

#endif

    }
    return;
}

void    sdummy(int dummy)
{
    /* Empty signal handler */
    //nothing_to_do = 0;
    return;
}

/*
 *
 */

int  main(int argc, char *argv[])

{
    struct sigaction act; char *pname = argv[0];
    int st = 0, pid = 0, f = 0;    
    int status;

    openlog("eatzomb", LOG_PID, LOG_USER);

    sigaction(SIGCHLD, NULL, &act);
    act.sa_handler = release_zombie;
    act.sa_flags   = SA_NOCLDSTOP | SA_NOCLDWAIT | SA_RESTART;
    //sigaction(SIGCHLD, &act, NULL);

    sigaction(SIGHUP, NULL, &act);
    act.sa_handler = sdummy;
    sigaction(SIGHUP, &act, NULL);

   while ((opt = getopt(argc,argv,"p:")) != EOF) switch (opt) {
            case '?':
                    syslog(LOG_ERR,"invalid options on command line!\n");
                    printf("Invalid option(s) on command line!\n");
                    closelog();
                    exit(1);

            case 'p':
                if ((pidc = atoi(optarg)) < -1) {
                      syslog(LOG_ERR, "illegal pid value (%s)!\n", optarg);
                      printf("Illegal pid value (%s)!\n", optarg);
                      closelog();
                      exit(1);
                    }
                    
            default:
                        /* Nothing */
                        break;
        }
        argc -= optind;  argv += optind;

	int ret, zsid;
	char *prog = strchr(pname, '/'); if(prog == NULL) prog = pname;

    printf("%s Ver 1.0 pid = %d\n", prog, pidc);
	
    // make us a session leader
    setsid();
    setpgrp();

    //printf("Our uid=%d gid=%d\n", getuid(), getgid());
    //printf("Our pid=%d ppid=%d\n", getpid(), getppid());
	
	//if(pidc == -1)
	//	{
	//	printf("Please specify pid. Exiting ...\n");
	//	exit(0);
	//	}

    // Make us a reaper
	errno = 0;
	ret = prctl(PR_SET_CHILD_SUBREAPER, 1);
	printf("Sent prctl ret=%d  errno=%d (%s)\n", ret, errno, strerror(errno));

	if(argv[0])
	    {
	    printf("argv '%s'\n", argv[0]);
	    }	
	
	if ((pid = fork()) == 0) {
        printf("in child %d\n", getpid());
		   //if ((f = console_open(O_RDWR|O_NOCTTY)) >= 0) {
		   //                         /* Take over controlling tty by force */
		   //                         (void)ioctl(f, TIOCSCTTY, 1);
		   //                         dup(f);
		   //                         dup(f);
		   // }

		    //pause();

		errno = 0;
		ret = prctl(PR_SET_CHILD_SUBREAPER, 1);
		//printf("Sent prctl ret=%d  errno=%d (%s)\n", ret, errno, strerror(errno));

        //int ret = execl(argv[0], "", (char*)NULL);        
        int ret = execv(argv[0], &argv[0]);        

        // Control should not come here
        //printf("Ret from exec %d\n", ret);
        
        exit(1);
        }
    else if (pid > 0) {    
        
        printf("in parent %d\n", pid);
		siginfo_t info;

        while(1==1)
            {
			memset(&info, sizeof(info), 0);

            int ret = waitid(P_ALL, 0,  &info, WEXITED);

            //int ret = waitpid(pid, &status, 0);
            //int ret = waitpid(-1, &status, 0);
      
            printf("Waited on ret=%d  si_pid=%d errno=%d (%s)\n", 
					ret, info.si_pid, errno, strerror(errno));
			
            sleep(1);
            }

        printf("in parent after wait %d\n", pid);
        
    	}
    else  
		{
        printf("Cannot fork\n");
	    }		
    exit (0);
}

