# 
# -*- coding: utf-8 -*-
#


import Tkinter as tk
import subprocess

class HyperlinkManager:

    def __init__(self, wtext):

        self.text = wtext

        # self.text.tag_config("dir_hyperred", foreground="green",foreground="black")
        self.text.tag_config("dir_hyperred",  background="green", foreground="black")

        self.text.tag_bind("dir_hyperred", "<Enter>", self._enter)
        self.text.tag_bind("dir_hyperred", "<Leave>", self._leave)
        self.text.tag_bind("dir_hyperred", "<Button-1>", self._click)

        # self.text.tag_config("hyperred", foreground="red")
        self.text.tag_config("hyperred", background="yellow", foreground="blue")

        self.text.tag_bind("hyperred", "<Enter>", self._enter)
        self.text.tag_bind("hyperred", "<Leave>", self._leave)
        self.text.tag_bind("hyperred", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.dir_links = {}
        self.links = {}

    def addToDir(self, link_data):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "dir_hyperred-%d" % len(self.dir_links)
        self.dir_links[tag] = link_data    
        return "dir_hyperred", tag

    def addlink(self, link_data):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyperred-%d" % len(self.links)
        self.links[tag] = link_data
        return "hyperred", tag

    def setIDE(self, ide):
        self.ide = ide

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        print "HyperlinkManagergreen_click"
        for tag in self.text.tag_names(tk.CURRENT):
            if tag.startswith("dir_hyperred-"):
                pathfile = self.dir_links[tag][0].replace("/","\\")
                print "link :",[self.dir_links[tag]]
                print "link2:",[pathfile]
                subprocess.Popen(r'explorer /select,"%s"'%pathfile)
                self.text.config(cursor="")
                return
            if tag.startswith("hyperred-"):
                print "link:",[self.links[tag]]

        
                #d = {"fname":self.links[tag][0], "line":self.links[tag][1],"column":}
                #notepad = toIDE[variable_ide.get()]
                commandstr = self.ide.format(**self.links[tag])
                print "commandstr:",[commandstr] 
                subprocess.Popen(commandstr)
                return


