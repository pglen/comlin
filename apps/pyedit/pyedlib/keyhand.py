#!/usr/bin/env python

# Key Handler for the editor. Extracted to a separate module
# for easy update. The key handler is table driven, so new key 
# assignments can be made with ease

import gtk            
import acthand

# Grabbed modifier defines from GTK
#
#  ... Turns out gtk.gdk 2.6+ defines these (above) constants as ...
#      gtk.gdk.*_MASK 
# Anyway, it was an exercise in grabbin' 'C' into python.

GDK_SHIFT_MASK      = 1 << 0
GDK_LOCK_MASK	    = 1 << 1
GDK_CONTROL_MASK    = 1 << 2
GDK_MOD1_MASK	    = 1 << 3
GDK_MOD2_MASK	    = 1 << 4
GDK_MOD3_MASK	    = 1 << 5
GDK_MOD4_MASK	    = 1 << 6
GDK_MOD5_MASK	    = 1 << 7
GDK_BUTTON1_MASK    = 1 << 8
GDK_BUTTON2_MASK    = 1 << 9
GDK_BUTTON3_MASK    = 1 << 10
GDK_BUTTON4_MASK    = 1 << 11
GDK_BUTTON5_MASK    = 1 << 12

#  /* The next few modifiers are used by XKB, so we skip to the end.
#   * Bits 15 - 25 are currently unused. Bit 29 is used internally.
#   */

GDK_SUPER_MASK    = 1 << 26
GDK_HYPER_MASK    = 1 << 27
GDK_META_MASK     = 1 << 28
  
GDK_RELEASE_MASK  = 1 << 30
GDK_MODIFIER_MASK = 0x5c001fff

# ------------------------------------------------------------------------
# Handle keys:

class KeyHand:

    ctrl = 0; alt = 0; shift = 0

    def __init__(self):

        self.act = acthand.ActHand()
        self.act.keyhand = self

        # Here one can customize the key / function assignments
        self.reg_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.Return, self.act.ret],
            [gtk.keysyms.KP_Enter, self.act.ret],
            [gtk.keysyms.Escape, self.act.esc],
            [gtk.keysyms.Insert, self.act.ins],
            [gtk.keysyms.KP_Insert, self.act.ins],

            [gtk.keysyms.Tab, self.act.tab],
            [gtk.keysyms.ISO_Left_Tab, self.act.tab],

            [gtk.keysyms.F1, self.act.f1],
            [gtk.keysyms.F2, self.act.f2],
            [gtk.keysyms.F3, self.act.f3],
            [gtk.keysyms.F4, self.act.f4],
            [gtk.keysyms.F5, self.act.f5],
            [gtk.keysyms.F6, self.act.f6],
            [gtk.keysyms.F7, self.act.f7],
            [gtk.keysyms.F8, self.act.f8],
            [gtk.keysyms.F9, self.act.f9],
            [gtk.keysyms.F10, self.act.f10],
            [gtk.keysyms.F11, self.act.f11],
            #[gtk.keysyms.F12, self.act.f12],
            ]

        # Separate keytab on ctrl for easy customization. May call functions
        # in any other keytabs. (if sensitive to mod key, separate actions result)
        
        self.ctrl_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.F6, self.act.f6],
            [gtk.keysyms.F10, self.act.f10],
            [gtk.keysyms.a, self.act.ctrl_a],
            [gtk.keysyms.A, self.act.ctrl_a],
            [gtk.keysyms.b, self.act.ctrl_b],
            [gtk.keysyms.B, self.act.ctrl_b],
            [gtk.keysyms.c, self.act.ctrl_c],
            [gtk.keysyms.D, self.act.ctrl_d],
            [gtk.keysyms.d, self.act.ctrl_d],
            [gtk.keysyms.C, self.act.ctrl_c],
            [gtk.keysyms.e, self.act.ctrl_e],
            [gtk.keysyms.E, self.act.ctrl_e],
            [gtk.keysyms.f, self.act.ctrl_f],
            [gtk.keysyms.F, self.act.ctrl_f],
            [gtk.keysyms.h, self.act.ctrl_h],
            [gtk.keysyms.H, self.act.ctrl_h],
            [gtk.keysyms.i, self.act.ctrl_i],
            [gtk.keysyms.I, self.act.ctrl_i],
            [gtk.keysyms.j, self.act.ctrl_j],
            [gtk.keysyms.J, self.act.ctrl_j],
            [gtk.keysyms.k, self.act.ctrl_k],
            [gtk.keysyms.K, self.act.ctrl_k],
            [gtk.keysyms.l, self.act.ctrl_l],
            [gtk.keysyms.L, self.act.ctrl_l],
            [gtk.keysyms.m, self.act.ctrl_m],
            [gtk.keysyms.M, self.act.ctrl_m],
            [gtk.keysyms.g, self.act.ctrl_g],
            [gtk.keysyms.G, self.act.ctrl_g],
            [gtk.keysyms.r, self.act.ctrl_r],
            [gtk.keysyms.R, self.act.ctrl_r],
            [gtk.keysyms.t, self.act.ctrl_t],
            [gtk.keysyms.T, self.act.ctrl_t],
            [gtk.keysyms.u, self.act.ctrl_u],
            [gtk.keysyms.U, self.act.ctrl_u],
            [gtk.keysyms.v, self.act.ctrl_v],
            [gtk.keysyms.V, self.act.ctrl_v],
            [gtk.keysyms.x, self.act.ctrl_x],
            [gtk.keysyms.X, self.act.ctrl_x],
            [gtk.keysyms.y, self.act.ctrl_y],
            [gtk.keysyms.Y, self.act.ctrl_y],
            [gtk.keysyms.z, self.act.ctrl_z],
            [gtk.keysyms.Z, self.act.ctrl_z],
            [gtk.keysyms.space, self.act.ctrl_space],
            ]

        # Separate keytab on ctrl - alt for easy customization. 

        self.ctrl_alt_keytab = [
            [gtk.keysyms.a, self.act.ctrl_alt_a],
            [gtk.keysyms.A, self.act.ctrl_alt_a],
            ]

        # Separate keytab on alt for easy customization. 

        self.alt_keytab = [
            [gtk.keysyms.Up, self.act.up],
            [gtk.keysyms.KP_Up, self.act.up],
            [gtk.keysyms.Down, self.act.down],
            [gtk.keysyms.KP_Down, self.act.down],
            [gtk.keysyms.Left, self.act.left],
            [gtk.keysyms.KP_Left, self.act.left],
            [gtk.keysyms.Right, self.act.right],
            [gtk.keysyms.KP_Right, self.act.right],
            [gtk.keysyms.Page_Up, self.act.pgup],
            [gtk.keysyms.KP_Page_Up, self.act.pgup],
            [gtk.keysyms.Page_Down, self.act.pgdn],
            [gtk.keysyms.KP_Page_Down, self.act.pgdn],
            [gtk.keysyms.Home, self.act.home],
            [gtk.keysyms.KP_Home, self.act.home],
            [gtk.keysyms.End, self.act.end],
            [gtk.keysyms.KP_End, self.act.end],
            [gtk.keysyms.Delete, self.act.delete],
            [gtk.keysyms.KP_Delete, self.act.delete],
            [gtk.keysyms.BackSpace, self.act.bs],
            [gtk.keysyms.a, self.act.alt_a],
            [gtk.keysyms.A, self.act.alt_a],
            [gtk.keysyms.b, self.act.alt_b],
            [gtk.keysyms.B, self.act.alt_b],
            [gtk.keysyms.c, self.act.alt_c],
            [gtk.keysyms.C, self.act.alt_c],
            [gtk.keysyms.d, self.act.alt_d],
            [gtk.keysyms.D, self.act.alt_d],
            [gtk.keysyms.i, self.act.alt_i],
            [gtk.keysyms.I, self.act.alt_i],
            [gtk.keysyms.j, self.act.alt_j],
            [gtk.keysyms.J, self.act.alt_j],
            [gtk.keysyms.k, self.act.alt_k],
            [gtk.keysyms.K, self.act.alt_k],
            [gtk.keysyms.l, self.act.alt_l],
            [gtk.keysyms.L, self.act.alt_l],
            [gtk.keysyms.o, self.act.alt_o],
            [gtk.keysyms.O, self.act.alt_o],
            [gtk.keysyms.q, self.act.alt_q],
            [gtk.keysyms.Q, self.act.alt_q],
            [gtk.keysyms.y, self.act.alt_y],
            [gtk.keysyms.Y, self.act.alt_y],
            [gtk.keysyms.p, self.act.f5],
            [gtk.keysyms.P, self.act.f5],
            [gtk.keysyms.n, self.act.f6],
            [gtk.keysyms.N, self.act.f6],
            [gtk.keysyms.r, self.act.ctrl_y],
            [gtk.keysyms.R, self.act.ctrl_y],
            [gtk.keysyms.s, self.act.alt_s],
            [gtk.keysyms.S, self.act.alt_s],
            [gtk.keysyms.t, self.act.ctrl_h],
            [gtk.keysyms.T, self.act.ctrl_h],
            [gtk.keysyms.u, self.act.ctrl_z],
            [gtk.keysyms.U, self.act.ctrl_z],
            [gtk.keysyms.v, self.act.alt_v],
            [gtk.keysyms.V, self.act.alt_v],
            [gtk.keysyms.w, self.act.alt_w],
            [gtk.keysyms.W, self.act.alt_w],
            [gtk.keysyms.g, self.act.alt_g],
            [gtk.keysyms.G, self.act.alt_g],
            [gtk.keysyms.f, self.act.alt_f],
            [gtk.keysyms.F, self.act.alt_f],
            ]

    # When we get focus, we start out with no modifier keys
    def reset(self):
        self.ctrl = 0; self.alt = 0; self.shift = 0

    # Main entry point for handling keys:
    
    def handle_key(self, self2, area, event):

        #print "key event",  int(event.type), int(event.state), 
        #print event.keyval, hex(event.keyval)
        #print event.state, event.string
        
        self.state2 = int(event.state)
        self.handle_key2(self2, area, event)
        
    # Main entry point for handling keys:
    
    def handle_key2(self, self2, area, event):
        if self2.record:
            if event.keyval == gtk.keysyms.F7 or \
                    event.keyval == gtk.keysyms.F8:
                #print "avoiding record/play recursion", event
                pass                                    
            else:
                var = (int(event.type), event.keyval, int(event.state),\
                        self.shift, self.ctrl, self.alt)            
                self2.recarr.append(var)     
                
        ret = self.handle_modifiers(self2, area, event)
        # Propagate to document (just for easy access)
        self2.ctrl = self.ctrl
        self2.alt = self.alt
        self2.shift = self.shift
        if ret: return
                
        if  event.type == gtk.gdk.KEY_PRESS:
            if self2.nokey:                                  
                if  (self.ctrl == True) and \
                    (event.keyval == gtk.keysyms.space):
                    self2.mained.update_statusbar("Keyboard enabled.")  
                    self2.nokey = False
                else:                 
                    self2.mained.update_statusbar(\
                        "Keyboard disabled. Press Ctrl-Space to enable.")
                    if event.keyval == gtk.keysyms.Escape:
                        self2.mained.update_statusbar("ESC")            
         
                return
                         
            # Call the appropriate handlers
        if self.ctrl and self.alt:
            self.handle_ctrl_alt_key(self2, area, event)
        elif self.alt:
            self.handle_alt_key(self2, area, event)
        elif self.ctrl:
            self.handle_ctrl_key(self2, area, event)
        else:
            self.handle_reg_key(self2, area, event)

    # --------------------------------------------------------------------
    # Note that it does not handle stacked control keys - just on / off

    def handle_modifiers(self, self2, area, event):

        ret = False
        
        # This turned out to be a bust ... let the OS feed me the right state
        # However, we still interpret them so the key is discarded
        # The key state was inconsistent, as the key is not fed when there is 
        # no focus. For example alt-tab - the focus goes away on tab - 
        # alt release is never fed to us. See Below.
        # Also, if you want to interpret Left-Alt or Right-Alt, 
        # (or L/R shift/control), here is the place to do it.        

        # Do key down:
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Alt_L or \
                    event.keyval == gtk.keysyms.Alt_R:
                #print "Alt down"
                #self2.flash(True)
                #self.alt = True; 
                ret = True
            elif event.keyval == gtk.keysyms.Control_L or \
                    event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl down"
                #self.ctrl = True; 
                ret = True
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift down"
                #self.shift = True; 
                ret = True

        # Do key up
        elif  event.type == gtk.gdk.KEY_RELEASE:
            if event.keyval == gtk.keysyms.Alt_L or \
                  event.keyval == gtk.keysyms.Alt_R:
                #print "Alt up"
                #self2.flash(False)
                #self.alt = False; 
                ret = True
            if event.keyval == gtk.keysyms.Control_L or \
                  event.keyval == gtk.keysyms.Control_R:
                #print "Ctrl up"
                #self.ctrl = False; 
                ret = True
            if event.keyval == gtk.keysyms.Shift_L or \
                  event.keyval == gtk.keysyms.Shift_R:
                #print "shift up"
                #self.shift = False; 
                ret = True           
    
        #if event.state & GDK_SHIFT_MASK:
        #if event.state & gtk.gdk.SHIFT_MASK:
        if self.state2 & gtk.gdk.SHIFT_MASK:
            self.shift = True
        else:
            self.shift = False

        #if event.state & GDK_MOD1_MASK:
        if self.state2  & gtk.gdk.MOD1_MASK:
            self.alt = True
        else:
            self.alt = False

        #if event.state & GDK_CONTROL_MASK:
        if self.state2  & gtk.gdk.CONTROL_MASK:
            self.ctrl = True
        else:
            self.ctrl = False

        return ret
    # --------------------------------------------------------------------

    # Obsolete:
    def handle_shift_key(self, self2, area, event):
        #print "Shift hand"
        #xidx = self2.caret[0]; idx =  self2.caret[1] 
        ret = False                
        return ret

    # --------------------------------------------------------------------
    # Control Alt keytab

    def handle_ctrl_alt_key(self, self2, area, event):
        self._handle_key(self2, area, event, self.ctrl_alt_keytab)

    # --------------------------------------------------------------------
    # Control keytab

    def handle_ctrl_key(self, self2, area, event):
        self._handle_key(self2, area, event, self.ctrl_keytab)

    # --------------------------------------------------------------------
    # Regular keytab

    def handle_reg_key(self, self2, area, event):
        # Handle multi key press counts by resetting if not that key
        if event.type == gtk.gdk.KEY_PRESS:
            if event.keyval != gtk.keysyms.Home:
                self.act.was_home = 0
            if event.keyval != gtk.keysyms.End:                
                self.act.was_end = 0
            
        self._handle_key(self2, area, event, self.reg_keytab)

    # --------------------------------------------------------------------
    # Alt key

    def handle_alt_key(self, self2, area, event):
        if  event.type == gtk.gdk.KEY_PRESS:
            #print "alt hand", event
            if event.keyval >= gtk.keysyms._1 and event.keyval <= gtk.keysyms._9:
                #print "Alt num", event.keyval - gtk.keysyms._1
                num = event.keyval - gtk.keysyms._1
                if num >  self2.notebook.get_n_pages() - 1:
                    self2.mained.update_statusbar("Invalid tab (page) index.")
                else:
                    self2.notebook.set_current_page(num)
                
            elif event.keyval == gtk.keysyms._0:
                self2.appwin.window.set_focus(self2.appwin.treeview)
            else:
                self._handle_key(self2, area, event, self.alt_keytab)
        
    # Internal key handler. Keytab preselected by caller
    def _handle_key(self, self2, area, event, xtab):
        #print event
        ret = False
        if  event.type == gtk.gdk.KEY_PRESS:
            gotkey = False
            for kk, func in xtab:
                if event.keyval == kk:        
                    gotkey = True
                    func(self2)
                    break
            # No key assignment found, assume char
            if not gotkey:
               if event.keyval == gtk.keysyms.F12:
                    if self.shift:
                        self2.showtab(True)
                    elif self.ctrl:
                        self2.hexview(True)
                    elif self.alt:
                        self2.showcol(True)
                    else:
                        self2.flash(True)
               else:
                    self.act.add_key(self2, event)
               
        if  event.type == gtk.gdk.KEY_RELEASE:
            if event.keyval == gtk.keysyms.F12:
                    if self.shift:
                        self2.showtab(False)
                    if self.ctrl:
                        self2.hexview(False)
                    elif self.alt:
                        self2.showcol(False)
                    else:
                        self2.flash(False)
               
        return ret























































