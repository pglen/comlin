// Defunct file


#define CONSOLE		"/dev/console"
#define VT_MASTER	"/dev/tty0"

#define DEBUG_ZOMBIE
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


