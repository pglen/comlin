# A collection of obsolete code while writing pyedit

def handle_keys(host):

    # Do key down:
    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Alt_L or \
                event.keyval == gtk.keysyms.Alt_R:
            #print "Alt down"
            host.alt = True; 
        elif event.keyval == gtk.keysyms.Control_L or \
                event.keyval == gtk.keysyms.Control_R:
            #print "Ctrl down"
            self.ctrl = True; ret = True
        if event.keyval == gtk.keysyms.Shift_L or \
              event.keyval == gtk.keysyms.Shift_R:
            #print "shift down"
            host.shift = True;

    # Do key up
    elif  event.type == gtk.gdk.KEY_RELEASE:
        if event.keyval == gtk.keysyms.Alt_L or \
              event.keyval == gtk.keysyms.Alt_R:
            #print "Alt up"
            host.alt = False;
        if event.keyval == gtk.keysyms.Control_L or \
              event.keyval == gtk.keysyms.Control_R:
            #print "Ctrl up"
            host.ctrl = False;
        if event.keyval == gtk.keysyms.Shift_L or \
              event.keyval == gtk.keysyms.Shift_R:
            #print "shift up"
            host.shift = False; 
        

