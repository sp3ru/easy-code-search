# 
# -*- coding: utf-8 -*-
#


import Tkinter
import tkFont
import os
from tkLinks import HyperlinkManager
from textWidget import TextWidget



class HistoryWidget(TextWidget):
    def __init__(self,root,*w,**kw):
        TextWidget.__init__(self,root,*w,**kw )
        self.entities = []

    def clear(self):
        self.entities = []
        self.delete("0.0","end")

    def addEnt(self, data):
        if self.entities and data == self.entities[-1]:
            return
        self.entities.append(data)
        TextWidget.addEnt(self, data)
        


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
        
        butHide = Tkinter.Button(self,command = self._clear,text = "clear")
        butHide.place(relx=1, x=-19, y=2, anchor=Tkinter.NE)

    def _clear(self):
        self.wtext.clear()

    def setIDE(self, value):
        self.wtext.hyperlink.setIDE(value)
    
    def addEnt(self, data):
        self.wtext.addEnt(data)

    def setHistory(self, allHistoty):
        for data in allHistoty:
            self.addEnt(data)

        

class HistoryClickManager(object):
    """docstring for HistoryClickManager"""
    def __init__(self):
        self.entities = []
        self._topWindow = None

    def addEnt(self, data):
        if self.entities and data == self.entities[-1]:
            return
        self.entities.append(data)
        if self._topWindow:
            self._topWindow.addEnt(data)

    def show(self):
        if not self._topWindow:
            self._topWindow = HistoryWindow()
            self._topWindow.setHistory(self.entities)
            self._topWindow.protocol("WM_DELETE_WINDOW", self.onTopDestroy)
            self._topWindow.setIDE(self.ide)


    def hide(self):
        if self._topWindow:
            self._topWindow.destroy()
            self._topWindow = None

    def onTopDestroy(self):
        self._topWindow.destroy()
        self._topWindow = None

    def setIDE(self, value):
        self.ide = value
        if self._topWindow:
            self._topWindow.setIDE(value)




if __name__ == '__main__':
    root = Tkinter.Tk()
    
    x = HistoryWindow()
    root.mainloop()