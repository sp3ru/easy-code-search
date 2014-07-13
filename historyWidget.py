# 
# -*- coding: utf-8 -*-
#


import Tkinter
import tkFont
import os
from tkLinks import HyperlinkManager



class HistoryWidget(Tkinter.Text):
    def __init__(self,root,*w,**kw):
        Tkinter.Text.__init__(self,root,*w,**kw )
        self.entities = []
        self.init()
        self.hyperlink = HyperlinkManager(self)


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
        self.entities = []
        self.delete("0.0","end")

    def drawNum(self, stroke):
        num,_ = stroke.split("|",1)    
        line, column = self.index('insert').split('.')
        end = len(num) +1
        self.tag_add("number", "%s.%s"%(line,0),"%s.%s"%(line,end))

    def addEnt(self, data):
        if self.entities and data == self.entities[-1]:
            return
        self.entities.append(data)
        wtext = self
        fullname =data['fullname']
        subsfullname =data['subsfullname']
        wtext.insert('end',"\n"+'_'*20+'\n')   
        wtext.insert('end',' dir',self.hyperlink.addToDir([fullname,0])  ) 
        wtext.insert('end','   ' ) 
        if not data["isDir"]:
            wtext.insert('end',"TOIDE", self.hyperlink.addlink({"fname":fullname,"line":0,"column":0,}) ) 
        # wtext.insert('end',fullname, hyperlink.addlink({"fname":fullname,"line":0,"column":0}) ) 
        wtext.insert('end',' %s     %dKB  '  %(data["encoding"], data["size"]/1024))
        wtext.insert('end',"\n") 
        wtext.insert('end',fullname, "fname" ) 
        # wtext.insert('end',"\n" ) 

        line, column = wtext.index('insert').split('.')
        if subsfullname:
            for start,end, _ in subsfullname:
                wtext.tag_add("here", "%s.%s"%(line,start),"%s.%s"%(line,end))
                
        wtext.insert('end','\n\n' )  
        last_line_number  = -1 
        for cursub,(stroke,linenumber,indexes, sub_addStrUp, sub_addStrDown) in enumerate(data["subs"]):
            column = indexes[0][-1]
            # wtext.insert('end',stroke, hyperlink.addlink({"fname":fullname,"line":linenumber,"column":column}) )
            # line, column = wtext.index('insert').split('.')
            # for start,end, _ in indexes:
            #     wtext.tag_add("here", "%s.%s"%(line,start),"%s.%s"%(line,end))
            ######################################################
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
            for istart, iend, ireal in indexes:
                if lastiend <istart:
                    wtext.insert('end',stroke[lastiend:istart] )
                wtext.insert('end',stroke[istart:iend], self.hyperlink.addlink({"fname":fullname,"line":linenumber,"column":ireal}) ) 
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



class HistoryWindow(Tkinter.Toplevel):
    """docstring for HistoryWindow"""
    def __init__(self,*w,**kw):
        Tkinter.Toplevel.__init__(self,*w,**kw )
        self.wtext = HistoryWidget(self, wrap = 'none', font = ("courier",14),tabs =("0.4i"))

        vscrollbar = Tkinter.Scrollbar(self, orient='vert', command=self.wtext.yview)
        self.wtext['yscrollcommand'] = vscrollbar.set
        hscrollbar = Tkinter.Scrollbar(self, orient='hor', command=self.wtext.xview)
        self.wtext['xscrollcommand'] = hscrollbar.set

        vscrollbar.pack(side = "right",fill = "y",expand=0)
        hscrollbar.pack(side = "bottom",fill = "x",expand=0)
        self.wtext.pack(side = "right",fill = Tkinter.BOTH,expand=1)

    def setIDE(self, value):
        self.wtext.hyperlink.setIDE(value)
    
    def addEnt(self, data):
        self.wtext.addEnt(data)

    def setHistory(self, allHistoty):
        for data in allHistoty:
            self.addEnt(data)

        







if __name__ == '__main__':
    root = Tkinter.Tk()
    w = HistoryWidget(root, wrap = 'none', font = ("courier",14),tabs =("0.4i"))
    w.pack()
    x = HistoryWindow()
    root.mainloop()