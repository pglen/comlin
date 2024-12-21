#!/usr/bin/python

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import subprocess

found  = 0
device = ""

def action(*args):

  # Filter out non string arguments
  if len(args) == 0:
    # print "empty"
    return

  if type(args[0]) != dbus.String and type(args[0]) != dbus.ObjectPath:
    #print " not string ", type(args[0]), args[0]
    return

  # Handle power button:
  if len(args) == 2 and args[0] == "ButtonPressed" and args[1] == "power":
    # The action to perform when the power button is pressed
    print "Power button pressed!"
    subprocess.call(["/usr/bin/python", "/apps/power/ctrl_alt_del.py"]);

 # Handle power button:
  if len(args) == 2 and args[0] == "ButtonPressed" and args[1] == "lid":
    # The action to perform when the power button is pressed
    print "Lid closed!", args
    #subprocess.call(["/usr/bin/python", "/apps/power/ctrl_alt_del.py"]);

# Initialize the event loop
DBusGMainLoop(set_as_default=True)

# Connect to the System DBUS
system_bus = dbus.SystemBus()

# Declare an interest in DBUS signals
system_bus.add_signal_receiver(action)

print "Started listening"
# Wait for events
gobject.MainLoop().run()

