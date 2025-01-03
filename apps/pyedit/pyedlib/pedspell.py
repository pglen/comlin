#!/usr/bin/env python

import signal, os, time, string, pickle
from threading import Timer
import gobject, gtk, pango
import leven, pedconfig

from pedutil import *

index2 = []; index3 = []; index4 = [] 
userdic = []

# Punctuation characters (most all non-alphanumeric chars)
# Note the space at the beginning
punctuation = " ,./<>?;\':[]\{}|=-`!@#$%^&*()_+\""

# Benchmark time 
#got_clock = 0

# ------------------------------------------------------------------------
# Spell buffer. We read the spell.txt file into a python array. 
# Lower case it, and we create an index to the letters aa-zz. (double letter)
# On search, we look at the first 2 letters and search the index for offset 
# in the array. This loads on 300 msec on an average system, and spell 
# checks the current context (of an average python file) in 5-15 msec. 
# Not bad for a 200+ thousand word dictionary. Without the index the 
# check took 3.00 full seconds. The spell operates on the idle timer,
# within the next N msec ticks. (configurable)

# We spell check the strings and comments only. The algorithm used to 
# select the checkable portion of the file is similar to the algorithm 
# used in coloring. Speed versus intelligence, so 'backslash quote' will
# fool the speller into thinking it is code.
# As the speller's presence is advisory, no harm is done. You can 
# cooperate in your strings with the speller by using single quote in 
# double quote strings and vice-versa. One useful trick is to escape
# the offending quote. Note, that if it is simpler for the editor,
# it is simpler to the compiler, and to the maintainer / reader.

document = None

def spell(self2, allflag = False):

    #global got_clock
    global document
    document = self2

    # Profile line, use it on bottlenecks
    #ck = time.clock()   
    
    if not self2.spell:        
        if len(self2.ularr):
            self2.ularr = []
            self2.invalidate()
        return
    
    #print "spell", allflag
    
    self2.ularr = []
    try:    
        errcnt = 0
        xlen = len(self2.text); cnt = self2.ypos
        yyy = self2.ypos + self2.get_height() / self2.cyy 

        # Contain checking to visible range
        while True:
            if cnt >= xlen: break
            if cnt >= yyy: break
            line = self2.text[cnt]            
            if allflag:
                # Spell all of it
                err = spell_line(line, 0, len(line))
                for ss, ee in err:
                    self2.ularr.append((ss, cnt, ee))
                    errcnt += 1
            else: 
                # Comments      
                ccc = line.find("#"); cccc = line.find('"')

                # See if hash precedes quote (if any)
                if ccc >= 0 and (cccc > ccc or cccc == -1):
                    ccc2 = calc_tabs(line, ccc)                    
                    err = spell_line(line, ccc, len(line))
                    for ss, ee in err:
                        self2.ularr.append((ss, cnt, ee))
                        #print  ss, ee, cnt, "'" + line[ss:ee] + "'"
                        errcnt += 1
                else:   
                    # Locate strings
                    qqq = 0                                 
                    while True:
                        quote = '"'
                        sss = qqq
                        qqq = line.find(quote, qqq); 
                        if qqq < 0:
                            # See if single quote is found
                            qqq = line.find("'", sss); 
                            if qqq >= 0:
                                quote = "'"                    
                        if qqq >= 0:
                            qqq += 1
                            qqqq = line.find(quote, qqq)
                            if qqqq >= 0:
                                qqq -= self2.xpos           
                                qqq2 = calc_tabs(line, qqq)                    
                                err = spell_line(line, qqq, qqqq)
                                for ss, ee in err:
                                    self2.ularr.append((ss, cnt, ee))
                                    #print  ss, ee, cnt, "'" + line[ss:ee] + "'"
                                    errcnt += 1
                                qqq = qqqq + 1
                            else:
                                break
                        else:
                            break
            cnt += 1
        self2.invalidate()
        #self2.mained.update_statusbar("%d spelling mistakes." % errcnt)                     

    except:
        print "Exception on spell check", sys.exc_info()
        
    #print  "all", time.clock() - got_clock        

# Ret an array of error misspelled x,y coord for this line
def spell_line(line, beg, end):

    #print "spell_line", line[beg:end]
    err = [];  idx = beg
    while True:
        if idx >= end: break
        idx = xnextchar2(line, punctuation, idx)
        #ss, ee = selword(line, idx)
        ss, ee = selasci(line, idx)
        found = spell_word(line[ss:ee])
        if not found:
            found = spell_user(line[ss:ee])
        
        # communicate it to upper layers
        if not found:
            err.append((ss, ee))
        idx = ee + 1
    return err
    
# ------------------------------------------------------------------------
# Return True if word found

def spell_word(word):

    #print "word", "'" + word + "'"
    
    if len(word) <= 1:                      # Do not spell short words
        return  True
        
    if word[0] == "#":                      # Hex Numbers, hashes
        return True   

    if word[0] >= "0" and word[0] <= "9":   # Numbers
        return True   
    
    lw = word.lower().strip().lstrip()
    global index2, index3
    # Pre read index
    if len(index2) == 0:
        build_index()
        
    found = False
    # Locate start and end
    cnt = 0; sss = 0; eee = 0
    for bb, bbb in index3:
        if lw[0:2] == bb:
            sss = bbb
            eee = index3[cnt+1][1]
            break
        cnt += 1
    #print "start, end", sss, eee
    # Finally, search within limits
    while True:
        if sss >= eee: break        
        if  index2[sss] == lw:
            #print "found", lw, word
            found = True
            break
        sss += 1
            
    return found
    
#  -----------------------------------------------------------------------
# If not found in the the regular dictionary, see if it is in user's

def spell_user(word):
   
    # Load / re-load 
    global userdic, document
    if (len(userdic) == 0) or (document.newword == True):
        document.newword = False 
        load_user_dict()
        
    if len(word) <= 1:          # Do not spell short words
        return  True
        
    if word[0] == "#":          # Hex Numbers, hashes
        return True   
    
    found = False 
    lw = word.lower().strip().lstrip()
    
    for aa in userdic:
        #print "dic", aa
        if  aa == lw:
            found = True 
            break

    return found
    
# ------------------------------------------------------------------------
# User dictionary. Crafted to be as simple as possible, no indexing etc ..
# We do not expect the user dictionary to grow beyond tens of words.
# Note: the dictionary reloads as we add new words.

def load_user_dict():

    global userdic
    #print "load_user_dict"
    xfile = pedconfig.conf.config_dir + "/" + "userdict.txt"
    
    # No dictionary yet
    if not os.path.isfile(xfile):
        return
    try:
        fd = open(xfile, "r")
    except:
        print "Cannot open user dictionary"
        return
   
    userdic = []
    while True :
        try:
            line = fd.readline()
            line = line.rstrip("\n")
            #print "load line", "'" + line + "'"
            if line == "":
                break
            userdic.append(line)
        except:
            break
    fd.close()

# ------------------------------------------------------------------------

def build_index():

    global index2, index3

    global document

    #document.mained.update_statusbar("Loading dictionary")                     
    
    # It is an msdos file (don't ask)
    index = readfile(get_exec_path("spell.txt"), "\r\n")

    #print index[0:10]
    for ww in index:
        index2.append(ww.lower())               
        
    #print index2[0:10]        
    prev = ""; prevs = ""; cnt = 0
    for ii in index2:
        if len(ii) >= 2:
            # The dictionary contained some garbage
            if ii[0].isalnum() and ii[1].isalnum():        
                ss = ii[0:2]
                if ss != prev:                                      
                    index3.append((ss, cnt))    
                    prev = ss                    
                # Do single index as well
                sss = ii[0:1]
                if sss != prevs:                                      
                    index4.append((sss, cnt))    
                    prevs = sss                    
        cnt += 1     
        
    # End Marker              
    index3.append((" ", cnt))            
    #print index3
    
    #global got_clock
    #print  "building idx", time.clock() - got_clock        
    
    #document.mained.update_statusbar(" ")                     

# ------------------------------------------------------------------------
        
def suggest(self2, xstr):

    got_clock = time.clock()   

    #print "Suggest", "'" + xstr + "'"
    cntx = 0
    lw = xstr.lower()
    
    global index2, index3, index4
    
    # Pre read index
    if len(index2) == 0:
        build_index()

    arr = []
    # Locate start and end
    cnt = 0; sss = 0; eee = 0
    # single index
    '''for bb, bbb in index4:
        if lw[0:1] == bb:
            sss = bbb
            eee = index4[cnt+1][1]
            break
        cnt += 1'''
    # double index        
    for bb, bbb in index3:
        if lw[0:2] == bb:
            sss = bbb
            eee = index3[cnt+1][1]
            break
        cnt += 1
        
    #print "start, end", sss, eee
    #print index2[sss], index2[eee]
    
    # Finally, search within limits
    while True:
        if sss >= eee: break        
        if cntx > 100: break
        ret = leven.Distance(index2[sss], lw)
        if ret < 4:
            arr.append((ret, index2[sss])); 
            cntx += 1
        sss += 1
    
    #print  "suggest", time.clock() - got_clock        
    arr.sort()
    return arr[:15]
    
# EOF


