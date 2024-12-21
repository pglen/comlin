#!/usr/bin/env python

# ------------------------------------------------------------------------
# This is open source editor. Written on python. The motivation for 
# this project was to create a modern multi-platform editor. 
# Simple, powerful, configurable, extendable. 
#
# Pyedit has:
#
#    o  macro recording/play, 
#    o  search/replace, 
#    o  functional navigation,
#    o  comment/string spell check, 
#    o  auto backup, 
#    o  persistent undo/redo, 
#    o  auto complete, auto correct, 
#    o  ... and a lot more. 
#
# It is fast, it is extendable, as python lends itself to easy tinkering. 
# The editor has a table driven key mapping. One can easily edit the key 
# map in keyhand.py, and the key actions in acthand.py The default key map 
# resembles gedit / wed / etp / brief

# ASCII only, fixed font only. For now ... Requires pygtk.

import os, sys, getopt, signal
import gobject, gtk

import pyedlib.keyhand, pyedlib.acthand
import pyedlib.pedutil, pyedlib.pedwin
import pyedlib.pedconfig, pyedlib.pedsql
import pyedlib.log

from pyedlib.pedutil import *

mainwin = None
show_timing = 0
show_config = 0
clear_config = 0
  
# ------------------------------------------------------------------------

def main(strarr):

    if(pyedlib.pedconfig.conf.verbose):
        print "PyEdit running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    signal.signal(signal.SIGTERM, terminate)
    mainwin = pyedlib.pedwin.EdMainWindow(None, None, strarr)
    pyedlib.pedconfig.conf.pedwin = mainwin 
    
    gtk.main()
     
def help():

    print 
    print "PyEdit version: ", pyedlib.pedconfig.conf.version
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]"
    print "Options:"
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose (to stdout and log)"
    print "            -f        - Start Full screen"
    print "            -c        - Dump Config"
    print "            -x        - Clear (eXtinguish) config (will prompt)"
    print "            -h        - Help"
    print

# ------------------------------------------------------------------------

def terminate(arg1, arg2):

    if(pyedlib.pedconfig.conf.verbose):
        print "Terminating pyedit.py, saving files to ~/pyedit"
        
    # Save all     
    pyedlib.pedconfig.conf.pedwin.activate_quit(None)    
    #return signal.SIG_IGN

# Start of program:

if __name__ == '__main__':

    # Redirect stdout to a fork to real stdout and log. This way messages can 
    # be seen even if pyedit is started without a terminal (from the GUI)
    sys.stdout = pyedlib.log.fake_stdout()
    
    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hfvxct")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    pyedlib.pedconfig.conf.version = 0.21

    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-f": pyedlib.pedconfig.conf.full_screen = True
        if aa[0] == "-v": pyedlib.pedconfig.conf.verbose = True            
        if aa[0] == "-x": clear_config = True            
        if aa[0] == "-c": show_config = True            
        if aa[0] == "-t": show_timing = True
    
    try:
        if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
            if(pyedlib.pedconfig.conf.verbose):
                print "making", pyedlib.pedconfig.con.config_dir
            os.mkdir(pyedlib.pedconfig.conf.config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
        print "Cannot access config dir:", pyedlib.pedconfig.conf.config_dir
        sys.exit(1)

    if not os.path.isdir(pyedlib.pedconfig.conf.data_dir):
        if(pyedlib.pedconfig.conf.verbose):
            print "making", pyedlib.pedconfig.con.data_dir
        os.mkdir(pyedlib.pedconfig.conf.data_dir)
         
    if not os.path.isdir(pyedlib.pedconfig.conf.macro_dir):
        if(pyedlib.pedconfig.conf.verbose):
            print "making", pyedlib.pedconfig.con.macro_dir
        os.mkdir(pyedlib.pedconfig.conf.macro_dir)
    
    # Initialize sqlite to load / save preferences & other info    
    sql = pyedlib.pedsql.pedsql(pyedlib.pedconfig.conf.sql_data)
        
    # Initialize pedconfig for use  
    pyedlib.pedconfig.conf.sql = sql
    pyedlib.pedconfig.conf.keyh = pyedlib.keyhand.KeyHand()

    # To clear all config vars
    if clear_config:    
        print "Are you sure you want to clear config ? (y/n)"
        aa = sys.stdin.readline()
        if aa[0] == "y":
            print "Removing configuration ... ",
            sql.rmall()        
            print "OK"
        sys.exit(0)

    # To check all config vars
    if show_config:    
        print "Dumping configuration:"
        ss = sql.getall(); 
        for aa in ss: 
            print aa
        sys.exit(0)

    #pyedlib.log.printx("Started pyedit")
                           
    main(args[0:])

# EOF






