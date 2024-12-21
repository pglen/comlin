#!/usr/bin/env python

import gobject
import gtk
import time
import signal, os, time
import logging
import mainwin


'''
def mylog(strx):
    try:
        logging.warning  (strx)
    except:
        print "Cannot log ", strx
'''    
        
def main():

    '''
    try:
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='ctrl_alt_del.log',
                    filemode='w')

        logging.info('ctrl_alt_del started')
    except:
        pass
    '''

    #Logger = logging.getLogger("ctrl_alt_del")
    #Logger.setLevel(logging.WARNING)

    mainwin.AppMainWindow()
   
    print "Started App"
    gtk.main()
    print "Exited app"
    
    #print "action requested: ", mainwin.action

    if mainwin.action == 1:
        pass
    elif mainwin.action == 2:
        pass
    else:
        #print "none"
        pass

    signal.alarm(0)
    time.sleep(1);     

if __name__ == '__main__':
    main()


