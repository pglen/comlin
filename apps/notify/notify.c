/*****************************************************************************\

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

\*****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <signal.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <syslog.h>
#include <dlfcn.h>

#define _STRINGIZE(x) #x
#define STRINGIZE(x) _STRINGIZE(x)
#define BUG(args...) syslog(LOG_ERR, __FILE__ " " STRINGIZE(__LINE__) ": " args)

static int verbose;

static void usage()
{
    fprintf(stderr, "\nUsage: notify [-t timeout] [-d delay ] [-h] [-r] header message \n\n");
    fprintf(stderr, "     -h            show help (this message)\n");
    fprintf(stderr, "     -r            add random interval to delay (0-5 sec)\n");
    fprintf(stderr, "     -t timeout    show for timeout msec \n");
    fprintf(stderr, "     -d delay      wait for delay seconds\n\n");

    fprintf(stderr, "The delay and random are cummulative.\n\n");
    //fprintf(stderr, "The timeout specified in milliseconds the delay in seconds.\n\n");
         
} /* usage */


static int notify(const char *summary, const char *message, int ms_timeout) 
{
    void *handle=NULL, *n;
    int stat=1; 

    typedef void  (*notify_init_t)(char *);
    typedef void *(*notify_notification_new_t)(const char *, const char *, const char *, void *);
    typedef void  (*notify_notification_set_timeout_t)(void *, int);
    typedef void (*notify_notification_show_t)(void *, char *);

    notify_init_t n_init;
    notify_notification_new_t n_new;
    notify_notification_set_timeout_t n_timeout;
    notify_notification_show_t n_show;

    //set_x_environment();

    /* Bypass glib build dependencies by loading libnotify manually. */  

    if ((handle = dlopen("libnotify.so.1", RTLD_LAZY)) == NULL)
    {
       BUG("failed to open libnotify: %m\n");
       goto bugout;
    }

    if ((n_init = (notify_init_t)dlsym(handle, "notify_init")) == NULL)
    {
       BUG("failed to find notify_init: %m\n");
       goto bugout; 
    }
    n_init("Basics");

    if ((n_new = (notify_notification_new_t)dlsym(handle, "notify_notification_new")) == NULL)
    {
       BUG("failed to find notify_notification_new: %m\n");
       goto bugout;
    }
    n = n_new(summary, message, NULL, NULL);

    if ((n_timeout = (notify_notification_set_timeout_t)dlsym(handle, "notify_notification_set_timeout")) == NULL)
    {
        BUG("failed to find notify_notification_set_timeout: %m\n");
        goto bugout;
    }
    n_timeout(n, ms_timeout);

    if ((n_show = (notify_notification_show_t)dlsym(handle, "notify_notification_show")) == NULL)
    {
       BUG("failed to find notify_notification_show: %m\n");
       goto bugout;
    }
    n_show(n, NULL);

    stat=0;

bugout:
    if (handle)
       dlclose(handle);

    return stat;
} /* notify */


int main(int argc, char *argv[])
{
   int i, ret = 0, randx = 0;
   int cnt, bytes_read, timeout = 3000, delay = 0;

   while ((i = getopt(argc, argv, "rnht:d:")) != -1)
   {
      switch (i)
      {
      case 't':
        timeout = atoi(optarg);
        //printf("timeout %d\n", timeout);
        break;

      case 'd':
        delay = atoi(optarg);
        //printf("delay %d\n", delay);
        break;

     case 'r':
        srand(time(NULL));
        randx = rand() % 5;
        //printf("rand %d", randx);
        delay += randx;
        break;

      case 'h':
         usage();
         exit(0);

      case 'n':
        //printf("noop\n");
         break;

      case '?':
         usage();
         fprintf(stderr, "unknown argument: %s\n", argv[1]);
         exit(-1);

      default:
         break;
      }
   }

    // This is dirty .. but I left it in
    argc -= optind;  argv += optind;

    //printf("argc %d optind %d\n", argc, optind);

    if(argc < 2)
        {        
        //fprintf(stderr, "Not enough arguments.\n");
        usage();
        exit(0);
        }

    if(delay)
        sleep(delay);

    notify(argv[0], argv[1], timeout);

   exit(ret);

} /* main */


