#!/usr/bin/python

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import subprocess

found  = 0
device = ""

def action(*args):

  global found, device
  
  #print 
  
  # Filter out non string arguments
  if len(args) == 0:
    # print "empty"
    return

  if type(args[0]) != dbus.String:
    #print " not string"
    return

  print "dbus: ",

  for aa in range(len(args)):
    print aa, args[aa],
  print 

  return

  if len(args) == 2 and args[0] == "ButtonPressed" and args[1] == "power":
    # The action to perform when the power button is pressed
    print "Power button pressed!"
    subprocess.call(["beep", "-f104", "-l40", "-r2"]);

  look = "/org/freedesktop/UDisks/devices/"
  look2 = "/org/freedesktop/Hal/devices" #/volume"

  idx = args[0].find(look)

  if idx >= 0:
	#print "found0"
	found = 1
	device = args[0]
	#print args[0][len(look2):]
	#print args[0]

  if found == 1:
	idx2 = args[0].find(look2)
	if idx2 >= 0:
	   found = 2
	   print device, "::", args[0]

# Initialize the event loop
DBusGMainLoop(set_as_default=True)

# Connect to the System DBUS
system_bus = dbus.SystemBus()

# Declare an interest in DBUS signals
system_bus.add_signal_receiver(action)

print "Started listening"
# Wait for events
gobject.MainLoop().run()



