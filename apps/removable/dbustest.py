#!/usr/bin/python

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import subprocess

found  = 0
device = ""

def action(*args):

  global found, device, look, look2
  
  #print 
  
  # Filter out non string arguments
  if len(args) == 0:
    # print "empty"
    return

  if type(args[0]) != dbus.String and type(args[0]) != dbus.ObjectPath:
    #print " not string ", type(args[0]), args[0]
    return

  look = "/org/freedesktop/UDisks/devices/"       
  look2 = "/org/freedesktop/Hal/devices/volume_uuid_"

  print "dbus: ", args[0]
  #print look

  #for aa in range(len(args)):
  #  print aa, args[aa],
  #print 
  #return

  # Handle removable drive:
  idx = args[0].find(look)
  #print idx

  if idx >= 0 and found == 0:
	#print "found0", args[0]
	found = 1
	device = args[0][len(look):]
	#print args[0][len(look):]

  if found == 1:
	idx2 = args[0].find(look2)
	if idx2 >= 0:
	   found = 2
	   devx = "/dev/" + device
	   print "Mounting", devx, "onto", args[0][len(look2):]
	   try:
	   	subprocess.call(["udisks", "--mount", devx]);
	   except:
		pass  #print "Subprocess exception"
	else:
	   found = 0

  # Handle power button:
  if len(args) == 2 and args[0] == "ButtonPressed" and args[1] == "power":
    # The action to perform when the power button is pressed
    print "Power button pressed!"
    subprocess.call(["beep", "-f104", "-l40", "-r2"]);


# Initialize the event loop
DBusGMainLoop(set_as_default=True)

# Connect to the System DBUS
system_bus = dbus.SystemBus()

# Declare an interest in DBUS signals
system_bus.add_signal_receiver(action)

print "Started listening"
# Wait for events
gobject.MainLoop().run()



