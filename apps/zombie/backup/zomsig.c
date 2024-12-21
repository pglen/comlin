// Defunct file

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

