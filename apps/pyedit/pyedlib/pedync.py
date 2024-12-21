#!/usr/bin/env python

# Prompt Handler for pyedit

import os, string, gtk, gobject
import pyedlib.pedconfig
# ------------------------------------------------------------------------

def yes_no_cancel(title, message, cancel = True):

    dialog = gtk.Dialog(title,
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

    dialog.set_default_response(gtk.RESPONSE_YES)
    sp = "     "
    label = gtk.Label(message); 
    label2 = gtk.Label(sp);     label3 = gtk.Label(sp)
    hbox = gtk.HBox() ;         hbox.pack_start(label2);  
    hbox.pack_start(label);     hbox.pack_start(label3)
    dialog.vbox.pack_start(hbox)

    dialog.add_button("_Yes", gtk.RESPONSE_YES)
    dialog.add_button("_No", gtk.RESPONSE_NO)
    
    if cancel:
        dialog.add_button("_Cancel", gtk.RESPONSE_CANCEL)

    dialog.connect("key-press-event", area_key, cancel)
    #dialog.connect("key-release-event", area_key, cancel)
    dialog.show_all()
    response = dialog.run()       
    # Convert all responses to cancel
    if  response == gtk.RESPONSE_CANCEL or \
        response == gtk.RESPONSE_REJECT or \
        response == gtk.RESPONSE_CLOSE  or \
        response == gtk.RESPONSE_DELETE_EVENT:
        response = gtk.RESPONSE_CANCEL        
    dialog.destroy()
    return  response 

def area_key(win, event, cancel):
    #print event
    if event.keyval == gtk.keysyms.y or \
        event.keyval == gtk.keysyms.Y:
        win.response(gtk.RESPONSE_YES)
    if event.keyval == gtk.keysyms.n or \
        event.keyval == gtk.keysyms.N:
        win.response(gtk.RESPONSE_NO)

    if cancel:
        if event.keyval == gtk.keysyms.c or \
            event.keyval == gtk.keysyms.C:
            win.response(gtk.RESPONSE_CANCEL)

# ------------------------------------------------------------------------
# Show About dialog:

def  about():
    dialog = gtk.AboutDialog()
    dialog.set_name(" PyEdit - Python Editor ")
    dialog.set_version(str(pyedlib.pedconfig.conf.version));
    comm = "\nPython based easily configurable editor.\n"\
        "\nRunning PyGtk %d.%d.%d" % gtk.pygtk_version +\
        "\nRunning GTK %d.%d.%d\n" % gtk.gtk_version  
    dialog.set_comments(comm);
    dialog.set_copyright("Portions \302\251 Copyright Peter Glen\n"
                          "Project placed in the Public Domain.")

    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')

    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
        #print "loaded pixbuf"
        dialog.set_logo(pixbuf)

    except gobject.GError, error:
        print "Cannot load logo for about dialog";

    #dialog.set_website("")

    ## Close dialog on user response
    dialog.connect ("response", lambda d, r: d.destroy())
    dialog.connect("key-press-event", about_key)

    dialog.show()

def about_key(win, event):
    #print "about_key", event
    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
            if event.state & gtk.gdk.MOD1_MASK:
                win.destroy()
    
# Show a regular message:

def message(strx, title = None, icon = gtk.MESSAGE_INFO):

    dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        icon, gtk.BUTTONS_CLOSE, strx)
       
    if title:
        dialog.set_title(title)
    else:
        dialog.set_title("pyedit")

    # Close dialog on user response
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show()


















