#!/usr/bin/env python

'''Application main window class
Demonstrates a typical application window, with menubar, toolbar, statusbar, 
            split pane, app position memory. '''

import signal, os, time
import gobject, gtk
import pydoc

(
  COLOR_RED,
  COLOR_GREEN,
  COLOR_BLUE
) = range(3)

(
  SHAPE_SQUARE,
  SHAPE_RECTANGLE,
  SHAPE_OVAL,
) = range(3)

ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
      <menuitem action='Exit'/>
    </menu>
    <menu action='PreferencesMenu'>
      <menu action='ColorMenu'>
        <menuitem action='Red'/>
        <menuitem action='Green'/>
        <menuitem action='Blue'/>
      </menu>
      <menu action='ShapeMenu'>
        <menuitem action='Square'/>
        <menuitem action='Rectangle'/>
        <menuitem action='Oval'/>
      </menu>
      <menuitem action='Bold'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar  name='ToolBar'>
    <toolitem action='New'/>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''
 
winx = 0
count = 15
count2 = 1
in_final = 0;
action = 0

# ------------------------------------------------------------------------
#  Define Application Main Window claass

class AppMainWindow(gtk.Window):

    def __init__(self, parent=None):

        register_stock_icons()
       
        # Create the toplevel window
        gtk.Window.__init__(self)

        global winx; winx = self

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

         #self.set_title(self.__class__.__name__)
        #self.set_default_size(500, 300)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Community Linux Password Prompt");

        merge = gtk.UIManager()
        self.set_data("ui-manager", merge)
        merge.insert_action_group(self.__create_action_group(), 0)
        self.add_accel_group(merge.get_accel_group())
        
        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "Building menus failed: %s" % msg

      	bar = merge.get_widget("/MenuBar")
        bar.show()

        table = gtk.Table(6, 3, False)
        self.add(table)
       
        self.lab = gtk.Label("Enter Password. ")		
        table.attach(self.lab,
            # X direction           Y direction
            0, 7,                   1, 2,
            #gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            gtk.SHRINK, gtk.SHRINK,
            20,                      20)

        labx = gtk.Label(" ")	;         laby = gtk.Label(" ")		
        
        table.attach(labx,
            # X direction           Y direction
            0, 1,                   2, 3,
            #gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            gtk.SHRINK, gtk.SHRINK,
            20,                      20)

        table.attach(laby,
            # X direction           Y direction
            6, 7,                   2, 3,
            #gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            gtk.SHRINK, gtk.SHRINK,
            20,                      20)

        #butt1 = gtk.Button("   _Shut Down   ")
        #butt1.show() ; butt1.set_use_underline(True)    
        #butt1.connect("clicked", shutd)
        
        #table.attach(butt1,
        #    # X direction           Y direction
        #    1, 2,                   2, 3,
        #    gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
        #    #gtk.SHRINK, gtk.SHRINK,
        #    10,                      10)

        lab1 = gtk.Label("Enter Password: ")        
        table.attach(lab1,
            # X direction           Y direction
            3, 4,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            #gtk.SHRINK, gtk.SHRINK,
            10,                      10)

        #text2 = gtk.TextView()
        #text2.set_cursor_visible(True)
        #text2.set_size_request(200, -1)
#        text2.set_border_width(1)
        #text2.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 1)
        #text2.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 1)
        #text2.set_border_window_size(gtk.TEXT_WINDOW_TOP, 1)
        #text2.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, 1)
        #text2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(100,100,00))
        #text2.set_border_window_size(gtk.TEXT_WINDOW_LEFT | gtk.TEXT_WINDOW_LEFT, 10)
        #buffer = text2.get_buffer()
        # buffer.insert_at_cursor("")
        
        text2 = gtk.Entry()
        text2.set_visibility(False)
        #text2.connect("insert-at-cursor", ekey, 100)
        text2.connect("key-press-event",  ekey, self)

        table.attach(text2,
            # X direction           Y direction
            4, 5,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            #gtk.SHRINK, gtk.SHRINK,
            20,                      20)
    
        butt2 = gtk.Button("   Set Pass   ")
        butt2.show() ; butt2.set_use_underline(True)
        butt2.connect("clicked", reboo)

        table.attach(butt2,
            # X direction           Y direction
            5, 6,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            #gtk.SHRINK, gtk.SHRINK,
            20,                      20)

        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                                gtk.gdk.POINTER_MOTION_HINT_MASK |
                                gtk.gdk.BUTTON_PRESS_MASK |
                                gtk.gdk.BUTTON_RELEASE_MASK |
                                gtk.gdk.KEY_PRESS_MASK |
                                gtk.gdk.KEY_RELEASE_MASK )

        self.connect("window_state_event", self.update_resize_grip)
        self.connect("destroy", OnExit)
        self.connect("key-press-event", area_key)

        #self.update_statusbar(buffer)

        self.show_all()

        # Set the signal handler for 1s tick
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)

# ------------------------------------------------------------------------

    def area_motion(self, area, event):
        #print "motion event", event
        pass

    def __create_action_group(self):
        # GtkActionEntry
        entries = (
          ( "FileMenu", None, "_File" ),               # name, stock id, label
          ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
          ( "ColorMenu", None, "_Color"  ),            # name, stock id, label
          ( "ShapeMenu", None, "_Shape" ),             # name, stock id, label
          ( "HelpMenu", None, "_Help" ),               # name, stock id, label
          ( "New", gtk.STOCK_NEW,                      # name, stock id
            "_New", "<control>N",                      # label, accelerator
            "Create a new file",                       # tooltip
            self.activate_action ),
          ( "Open", gtk.STOCK_OPEN,                    # name, stock id
            "_Open","<control>O",                      # label, accelerator
            "Open a file",                             # tooltip
            self.activate_action ),
          ( "Save", gtk.STOCK_SAVE,                    # name, stock id
            "_Save","<control>S",                      # label, accelerator
            "Save current file",                       # tooltip
            self.activate_action ),
          ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
            "Save _As...", None,                       # label, accelerator
            "Save to a file",                          # tooltip
            self.activate_action ),
          ( "Quit", gtk.STOCK_QUIT,                    # name, stock id
            "_Quit", "<control>Q",                     # label, accelerator
            "Quitx",                                    # tooltip
             self.activate_quit ),
          ( "Exit", gtk.STOCK_QUIT,                    # name, stock id
            "_Exit", "<alt>X",                         # label, accelerator
            "Exit program",                            # tooltip
             self.activate_quit ),          
          ( "About", None,                             # name, stock id
            "_About", "<control>A",                    # label, accelerator
            "About",                                   # tooltip
            self.activate_about ),
          ( "Logo", "demo-gtk-logo",                   # name, stock id
             None, None,                              # label, accelerator
            "GTK+",                                    # tooltip
            self.activate_action ),
        );

        # GtkToggleActionEntry
        toggle_entries = (
          ( "Bold", gtk.STOCK_BOLD,                    # name, stock id
             "_Bold", "<control>B",                    # label, accelerator
            "Bold",                                    # tooltip
            self.activate_action,
            True ),                                    # is_active
        )

        # GtkRadioActionEntry
        color_entries = (
          ( "Red", None,                               # name, stock id
            "_Red", "<control><shift>R",               # label, accelerator
            "Blood", COLOR_RED ),                      # tooltip, value
          ( "Green", None,                             # name, stock id
            "_Green", "<control><shift>G",             # label, accelerator
            "Grass", COLOR_GREEN ),                    # tooltip, value
          ( "Blue", None,                              # name, stock id
            "_Blue", "<control><shift>B",              # label, accelerator
            "Sky", COLOR_BLUE ),                       # tooltip, value
        )

        # GtkRadioActionEntry
        shape_entries = (
          ( "Square", None,                            # name, stock id
            "_Square", "<control><shift>S",            # label, accelerator
            "Square",  SHAPE_SQUARE ),                 # tooltip, value
          ( "Rectangle", None,                         # name, stock id
            "_Rectangle", "<control><shift>R",         # label, accelerator
            "Rectangle", SHAPE_RECTANGLE ),            # tooltip, value
          ( "Oval", None,                              # name, stock id
            "_Oval", "<control><shift>O",              # label, accelerator
            "Egg", SHAPE_OVAL ),                       # tooltip, value
        )

        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("AppWindowActions")
        action_group.add_actions(entries)
        action_group.add_toggle_actions(toggle_entries)
        action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
        action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

        return action_group

    def activate_about(self, action):
        dialog = gtk.AboutDialog()
        dialog.set_name("Hello World")
        dialog.set_version("1.0");
        dialog.set_comments("\nPyGTK Extended Hello\n");
        dialog.set_copyright("\302\251 Copyright Peter Glen")

        try:
	        pixbuf = gtk.gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
                #print "loaded pixbuf"
                dialog.set_logo(pixbuf)
    
        except gobject.GError, error:
            print "Cannot load logo for about dialog";

        #dialog.set_website("")
        ## Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_quit(self, action):
        print "Exit called"        
        gtk.main_quit()

    def activate_radio_action(self, action, current):
        active = current.get_active()
        value = current.get_current_value()

        if active:
            dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                "You activated radio action: \"%s\" of type \"%s\".\nCurrent value: %d" %
                (current.get_name(), type(current), value))

            # Close dialog on user response
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()

    def update_statusbar(self, buffer):
        # clear any previous message, underflow is allowed
        #self.statusbar.pop(0)
        #count = buffer.get_char_count()
        #iter = buffer.get_iter_at_mark(buffer.get_insert())
        #row = iter.get_line()
        #col = iter.get_line_offset()
        #self.statusbar.push(0,
        #'Cursor at row %d column %d - %d chars in document' % (row, col, count))
        pass

    def update_resize_grip(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))

    
# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.

def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = gtk.IconFactory()
    factory.add_default()

    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
    #print img_path
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
        # Register icon to accompany stock item
     
        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        icon_set = gtk.IconSet(transparent)
        factory.add('demo-gtk-logo', icon_set)

    except gobject.GError, error:
        #print 'failed to load GTK logo ... trying local'
        try:
		    #img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
		    pixbuf = gtk.gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
		    # Register icon to accompany stock item
		    # The gtk-logo-rgb icon has a white background, make it transparent
		    # the call is wrapped to (gboolean, guchar, guchar, guchar)
		    transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
		    icon_set = gtk.IconSet(transparent)
		    factory.add('demo-gtk-logo', icon_set)

        except gobject.GError, error:
            #print 'failed to load GTK logo for toolbar'
            pass

def ekey(self, strg, user1):
    #print "Pass window key press event", strg
    #print strg.keyval
    if strg.keyval == 65293:
        print "return pressed text=", self.get_text()
        user1.activate_action(user1)
    
# Callback for cleanup

def OnExit(arg):
    signal.alarm(0)
    print "OnExit called \"" + arg.get_title() + "\""
    arg.set_title("Exiting ...")
    #time.sleep(5);         
               
def shutd(arg1):
    global winx, count, in_final, action
    action = 1;
    print "Shutdown clicked"
    winx.lab.set_text("Shutting down ...")    
    in_final = True;

def reboo(arg1):
    global winx, count, in_final, action; 
    print "reboo clicked"
    winx.lab.set_text("Rebooting ...")    
    action = 2
    in_final = True;
    
def cance(arg1):
    global winx, count, in_final; 
    print "Cancel clicked"
    winx.lab.set_text("Cancelling ...")    
    in_final = True;

def area_key(area, event):
    global winx, count, in_final; 
    #print "area ", area, " key event ", key.hardware_keycode, \
    #     key.keyval, key
    if event.keyval == 65307:
        print "Cancel pressed"
        winx.lab.set_text("Cancelling ...")    
        in_final = True;
        
def handler(signum, frame):
    global count, winx, count2

    if  in_final:
        count2 -=1
        if count2 == 0:
            #winx.destroy()
            gtk.main_quit()         
            pass
    else:
        #print 'Signal handler called with signal', signum
        strx = "System will shut down in " + str(count) + " seconds "
        winx.lab.set_text(strx)    
        if count == 0:
            shutd(0)        

    signal.alarm(1)
    count -= 1


