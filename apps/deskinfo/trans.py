#!/usr/bin/env python

import gobject
import gtk
import time
import signal, os, time
import logging
import cairo

'''
The expose event handler for the window.

This function performs the actual compositing of the event box onto
the already-existing background of the window at 50% normal opacity.

In this case we do not want app-paintable to be set on the widget
since we want it to draw its own (red) background. Because of this,
however, we must ensure that we use g_signal_register_after so that
this handler is called after the red has been drawn. If it was
called before then GTK would just blindly paint over our work.

Note: if the child window has children, then you need a cairo 1.16
feature to make this work correctly.
'''

image = None;

'''xx'''
# ------------------------------------------------------------------------

def transparent_expose(widget, event):

    print "transparent_expose"

    #cr = widget.window.cairo_create()
    #cr.set_operator(cairo.OPERATOR_CLEAR)
    
    # Ugly but we don't have event.region
    #region = gtk.gdk.region_rectangle(event.area)
    
    #cr.region(region)
    #cr.fill()
    
    return False

# ------------------------------------------------------------------------

def window_expose_event(widget, event):
    
    global image

    print "window_expose_event image"

    #, image, "area", event.area
    #return False

    #get our child (in this case, the event box)
    child = widget.get_child()
    
    #create a cairo context to draw to the window
    cr = widget.window.cairo_create()

    #the source data is the (composited) event box
    cr.set_source_pixmap (child.window,
                          child.allocation.x,
                          child.allocation.y)

    #draw no more than our expose event intersects our child
    region = gtk.gdk.region_rectangle(child.allocation)
    r = gtk.gdk.region_rectangle(event.area)
    region.intersect(r)
    cr.region (region)
    cr.clip()

    gc = child.style.fg_gc[gtk.STATE_NORMAL]
    
    x=10; y=10
    points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                 (x+30,y+10), (x+50,y+10)]

    child.window.draw_points(gc, points)

    #composite, with a 50% opacity
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.paint_with_alpha(0.5)

    return False

# Make the widgets
w = gtk.Window()
#w.set_decorated(False)

#w.resize(100,100)       

w.set_default_size(500, 300)
w.set_position(gtk.WIN_POS_CENTER)
        
b = gtk.Button("A Button")
e = gtk.EventBox()
        
#print gtk.gdk.Screen.get_width(gtk.gdk.Screen())
print "Monitors:", gtk.gdk.Screen.get_n_monitors(gtk.gdk.Screen()),
print "width:", gtk.gdk.screen_width(),  "height:", gtk.gdk.screen_height()

rw = gtk.gdk.Screen.get_root_window(gtk.gdk.Screen())

print "root window ", rw

    

#listx=gtk.gdk.DisplayManager.list_displays(gtk.gdk.display_manager_get())
#for aa in listx:
#    print aa

# Put a xxx background on the window
#col = gtk.gdk.color_parse("blue")
#w.modify_bg(gtk.STATE_NORMAL, col)

# Set the colourmap for the event box.
# Must be done before the event box is realised.
#screen = e.get_screen()
#rgba = screen.get_rgba_colormap()
#e.set_colormap(rgba)

# Set our event box to have a fully-transparent background
# drawn on it. Currently there is no way to simply tell GTK+
# that "transparency" is the background colour for a widget.
#e.set_app_paintable(True)
#e.connect("expose-event", transparent_expose)

# Put them inside one another
w.set_border_width(20)
#w.add(e)

#e.add(b)
#e.add(laby)
w.set_app_paintable(True)


# Realise and show everything
w.show_all()

w.window.set_composited(True)
w.connect("expose-event", window_expose_event)

screen = w.get_screen()
rgba = screen.get_rgba_colormap()
#w.set_colormap(rgba)

pixmap, mask = gtk.gdk.pixmap_create_from_xpm(w.window, None, "/usr/share/pixmaps/keys.xpm")
image = gtk.Image()
image.set_from_pixmap(pixmap, mask)

#print "image", image
#image.show()
w.add(image)
#w.shape_combine_mask(pix[0], 0,0)
#print w.__doc__

# Set the event box GdkWindow to be composited.
# Obviously must be performed after event box is realised.
#e.window.set_composited(True)

# Set up the compositing handler.
# Note that we do _after_ so that the normal (red) background is drawn
# by gtk before our compositing occurs.


#w.connect_after("expose-event", window_expose_event)
#w.connect_after("expose-event", transparent_expose)

gtk.main()

