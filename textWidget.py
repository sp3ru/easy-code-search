import Tkinter
import tkFont
import os
import copy
from tkLinks import HyperlinkManager


class TextWidget(Tkinter.Text):
    def __init__(self,root,*w,**kw):
        Tkinter.Text.__init__(self,root,*w,**kw )
        self.init()
        self.hyperlink = HyperlinkManager(self)


    def setIDE(self, value):
        self.hyperlink.setIDE(value)
        print "setIDE:", value

    def setClickCallback(self, foo):
        self.hyperlink.setCallback(foo)

    def init(self):
        f2 = tkFont.Font(self, self.cget("font"))
        f2.configure(underline = 0)
        f2.configure(weight = "bold")
        f2.configure(size = 16)
        self.tag_config("here",  foreground="blue", font = f2,background="DarkKhaki")                
        self.tag_config("folder", background="green", foreground="black")  
        self.tag_config("number", foreground="grey")  
        f = tkFont.Font(self, self.cget("font"))
        f.configure(underline = True)  
        self.tag_config("fname", foreground="blue") 

    def clear(self):
        self.delete("0.0","end")

    def drawNum(self, stroke):
        num,_ = stroke.split("|",1)    
        line, column = self.index('insert').split('.')
        end = len(num) +1
        self.tag_add("number", "%s.%s"%(line,0),"%s.%s"%(line,end))

    def addEnt(self, data):
        wtext = self
        fullname =data['fullname']
        subsfullname =data['subsfullname']
        wtext.insert('end',"\n"+'_'*20+'\n')   
        wtext.insert('end',' dir',self.hyperlink.addToDir([fullname,0])  ) 
        wtext.insert('end','   ' ) 
        if not data["isDir"]:
            wtext.insert('end',"TOIDE", self.hyperlink.addlink({"fname":fullname,"line":0,"column":0, "info":data}) ) 
        
        wtext.insert('end',' %s     %dKB  '  %(data["encoding"], data["size"]/1024))
        wtext.insert('end',"\n") 
        wtext.insert('end',fullname, "fname" ) 
        
        line, column = wtext.index('insert').split('.')
        if subsfullname:
            for start,end, _ in subsfullname:
                wtext.tag_add("here", "%s.%s"%(line,start),"%s.%s"%(line,end))
                
        wtext.insert('end','\n\n' )  
        last_line_number  = -1 
        for cursub,(stroke,linenumber,indexes, sub_addStrUp, sub_addStrDown) in enumerate(data["subs"]):
            column = indexes[0][-1]
            subaddkeys = sub_addStrUp.keys()
            subaddkeys.sort()
            for sub_a_k in subaddkeys:
                if  sub_a_k > last_line_number:
                    if sub_a_k > last_line_number+1:
                        wtext.insert('end', "...\n","number")
                    wtext.insert('end', sub_addStrUp[sub_a_k])
                    self.drawNum(sub_addStrUp[sub_a_k])
                    wtext.insert('end','\n' ) 
                    last_line_number = sub_a_k    

            if not subaddkeys and last_line_number != -1:
                if linenumber > last_line_number+1:
                        wtext.insert('end', "...\n","number")  

            lastiend =0
            copyd = copy.deepcopy(data)
            copyd["subs"] = [data["subs"][cursub]]
            for istart, iend, ireal in indexes:
                if lastiend <istart:
                    wtext.insert('end',stroke[lastiend:istart] )
                wtext.insert('end',stroke[istart:iend], self.hyperlink.addlink({"fname":fullname,"line":linenumber,"column":ireal, "info":copyd}) ) 
                lastiend   =    iend
            if iend <  len(stroke):
                  wtext.insert('end',stroke[iend:] )
            self.drawNum(stroke)
            wtext.insert('end','\n' ) 

            #####################################################
            nextlinenumber = -1
            if cursub+1 < len( data["subs"]): 
                nextlinenumber =  data["subs"][cursub+1][1]
            subaddkeys = sub_addStrDown.keys()
            subaddkeys.sort()
            for sub_a_k in subaddkeys:
                if nextlinenumber== -1 or sub_a_k < nextlinenumber:
                    wtext.insert('end', sub_addStrDown[sub_a_k])
                    self.drawNum(sub_addStrDown[sub_a_k])
                    wtext.insert('end','\n' ) 
                    linenumber = sub_a_k


            last_line_number = linenumber