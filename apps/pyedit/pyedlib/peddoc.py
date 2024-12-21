#!/usr/bin/env python

import signal, os, time, string, pickle
import gobject, gtk, pango

import keyhand, pedconfig, pedync, pedspell, pedmenu
from pedutil import *

VSCROLLGAP  = 2             # Gap between the page boundary and ver. scroll
HSCROLLGAP  = 4             # Gap between the page boundary and hor. scroll
PAGEUP      = 20            # One page worth of scroll
BOUNDLINE   = 80            # Boundary line for col 80 

# Do not redefine this here, as it is determined by the gtk (pango) lib
#TABSTOP = 8                 # One tab stop worth of spaces

# On version 0.21 (and after) we force GTK to assume our idea of tabstop.
# Even though we do not draw the tabs with GTK it is cleaner (simpler)
# this way. (See mess on tabs before V21)
TABSTOP = 4                 # One tab stop worth of spaces

# Profile line, use it on bottlenecks
#got_clock = time.clock()   
# profiled code here
#print  "Str", time.clock() - got_clock        

from keywords import *

# Globals

last_scanned = None
     
# Colors for the text, configure the defaults here

FGCOLOR  = "#000000"
RBGCOLOR = "#bbbbff"              
CBGCOLOR = "#ffbbbb"
KWCOLOR  = "#88aaff"
CLCOLOR  = "#880000"
COCOLOR  = "#4444ff"
STCOLOR  = "#ee44ee"
 
# UI specific values:

DRAGTRESH = 5                   # This many pixels for drag highlight
    
# ------------------------------------------------------------------------
# We create a custom class for display, as we want a text editor that 
# can take thousands of lines.

class pedDoc(gtk.DrawingArea):

    def __init__(self, buff, appwin, readonly = False):
        
        # Save params
        self.appwin = appwin; 
        self.readonly = readonly      

        # Gather globals
        self.keyh = pedconfig.conf.keyh

        # Init vars
        self.xpos = 0; self.ypos = 0
        self.changed = False; 
        self.src_changed = False
        self.needscan = True; 
        self.record = False; 
        self.recarr = []                # Macros
        self.undoarr = []               # Undo
        self.redoarr = []               # Redo
        self.queue = []                 # Idle tasks
        self.colsel = False
        self.oldsearch = ""
        self.oldgoto = ""
        self.oldrep = ""
        self.xsel = -1; self.ysel = -1
        self.xsel2 = -1; self.ysel2 = -1
        self.mx = -1; self.my = -1    
        self.caret = []; self.caret.append(0); self.caret.append(0)        
        self.focus = False
        self.insert = True       
        self.startxxx = -1;  self.startyyy = -1
        self.hex = False
        self.colflag = True
        self.acorr = True
        self.scol = False        
        self.accum = []; 
        self.tokens = [];
        self.ularr = []
        self.bigcaret = False                
        self.stab = False                
        self.honeshot = False                
        self.initial_undo_size = 0
        self.initial_redo_size = 0
        self.spell = False
        self.spellmode = False
        # Init configurables
        self.vscgap = VSCROLLGAP      
        self.hscgap = HSCROLLGAP      
        self.pgup  = PAGEUP
        self.tabstop = TABSTOP
        # Process buffer into list
        self.text = buff
        self.maxlinelen = 0
        self.maxlines = 0
        self.fired = 0
        self.countup = 0
        self.nokey = False 
        self.newword = False
        
        # Parent widget                 
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        
        # Our font
        fsize  =  pedconfig.conf.sql.get_int("fsize")
        fname  =  pedconfig.conf.sql.get_str("fname")
        if fsize == 0: fsize = 14
        if fname == "": fname = "Monospace"
        
        self.setfont(fname, fsize)
        
        if self.readonly:
            self.set_tooltip_text("Read only buffer")
        
        # Create scroll items        
        sm = len(self.text) + self.get_height() / self.cyy + 10        
        self.hadj = gtk.Adjustment(0, 0, self.maxlinelen, 1, 15, 25);
        self.vadj = gtk.Adjustment(0, 0, sm, 1, 15, 25)
        
        self.vscroll = gtk.VScrollbar(self.vadj)
        self.hscroll = gtk.HScrollbar(self.hadj)
        
        # We connect scrollers after construction
        self.hadj.connect("value-changed", self.hscroll_cb)
        self.vadj.connect("value-changed", self.vscroll_cb)

        self.set_events(    gtk.gdk.ALL_EVENTS_MASK )
        self.colormap = gtk.widget_get_default_colormap()
        self.setcol()
        
        # Set default background color
        if self.readonly:
            color = self.colormap.alloc_color("#d8d8d8")
            self.modify_bg(gtk.STATE_NORMAL, color)
        
        self.connect("expose-event", self.area_expose_cb)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect("key-release-event", self.area_key)
        self.connect("focus", self.area_focus)
        self.connect("configure_event", self.configure_event)
        self.connect("size-request", self.size_request)
        self.connect("size-allocate", self.size_alloc)    
        self.connect("scroll-event", self.scroll_event)    
        self.connect("focus-in-event", self.focus_in_cb)    
        self.connect("focus-out-event", self.focus_out_cb)    
        
    # Customize your colors here
    def setcol(self):        
    
        ccc = pedconfig.conf.sql.get_str("fgcolor")
        if ccc == "":
            self.fgcolor  = self.colormap.alloc_color(FGCOLOR)              
        else: 
            self.fgcolor  = self.colormap.alloc_color(ccc)              
        
        ccc = pedconfig.conf.sql.get_str("rbgcolor")
        if ccc == "":
            self.rbgcolor = self.colormap.alloc_color(RBGCOLOR)              
        else: 
            self.rbgcolor = self.colormap.alloc_color(ccc)              
        
        ccc = pedconfig.conf.sql.get_str("cbgcolor")
        if ccc == "":
            self.cbgcolor = self.colormap.alloc_color(CBGCOLOR)              
        else: 
            self.cbgcolor = self.colormap.alloc_color(ccc)              
        
        ccc = pedconfig.conf.sql.get_str("kwcolor")
        if ccc == "":
            self.kwcolor = self.colormap.alloc_color(KWCOLOR)              
        else: 
            self.kwcolor = self.colormap.alloc_color(ccc)              
       
        ccc = pedconfig.conf.sql.get_str("clcolor")
        if ccc == "":
            self.clcolor = self.colormap.alloc_color(CLCOLOR)              
        else: 
            self.clcolor = self.colormap.alloc_color(ccc)              
        
        ccc = pedconfig.conf.sql.get_str("cocolor")
        if ccc == "":
            self.cocolor = self.colormap.alloc_color(COCOLOR)              
        else: 
            self.cocolor = self.colormap.alloc_color(ccc)              
       
        ccc = pedconfig.conf.sql.get_str("stcolor")
        if ccc == "":
            self.stcolor = self.colormap.alloc_color(STCOLOR)              
        else: 
            self.stcolor = self.colormap.alloc_color(ccc)              
       
    def setfont(self, fam, size):
    
        self.pangolayout = self.create_pango_layout("a")
        fd = pango.FontDescription()
        fd.set_family(fam)
        fd.set_size(size * pango.SCALE); 
        self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        
        # Get Pango tabs
        self.tabarr = pango.TabArray(80, False)
        for aa in range(self.tabarr.get_size()):
            self.tabarr.set_tab(aa, pango.TAB_LEFT, aa * TABSTOP * self.cxx * pango.SCALE)
                
        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()
        
        if ts != None: 
            al, self.tabstop = ts.get_tab(1)
        self.tabstop /= self.cxx * pango.SCALE
        
    def  set_maxlinelen(self, mlen = -1, ignore = True):
        if mlen == -1: self.calc_maxline()  
        self.maxlinelen = mlen
        self.oneshot = ignore
        self.hadj.set_all(0, 0, self.maxlinelen * 2, 1, 15, 25);
        
    def  set_maxlines(self, lines = 0, ignore = True):              
        self.maxlines = len(self.text) + self.get_height() / self.cyy + 25
        self.oneshot = ignore
        self.vadj.set_all(0, 0, self.maxlines, 1, 15, 25);
                
    # Do Tasks  when the system is idle
    def idle_callback(self):
        #print "Idle callback"
        gobject.source_remove(self.source_id)        
        try:
            if self.changed:
                hhh = hash_name(self.fname) + ".sav"           
                xfile = pedconfig.conf.data_dir + "/" + hhh
                writefile(xfile, self.text)             
                strx = "Backed up file '{0:s}'".format(xfile)
                self.mained.update_statusbar(strx)
        except:
            print "Exception in idle handler", sys.exc_info()
            
    # Do Tasks2 when the system is idle
    def idle_callback2(self):
        #print "Idle callback2"
        gobject.source_remove(self.source_id2)        
        try:
            run_async_time(self)
        except:
            print "Exception in async handler", sys.exc_info()
        
    def locate(self, xstr):
        #print "locate '" + xstr +"'"        
        cnt = 0
        for line in self.text:
            idx = line.find(xstr)
            if idx >= 0:
                self.gotoxy(idx, cnt, len(xstr), True)
                break
            cnt += 1
        
    def focus_out_cb(self, widget, event):
        self.focus = False
        #print "focus_out_cb", widget, event    
    
    def focus_in_cb(self, widget, event):
        self.focus = True
        os.chdir(os.path.dirname(self.fname))
        self.update_bar2()
        self.needscan = True 
        self.do_chores()

        #print "focus_in_cb"
    
    def grab_focus_cb(self, widget):
        #print "grab_focus_cb", widget
        pass
        
    def area_enter(self, widget, event):
        #print "area_enter"
        pass
        
    def area_leave(self, widget, event):
        #print "area_leave"
        pass
        
    def scroll_event(self, widget, event):    
        #print "scroll_event"
        xidx = self.xpos + self.caret[0]
        yidx = self.ypos + self.caret[1]
        if event.direction == gtk.gdk.SCROLL_UP:
            yidx -= self.pgup / 2
        else:
            yidx += self.pgup / 2                    
        self.set_caret(xidx, yidx)
        self.invalidate()
        
    def hscroll_cb(self, widget):
        #print "hscroll_cb", widget.get_value()
        # Skip one callback
        if self.honeshot: 
            self.honeshot = False; return            
        xidx = int(widget.get_value())
        
        #print "hscroll_cb ok", widget.get_value()        
        self.set_caret(xidx, self.ypos + self.caret[1])        
        self.invalidate()

    def vscroll_cb(self, widget):
        #print "vscroll_cb", widget.get_value()
        # Skip one callback
        if self.oneshot: 
            self.oneshot = False; return
        #print "vscroll_cb ok", widget.get_value()
        yidx = int(widget.get_value())
        self.set_caret(self.xpos + self.caret[0], yidx)        
        self.invalidate()

    def size_request(self, widget, req):
        #print "size_request", req
        pass

    def size_alloc(self, widget, req):
        #print "size_alloc", req
        pass

    def configure_event(self, widget, event):
        #print "configure_event", event
        #self.grab_focus()
        #self.width = 0; self.height = 0
        #self.invalidate()
        #print self, event
        pass
        
    def _draw_text(self, gc, x, y, text, foreground = None, background = None):
        #print "draw_text"
        if self.hex:
            text2 = ""
            for aa in text:
                tmp = "%02x " % ord(aa)
                text2 += tmp                
            self.pangolayout.set_text(text2[self.xpos * 3:])            
        elif self.stab:
            text2 = "";  cnt = 0;
            for aa in text:
                if aa == " ":  text2 += "_"                
                elif aa == "\t":
                    spaces = self.tabstop - (cnt % self.tabstop)
                    cnt += spaces - 1
                    for bb in range(spaces): 
                        text2 += "o"
                else:
                    text2 += aa                                    
                cnt += 1
            self.pangolayout.set_text(text2[self.xpos:])            
        else:
            self.pangolayout.set_text(text[self.xpos:])
            
        xx, yy = self.pangolayout.get_pixel_size()
        self.window.draw_layout(gc, x, y, self.pangolayout, foreground, background)
        
        if self.scol:
            hhh = self.get_height()     
            pos = BOUNDLINE - self.xpos       
            self.window.draw_line(gc, pos * self.cxx, 0, pos * self.cxx, hhh)            
        
        return xx, yy
	
    def area_expose_cb(self, area, event):

        #print "area_expose_cb()", event.area.width, event.area.height
        
        # We have a window, goto start pos
        hhh = self.get_height()
        xlen = len(self.text)

        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        
        colormap = gtk.widget_get_default_colormap()        
        gcr.set_foreground(colormap.alloc_color("#ff0000"))

        #got_clock = time.clock()   
            
        # Paint text        
        xx = 0; yy = 0; 
        cnt = self.ypos;
        while cnt <  xlen:
            # Got fed up with tabs, generate an untabbed copy for drawing
            if self.hex or self.stab:
               text3 = self.text[cnt]
            else: 
               text3 = untab_str(self.text[cnt], self.tabstop)
               
            #print "'" + text3 + "'"
            
            dx, dy = self._draw_text(gcx, xx, yy, text3, self.fgcolor)
            cnt += 1
            yy += dy
            if yy > hhh:
                break

        # Do not paint color on hex:
        if self.hex or self.stab:
            self._drawcaret()        
            return True

        # Paint selection        
        xx = 0; yy = 0; 
        cnt = self.ypos;
    
        # Normalize (Read: [xy]ssel - startsel  [xy]esel - endsel
        xssel = min(self.xsel, self.xsel2)
        xesel = max(self.xsel, self.xsel2)
        yssel = min(self.ysel, self.ysel2)
        yesel = max(self.ysel, self.ysel2)
        # Override
        if not self.colsel:  
            if yssel != yesel:
                xssel = self.xsel
                xesel = self.xsel2
       
        draw_start = xssel
        if xssel != -1:
            if self.colsel: bgcol = self.cbgcolor
            else: bgcol = self.rbgcolor
            
            while cnt <  xlen:
                if cnt >= yssel and cnt <= yesel:
                    line = self.text[cnt]
                    if self.colsel:
                        frag = line[xssel:xesel]
                    else :   # Startsel - endsel                        
                        if cnt == yssel and cnt == yesel:   # sel on the same line
                            frag = line[xssel:xesel]
                        elif cnt == yssel:                  # start line
                            frag = line[xssel:]
                        elif cnt == yesel:                  # end line
                            draw_start = 0
                            frag = line[:xesel]
                        else:
                            draw_start = 0                  # intermediate line
                            frag = line[:]

                    dss = calc_tabs(line, draw_start, self.tabstop)
                    self._draw_text(gcx, dss * self.cxx, yy, frag, self.fgcolor, bgcol)
                    
                cnt = cnt + 1
                yy += self.cyy
                if yy > hhh:
                    break

        #print  "sel", time.clock() - got_clock        
       
        if self.colflag:
            # Color keywords. Very primitive coloring, a compromise for speed
            xx = 0; yy = 0; 
            cnt = self.ypos;
            while cnt <  xlen:
                #line = self.text[cnt]
                line =  untab_str(self.text[cnt])
                for kw in keywords:
                    ff = 0          # SOL
                    while True:
                        ff = line.find(kw, ff)
                        if ff >= 0:
                            ff2 = calc_tabs(line, ff, self.tabstop)                    
                            self._draw_text(gcx, ff2 * self.cxx, yy, line[ff:ff+len(kw)],
                                self.kwcolor, None)
                            ff += len(kw)
                            #break
                        else:        
                            break
                        
                for kw in clwords:
                    cc = 0      # SOL
                    while True:
                        cc = line.find(kw, cc)
                        if cc >= 0:
                            cc2 = calc_tabs(line, cc, self.tabstop)                    
                            self._draw_text(gcx, cc2 * self.cxx, yy, line[cc:cc+len(kw)],
                                self.clcolor, None)
                            cc += len(kw)
                        else:        
                            break
                        
                # Comments: # or // and "     
                ccc = line.find("#"); 
                if ccc < 0:
                    ccc = line.find("//"); 
                    
                cccc = line.find('"')
    
                # See if hash preceeds quote (if any)
                if ccc >= 0 and (cccc > ccc or cccc == -1):
                    ccc -= self.xpos
                    ccc2 = calc_tabs(line, ccc, self.tabstop)                    
                    self._draw_text(gcx, ccc2 * self.cxx, yy, line[ccc:],
                            self.cocolor, None)
                else:   
                    qqq = 0                                 
                    while True:
                        quote = '"'
                        sss = qqq
                        qqq = line.find(quote, qqq);                     
                        if qqq < 0:
                            # See if single quote is found
                            qqq = line.find("'", sss); 
                            if qqq >= 0:
                                quote = '\''                    
                        if qqq >= 0:
                            qqq += 1
                            qqqq = line.find(quote, qqq)
                            if qqqq >= 0:
                                qqq -= self.xpos           
                                qqq2 = calc_tabs(line, qqq, self.tabstop)
                                self._draw_text(gcx, 
                                        qqq2 * self.cxx, yy, line[qqq:qqqq], self.stcolor, None)
                                qqq = qqqq + 1
                            else:
                                break
                        else:
                            break
                            
                cnt = cnt + 1
                yy += self.cyy
                if yy > hhh:
                    break
        
        # Underline spelling errors
        yyy = self.ypos + self.get_height() / self.cyy             
        for xaa, ybb, lcc in self.ularr:
            # Draw within visible range
            if ybb >= self.ypos and ybb < yyy:
                ybb -= self.ypos; 
                xaa -= self.xpos; lcc -= self.xpos;
                self.draw_wiggle(gcr, 
                     xaa * self.cxx, ybb * self.cyy + self.cyy,
                            lcc * self.cxx, ybb * self.cyy + self.cyy)
            
        #print  "kw", time.clock() - got_clock        
    
        if self.startxxx != -1:
            self.gotoxy(self.startxxx, self.startyyy)
            self.startxxx = -1; self.startyyy = -1
        
        self._drawcaret()        
        return True

    # Underline red
    def draw_wiggle(self, gcr, xx, yy, xx2, yy2):

        # The  wiggle took too much processing power .... just a line
        self.window.draw_line(gcr, xx, yy, xx2, yy2)
    
        '''while True:
            xx3 = xx + 8        
            if xx3 >= xx2: break   
            self.window.draw_line(gcr, xx, yy, xx3, yy2+1)
            xx3 = xx3 + 8
            if xx3 >= xx2: break   
            #self.window.draw_line(gcr, xx, yy, xx3, yy2)            
            xx = xx3 '''
                      
    def idle_queue(func):
        self.queue.append(func)
        #print queue
    
    # --------------------------------------------------------------------
    # Draw caret

    def _drawcaret(self):

        #print "drawing caret", self.caret[0], self.caret[1], \
        #        self.caret[0] * self.cxx, self.caret[1] * self. cyy  
                        
        colormap = gtk.widget_get_default_colormap()
        if self.focus:    
            color = colormap.alloc_color("#008888")
        else:
            color = colormap.alloc_color("#aaaaaa")
        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcx.set_foreground(color)
      
        try:
            line = self.text[self.ypos + self.caret[1]]            
        except:
            line = ""
        
        xxx = calc_tabs2(line[self.xpos:], self.caret[0], self.tabstop)      
        xx = xxx * self.cxx               
        #xx = self.caret[0] * self.cxx       
        yy = self.caret[1] * self.cyy

        ch = self.cyy / 2; cw = self.cxx / 2

        # Order: Top, left right, buttom
        if self.focus:    
            # Flash cursor
            if self.bigcaret:
                rxx = xx + self.cxx
                ly = yy + self.cyy; uy = yy
                mmx = xx + cw; mmy = yy + ch
                dist = 80
                self.window.draw_line(gcx, mmx - dist, uy, mmx + dist, uy)
                self.window.draw_line(gcx, mmx - dist, ly, mmx + dist, ly)
                self.window.draw_line(gcx, xx , mmy - dist, xx, mmy + dist)        
                self.window.draw_line(gcx, rxx , mmy - dist, rxx, mmy + dist)        
            else:
                if self.insert:
                    self.window.draw_line(gcx, xx, yy, xx + cw, yy)
                    self.window.draw_line(gcx, xx + 1, yy, xx + 1, yy + self.cyy )
                    self.window.draw_line(gcx, xx + 3, yy, xx + 3, yy + self.cyy )
                    self.window.draw_line(gcx, xx , yy + self.cyy, xx + cw, yy + self.cyy )
                else:
                    self.window.draw_line(gcx, xx, yy, xx + cw, yy)
                    self.window.draw_line(gcx, xx + 1, yy, xx + 1, yy + self.cyy )
                    self.window.draw_line(gcx, xx + 2, yy, xx + 2, yy + self.cyy )
                    self.window.draw_line(gcx, xx + 3, yy, xx + 3, yy + self.cyy )
                    self.window.draw_line(gcx, xx + 4, yy, xx + 4, yy + self.cyy )
                    self.window.draw_line(gcx, xx , yy + self.cyy, xx + cw, yy + self.cyy )                
        else:
            #self.window.draw_line(gcx, xx, yy, xx + cw, yy)
            self.window.draw_line(gcx, xx + 1, yy + 2, xx + 1, yy -2 + self.cyy )
            self.window.draw_line(gcx, xx + 3, yy + 2, xx + 3, yy -2 + self.cyy )
            #self.window.draw_line(gcx, xx , yy + self.cyy, xx + cw, yy + self.cyy )

    def area_button(self, area, event):

        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                #print "Left Click at x=", event.x, "y=", event.y
    
                self.mx = event.x; self.my = event.y
                # Find current pos
                self.set_caret(self.xpos + int(event.x) / self.cxx, 
                                     self.ypos + int(event.y) / self.cyy )
                # Erase selection
                if self.xsel != -1:
                    self.clearsel()

            if event.button == 3:
                #print "Right Cldick at x=", event.x, "y=", event.y
                flag = False; xx = 0; yy = 0; zz = 0
                if self.spell:                    
                    yyy = self.ypos + self.get_height() / self.cyy             
                    for xaa, ybb, lcc in self.ularr:
                        # Look witdhin visible range
                        if ybb >= self.ypos and ybb < yyy:
                            ybb -= self.ypos; 
                            xaa -= self.xpos; lcc -= self.xpos;
                            xaa *= self.cxx ; ybb *= self.cyy 
                            lcc *= self.cxx
                            yy2 = ybb + self.cyy
                           
                            if self.intersect(xaa, ybb, lcc, yy2, event):
                                xx = xaa / self.cxx + self.xpos
                                yy = ybb / self.cyy + self.ypos
                                zz = lcc / self.cxx + self.xpos
                                flag = True                             
                if flag:
                    line = self.text[yy];
                    #print "'" + line[xx:zz] + "'"
                    self.xsel = xx; self.xsel2 = zz
                    self.ysel = self.ysel2 = yy
                    self.popspell(area, event, line[xx:zz] )
                else: 
                    self.poprclick(area, event)                       

        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            #print "button release", event.button 
            self.mx = -1; self.my = -1                
            ttt = "Release"
        elif  event.type == gtk.gdk._2BUTTON_PRESS:
            self.mx = event.x; self.my = event.y
            # Find current pos
            self.set_caret(self.xpos + int(event.x) / self.cxx, 
                                 self.ypos + int(event.y) / self.cyy )
            # Erase selection
            if self.xsel != -1:
                self.clearsel()
            # Select word
            if event.state & gtk.gdk.CONTROL_MASK:
                pedconfig.conf.keyh.act.alt_l(self)
            elif event.state & gtk.gdk.SHIFT_MASK:
                pedconfig.conf.keyh.act.ctrl_b(self)
            else: 
                pedconfig.conf.keyh.act.alt_v(self)
        else:
            print "Unexpected mouse op."
            
        self.grab_focus()
        return True

    # See if point in rect
    def intersect(self, xx, yy, xx2, yy2, event):
        # Does X intersect?
        if event.x > xx and event.x < xx2:
            #print "x inter", xaa, lcc
            # Does Y intersect?
            if event.y > yy and event.y < yy2:
                return True 
        return False 
        
    # Normalize 
    def normsel(self):                                                
        xssel = min(self.xsel, self.xsel2)
        xesel = max(self.xsel, self.xsel2)
        yssel = min(self.ysel, self.ysel2)
        yesel = max(self.ysel, self.ysel2)

        self.xsel  = xssel;  self.ysel  = yssel; 
        self.xsel2 = xesel;  self.ysel2 = yesel

    def pix2xpos(self, xx):
        return int(self.xpos + xx / self.cxx)

    def pix2ypos(self, yy):
        return int(self.ypos + yy / self.cyy)
   
    def pix2pos(self, xx, yy):
        return int(self.xpos + xx / self.cxx), int(self.ypos + yy / self.cyy)
        
    def area_motion(self, area, event):    
        #print "motion event", event.state, event.x, event.y        
        if event.state & gtk.gdk.BUTTON1_MASK:            
            if self.xsel == -1:
                begsel = False
                #print event.x - self.mx, event.y - self.my
                # Horiz drag - regular sel      
                if abs(event.x - self.mx) > DRAGTRESH:
                    self.colsel = False; begsel = True
                # Vert drag - colsel               
                elif abs(event.y - self.my) > DRAGTRESH:
                    self.colsel = True; begsel = True
                    
                if begsel:
                    self.xsel = self.xsel2 = self.pix2xpos(event.x) 
                    self.ysel = self.ysel2 = self.pix2ypos(event.y) 
                    #print "colsel xsel, ysel", self.colsel, self.xsel, self.ysel                    
            else: 
                # Already selected, mark 
                self.ysel2 = self.pix2ypos(event.y)                           
                if self.ysel2 < self.ysel:
                    self.xsel    = self.pix2xpos(event.x) 
                else:
                    self.xsel2 = self.pix2xpos(event.x) 

            self.invalidate()

        if event.state & gtk.gdk.SHIFT_MASK and  event.state & gtk.gdk.BUTTON1_MASK:
            print "Shift Drag", event.x, event.y         
        pass

    def gotoxy(self, xx, yy, sel = None, mid = False):

        #print "gotoxy", xx, yy
        
        # Contain
        ylen = len(self.text)
        xx2 = max(xx, 0);  yy2 = max(yy, 0)
        xx2 = min(xx, self.maxlinelen);  yy2 = min(yy, ylen)
        
        if sel:
            self.xsel = xx2; self.xsel2 = xx2 + sel
            self.ysel = yy2; self.ysel2 = yy2
            self.invalidate()
        
        if mid:
            self.set_caret_middle(xx, yy)
        else:
            self.set_caret(xx, yy)
            
        self.invalidate()

    # --------------------------------------------------------------------
    # Goto position, and place it to upper half / quarter
    
    def set_caret_middle(self, xx, yy, sel = None, quart = 2):
   
        # Needs scroll?
        #xxx, yyy = self.get_size()        
        xlen = len(self.text)

        # Put it back in view:                    
        off = (self.get_height() / self.cyy) / quart
        if yy > off:            
            self.ypos = yy - off
        else:
            self.ypos = 0
            
        self.set_caret(xx, yy)
        self.invalidate()
       
    # Dimenswions in character cell
    def get_height_char(self):
        return self.get_height()  / self.cyy;

    def get_width_char(self):
        return self.get_width() / self.cxx;
                        
    # --------------------------------------------------------------------
    # Goto position, put caret (cursor) back to view, [vh]scgap 
    # distance from ends. This function was a difficult to write. :-{
    # Note the trick with comparing old cursor pos for a hint on scroll
    # direction. 
    # xx, yy - absolute position in the text buffer
    
    def set_caret(self, xx, yy):

        #print "set_caret", xx, yy

        # Needs scroll?
        need_inval = False
        cww = self.get_width_char()
        chh = self.get_height_char()
        xlen = len(self.text)

        # ----------------------------------------------------------------
        # Put it back in view yyy:                    
        
        off = chh - self.vscgap
        if yy - self.ypos > off:            
            #print "Scroll from caret down"
            if yy > self.ypos + self.caret[1]:
                #print "move d", "ypos", self.ypos, "yy", yy
                self.ypos = yy - off
                need_inval = True
                
        if yy - self.ypos < self.vscgap and self.ypos:
            #print "Scroll from caret up"
            if yy < self.ypos + self.caret[1]:
                #print "move u", "ypos", self.ypos, "yy", yy
                self.ypos = yy - self.vscgap
                self.ypos = max(self.ypos, 0)            
                need_inval = True
            
        yy -= self.ypos                                                                
        if self.ypos < 0: self.ypos = 0
            
        # ----------------------------------------------------------------
        # Put it back in view xxx:                            
        
        xoff = cww - self.hscgap
        if  xx - self.xpos  > xoff:
            #print "Scroll from caret right", "xx", xx, "xpos", self.xpos
            if self.xpos + self.caret[0] < xx:
                #print "moved r",  xx, self.caret[0], self.xpos                
                self.xpos =  xx - xoff
                self.xpos = max(self.xpos, 0)
                need_inval = True
        
        if  xx - self.xpos <  self.hscgap: 
            #print "Scroll from caret left ", xx, self.xpos
            if self.xpos + self.caret[0] > xx:
                #print "moved l", "xx", xx, "caret", self.caret[0], "xpos", self.xpos 
                self.xpos = xx - self.hscgap
                self.xpos = max(self.xpos, 0)            
                need_inval = True
                
        xx -= self.xpos          
        if self.xpos < 0: self.xpos = 0
          
        oldx = self.caret[0] * self.cxx; 
        oldy = self.caret[1] * self.cyy

        # Cheat - invalidate all if tab is involved at old line
        try:
            line = self.text[oldy]
        except: 
            line = ""; need_inval = True            
        if line.find("\t") >= 0:
            need_inval = True

        self.caret[0] = xx; self.caret[1] = yy
        
        # Low limit
        if self.caret[0] < 0: self.caret[0] = 0
        if self.caret[1] < 0: self.caret[1] = 0
               
        wxx = self.caret[0] * self.cxx
        wyy = self.caret[1] * self.cyy

        # Cheat - invalidate all if tab is involoved
        try:
            line = self.text[self.ypos + self.caret[1]]
        except: 
            line = ""; need_inval = True            
        if line.find("\t") >= 0:
            need_inval = True
            
        # Optimize cursor movement invalidation
        if  not need_inval :
            rect = gtk.gdk.Rectangle(wxx, wyy, self.cxx * self.cxx /2, self.cyy + 1)
            self.invalidate(rect)

            rect = gtk.gdk.Rectangle(oldx, oldy, self.cxx + self.cxx /2 , self.cyy + 1)
            self.invalidate(rect)

        # Update scroll bars, prevent them from sending scroll message:
        self.oneshot = True; self.vscroll.set_value(self.ypos)        
        self.honeshot = True; self.hscroll.set_value(self.xpos)        
        
        self.update_bar2()
        
        if  need_inval or self.bigcaret:
            self.invalidate()            
        
    def update_bar2(self):
        self.mained.update_statusbar2(self.caret[0] + self.xpos, \
                self.caret[1] + self.ypos, self.insert, len(self.text))
        
    def clearsel(self):
        old = self.xsel
        self.xsel  =  self.ysel = -1
        self.xsel2 =  self.ysel2 = -1
        if old != -1:
            self.invalidate()
            
    def keytime(self):
        #print "keytime raw", time.time(), self.fired
        if self.fired ==  1:
            #print "keytime", time.time(), self.fired
            pedspell.spell(self, self.spellmode)
        self.fired -= 1
   
    # Call key handler
    def area_key(self, area, event):
    
        # Restart timer ticks
        pedconfig.conf.idle = pedconfig.conf.IDLE_TIMEOUT
        pedconfig.conf.syncidle = pedconfig.conf.SYNCIDLE_TIMEOUT
        
        # Maintain a count of events, only fire only fire on the last one
        self.fired += 1  
        gobject.timeout_add(300, self.keytime)
           
        # The actual key handler         
        self.keyh.handle_key(self, area, event)
        
        #if event.type == gtk.gdk.KEY_RELEASE:
        #    self.source_id = gobject.idle_add(self.idle_callback)
      
        # We handled it  
        return True

     # Invalidate currdent line
    def inval_line(self):
        rect = gtk.gdk.Rectangle(0, self.caret[1] * self.cyy, 
                self.get_width(), self.cyy)
        self.invalidate(rect)
   
    def invalidate(self, rect = None):                        
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

    def area_focus(self, area, event):
        #print "ped doc area focus", event
        return False

    # Add to usder dictiodnary:
    def addict(self, widget, string, arg):
        #print "addict", arg
        lw = arg.lower()
        xfile = pedconfig.conf.config_dir + "/" + "userdict.txt"
        try:
            fd = open(xfile, "a+")
        except:
            print "Cannot open user dictionary"
            return
        try:
            fd.write(lw); fd.write("\n")
        except:
            print "Cannot write to user dictionary"
        fd.close()
        self.newword = True
        # Force new spell check
        self.fired += 1
        gobject.timeout_add(300, self.keytime)
        
    def popspell(self, widget, event, xstr):
        # Credeate a new menu-item with a name...
        menu = gtk.Menu()      
        menu.append(self.create_menuitem("Checking '%s'" % xstr, None))
        menu.append(self.create_menuitem("Add to Dict", self.addict, xstr))
        menu.append(self.create_menuitem("-------------", None))
        
        strs = "Creating suggestion list for '{0:s}'".format(xstr) 
        self.mained.update_statusbar(strs)
        arr = pedspell.suggest(self, xstr)
        
        if len(arr) == 0:
            menu.append(self.create_menuitem("No Matches", None))        
        else: 
            for aa, bb in arr:
                menu.append(self.create_menuitem(bb, self.menuitem_response))
        
        menu.popup(None, None, None, event.button, event.time)
        #self.mained.update_statusbar("Done.")
        
    def poprclick(self, widget, event):
        #print "Making rclick"
        mm = self.build_menu(self.window, pedmenu.rclick_menu)
        mm.popup(None, None, None, event.button, event.time)

    def menuitem_response(self, widget, string, arg):
        #print "menuitem response '%s'" % string
        # See if capitalized:
        
        pedconfig.conf.keyh.act.clip_cb(None, string, self)
        self.fired += 1
        gobject.timeout_add(300, self.keytime)

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def create_menuitem(self, string, action, arg = None):
        rclick_menu = gtk.MenuItem(string)
        if action:
            rclick_menu.connect("activate", action, string, arg);
        rclick_menu.show()        
        return rclick_menu
   
        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("DocWindowActions")
        action_group.add_actions(entries)      
        return action_group

    def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")

    def get_size(self):
        rect = self.get_allocation()
        return rect.width, rect.height

    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width

    def save(self):
        strx = ""        
        if self.changed:
            # Is this the untitled name?
            base, ext =  os.path.splitext(pedconfig.conf.UNTITLED)
            base1 = os.path.basename(self.fname)
            base2, ext2 =  os.path.splitext(base1)
            if base2[:len(base)] == base:
                self.file_dlg(gtk.RESPONSE_YES)                
            else:
                self.writefile()
            strx = "Saved '{0:s}'".format(self.fname) 
            if(pedconfig.conf.verbose):
                print strx
        else:
            strx = "File is not modified." 

        self.mained.update_statusbar(strx)

    def saveas(self):        
        self.file_dlg(gtk.RESPONSE_YES)                
        
    def coloring(self, flag):
        self.colflag = flag
        self.invalidate()
    
    def showcol(self, flag):
        self.scol = flag
        self.invalidate()

    def hexview(self, flag):
        self.hex = flag
        self.invalidate()

    def flash(self, flag):
        self.bigcaret = flag
        self.invalidate()
    
    def showtab(self, flag):
        self.stab = flag
        self.scol = flag
        self.invalidate()
        
    def closedoc(self):
        strx = "Closing '{0:s}'".format(self.fname) 
        if(pedconfig.conf.verbose):
            print strx
        self.mained.update_statusbar(strx)
        self.saveparms()
        return self.prompt_save(False)

    # Load file into this buffer, return False on failure
    def loadfile(self, filename, create = False):
        self.fname = filename
        if self.fname == "": 
            strx = "Must specify file name."
            print  strx
            self.mained.update_statusbar(strx)
            return False
        try:            
            self.text = readfile(self.fname)
        except:
            errr = "Cannot read file '" + self.fname + "'" #, sys.exc_info()
            if(pedconfig.conf.verbose):
                print errr
            self.mained.update_statusbar(errr) 
            usleep(20)
            return False
        
        #self.ularr.append((10 ,10, 20))
        mlen = self.calc_maxline()
                
        # Set up scroll bars        
        self.set_maxlinelen(mlen, False)
        self.set_maxlines(len(self.text), False)
   
        self.loadundo()
        self.saveorg()
        self.savebackup()
        self.loadparms()
        
        # Propagate main wndow ref
        pedmenu.mained = self.mained
        
        # Turn off coloring if not python
        ext = os.path.splitext(self.fname)[1].lower()
        if ext != ".py" and ext != ".c" and ext !=".cpp":
            self.colflag = False
        return True
       
    def calc_maxline(self):
        mlen = 0
        for aa in self.text:       
            xlen = len(aa)
            if mlen < xlen: 
                mlen = xlen
        #self.maxlinelen = mlen
        return mlen
        
    # Load per file parms (cursor etc)         
    def loadparms(self):
        hhh = hash_name(self.fname)           
        
        self.startxxx  =  pedconfig.conf.sql.get_int(hhh + "/xx")
        self.startyyy  =  pedconfig.conf.sql.get_int(hhh + "/yy")
        # Note: we set cursor on first focus
        
    # Save per file parms (cursor, fname, etc)         
    def  saveparms(self):
        hhh = hash_name(self.fname)           
        pedconfig.conf.sql.put(hhh + "/xx", self.xpos + self.caret[0])        
        pedconfig.conf.sql.put(hhh + "/yy", self.ypos + self.caret[1])        
        pedconfig.conf.sql.put(hhh + "/fname", self.fname)        
        #print  "saveparm", time.clock() - got_clock        

    # Create org backup
    def saveorg(self):
        hhh = hash_name(self.fname) + ".org"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        if not os.path.isfile(xfile):
            try:
                writefile(xfile, self.text)                
            except:
                print "Cannot create (org) backup file", xfile, sys.exc_info()

   # Create backup
    def savebackup(self):
        hhh = hash_name(self.fname) + ".bak"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        try:
            writefile(xfile, self.text)                
        except:
            sss = "Cannot create backup file" + xfile + sys.exc_info()
            print sss
                    
    def prompt_save(self, askname = True):

        # Always save params
        self.saveparms()
        
        if not self.changed:
            #print "not changed", self.fname
            return 
        
        msg = "\nWould you like to save:\n\n  \"%s\" \n" % self.fname
        rp = pedync.yes_no_cancel("pyedit: Save File ?", msg)

        if rp == gtk.RESPONSE_YES:   
            if askname:
                self.file_dlg(rp)
            else:
                self.save()                
        elif rp == gtk.RESPONSE_NO:   
            pass
        elif  rp == gtk.RESPONSE_CANCEL:
            return True
        else:
            print "warning: invalid response from dialog"
                    
    def file_dlg(self, resp):
        if resp == gtk.RESPONSE_YES:
            but =   "Cancel", gtk.BUTTONS_CANCEL, "Save File", gtk.BUTTONS_OK
            fc = gtk.FileChooserDialog("Save file", None, gtk.FILE_CHOOSER_ACTION_SAVE, \
                but)
            #fc.set_do_overwrite_confirmation(True)
            fc.set_current_name(os.path.basename(self.fname))
            fc.set_default_response(gtk.BUTTONS_OK)
            fc.connect("response", self.done_fc)                
            fc.run()             

    def writefile(self):
        if(pedconfig.conf.verbose):
            print "Saving '"+ self.fname + "'"
        writefile(self.fname, self.text)
        self.saveundo()        
        self.saveparms()
        self.set_changed(False)
        self.set_tablabel()                       

    def delundo(self):
        self.undoarr = []; self.redoarr = [] 
        # Remove file
        hhh = hash_name(self.fname) + ".udo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        fh = open(xfile, "w")
        fh.close()
        hhh = hash_name(self.fname) + ".rdo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        fh = open(xfile, "w")
        fh.close()
        
    def saveundo(self):
        hhh = hash_name(self.fname) + ".udo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        try:
            fh = open(xfile, "w")
            pickle.dump(self.undoarr, fh)
        except:
            print "Cannot save undo file", sys.exc_info()

        hhh = hash_name(self.fname) + ".rdo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        try:
            fh = open(xfile, "w")
            pickle.dump(self.redoarr, fh)
        except:
            print "Cannot save redo file", sys.exc_info()

    def loadundo(self):
        hhh = hash_name(self.fname) + ".udo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        try:
            fh = open(xfile)
            self.undoarr = pickle.load(fh)
        except:
            pass
            # Ignore it, not all files will have undo
            #print "Cannot load undo file", xfile
        self.initial_undo_size = len(self.undoarr)

        hhh = hash_name(self.fname) + ".rdo"           
        xfile = pedconfig.conf.data_dir + "/" + hhh
        try:
            fh = open(xfile)
            self.redoarr = pickle.load(fh)
        except:
            pass
            # Ignore it, not all files will have redo
            #print "Cannot load redo file", xfile
        self.initial_redo_size = len(self.redoarr)
    
    def done_fc(self, win, resp):
        #print "done_fc", win, resp
        if resp == gtk.BUTTONS_OK:
            fname = win.get_filename()
            if not fname:
                print "Must have filename"
            else:         
                if os.path.isfile(fname):
                    dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                    "\nWould you like overwrite file:\n\n  \"%s\" \n" % fname)
                    dialog.set_title("Overwrite file ?")
                    dialog.set_default_response(gtk.RESPONSE_YES)
                    dialog.connect("response", self.overwrite_done, fname, win)
                    dialog.run()            
                else:
                    win.destroy()
                    self.fname = fname                        
                    self.writefile()                 
                            
    def overwrite_done(self, win, resp, fname, win2):
        #print "overwrite done", resp
        if resp == gtk.RESPONSE_YES:  
            self.fname = fname
            self.writefile()
            win2.destroy()
        win.destroy()                
        
    def do_chores(self):
    
        #print "do_chores"
        
        if  not self.needscan:
            return
            
        self.needscan = False        

        # Scan left pane
        pedconfig.conf.idle = pedconfig.conf.IDLE_TIMEOUT
        pedconfig.conf.syncidle = pedconfig.conf.SYNCIDLE_TIMEOUT
        
    def set_changed(self, flag):        
        old = self.changed
        self.changed = flag
        # Exec actions:
        if old != self.changed:            
            #print "Setting changed on ", self.fname
            self.set_tablabel()
            
    def set_tablabel(self):
        # Find me in tabs
        nn = self.notebook.get_n_pages(); cnt = 0
        while True:
            if cnt >= nn: break
            ppp = self.notebook.get_nth_page(cnt)
            if ppp.area == self:        
                self._setlabel(ppp) 
                break
            cnt += 1            

    def _setlabel(self, ppp):
        # Set label to tab
        ss = shortenstr(os.path.basename(self.fname), 24)
        if  self.changed:
            str2 = "  *" + ss + "  "
        else:
            str2 = "  " + ss + "  "
        label = gtk.Label(str2)
        label.set_tooltip_text(self.fname)
        label.set_single_line_mode(True)
        
        image = gtk.Image(); image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        butt = gtk.Button();  butt.add(image)
        butt.set_focus_on_click(False)
        butt.set_relief( gtk.RELIEF_NONE)        
        rc = butt.get_modifier_style()
        rc.xthickness = 1; rc.ythickness = 1        
        butt.modify_style(rc)        
        
        butt.connect("clicked", self.close_button)
        butt.set_tooltip_text("Close Document")
        hbox = gtk.HBox()
                
        hbox.pack_start(label)
        hbox.pack_start(butt)
        hbox.show_all()
        self.notebook.set_tab_label(ppp, hbox)

    def close_button(self, arg1):
        #print "close_button", arg1
        self.mained.closedoc()

    def savemacro(self):
        #print "Savemacro"               
        
        fname = "untitled.mac"
        xfile = pedconfig.conf.config_dir + "/macros/" + fname        
        old = os.getcwd()
        try:
            os.chdir(os.path.dirname(xfile))
        except:
            print "No macros directory"
            
        but =   "Cancel", gtk.BUTTONS_CANCEL, "Save Macro", gtk.BUTTONS_OK
        fc = gtk.FileChooserDialog("Save Macro", None, gtk.FILE_CHOOSER_ACTION_SAVE, \
            but)
      
        fc.set_current_name(os.path.basename(xfile))
        fc.set_default_response(gtk.BUTTONS_OK)
        fc.connect("response", self.done_mac_fc, old)                
        fc.run()   
        
    def done_mac_fc(self, win, resp, old):
        #print  "done_mac_fc", resp
        # Back to original dir
        os.chdir(os.path.dirname(old))        
        if resp == gtk.BUTTONS_OK:        
            try:
                fname = win.get_filename()
                if not fname:
                    print "Must have filename"
                else:         
                    fh = open(fname, "w")
                    pickle.dump(self.recarr, fh)
            except:
                print "Cannot save macro file", sys.exc_info()
            
        win.destroy()        
                
    def loadmacro(self):
        #print "Loadmacro"               

        xfile = pedconfig.conf.config_dir + "/macros/"    
        old = os.getcwd()
        try:
            os.chdir(os.path.dirname(xfile))
        except:
            print "No macros directory"
            
        but =   "Cancel", gtk.BUTTONS_CANCEL, "Load Macro", gtk.BUTTONS_OK
        fc = gtk.FileChooserDialog("Load Macro", None, gtk.FILE_CHOOSER_ACTION_OPEN, \
            but)
      
        #fc.set_current_name(os.path.basename(xfile))
        fc.set_default_response(gtk.BUTTONS_OK)
        fc.connect("response", self.done_mac_open_fc, old)                
        fc.run()   
        
    def done_mac_open_fc(self, win, resp, old):
        #print  "done_mac_fc", resp
        
        # Back to original dir
        os.chdir(os.path.dirname(old))        
        if resp == gtk.BUTTONS_OK:        
            try:
                fname = win.get_filename()
                if not fname:
                    print "Must have filename"
                else:         
                    fh = open(fname, "r")
                    self.recarr = pickle.load(fh)
                    fh.close()
            except:
                print "Cannot load macro file", sys.exc_info()
            
        win.destroy()                

    # Refresh current search buffer
    def search_again(self):
        if len(self.accum) == 0:
            return
            
        if self.src_changed:   
            self.search(self.srctxt, self.regex, self.boolcase, self.boolregex)

    # --------------------------------------------------------------------
    def search(self, srctxt, regex, boolcase, boolregex):
    
        # Remember old settings:
        self.srctxt = srctxt;       self.regex = regex
        self.boolcase = boolcase;   self.boolregex = boolregex
        self.src_changed = False 
                
        self.accum = []; 
     
        curr = self.caret[1] + self.ypos   
        was = -1; cnt = 0; cnt2 = 0
    
        for line in self.text:
            # Search one line for multiple matches
            mmm = src_line(line, cnt, srctxt, regex, boolcase, boolregex)

            if cnt > curr and was == -1:
                was = cnt2
            if  mmm:
                cnt2 += 1;    
                for sss in mmm:
                    self.accum.append(sss)
            if cnt % 100 == 0:            
                self.mained.update_statusbar("Searching at %d" % cnt)
                usleep(1)
            cnt += 1            
        return was, cnt2

# Run this on an idle callback so the user can work while this is going

def run_async_time(win):

    global last_scanned

    if  last_scanned == win:
        return
        
    last_scanned = win
    win.appwin.start_tree()            
          
    #print "run_sync_time", time.time()    
    
    sumw = []
    if win.text:
        try:
            for kw in sumkeywords:
                for line in win.text:
                    if line.find(kw) >= 0:
                        sumw.append(line)
        except:
            pass

    try:        
        win.appwin.update_treestore(sumw)
    except:
        # This is normal, ignore it
        print "run_async_time", sys.exc_info()    
        pass










