import Tkinter
import tkFont
import os

class wEntry(Tkinter.Entry):
    def __init__(self,root,*w,**kw):
        Tkinter.Entry.__init__(self,root,*w,**kw )
        self.root = root
        self._topFocused = False
        self.top = None  
        self.bind("<Control-space>",self.conMenu)
        self.bind("<Tab>", self._tabEvent)
        self.bind("<FocusOut>", self.conMenuHideAfter)
        self.bind("<Escape>", self._keyEscape)
        self.bind("<Down>", self._FocusTop)
        self.bind("<Up>", self._FocusTop)
        self.bind("<Return>", self._InsertPath)
        self.bind("<Key>", self._keyPress)



    def _InsertPath(self,*e):
        if not self.top:
            return
        index = self.index(Tkinter.INSERT)
        text = self.get()
        subtxt  =text[:index]   
        curDirdirname = unicode(os.path.dirname(subtxt ))
        self.delete(0, Tkinter.END)

        if curDirdirname:
            curDirdirname = os.path.normpath(curDirdirname)
            self.insert(0, curDirdirname + u"\\")

        cursel = self.top.listbox.get(Tkinter.ACTIVE)
        if cursel:
            self.insert(Tkinter.END, cursel + u"\\")
         
        self.conMenu()    
        return "break"

    def _ListboxB1(self, *e):
        self.after(200, self._InsertPath )   


    def _FocusTop(self, *e):
        if self.top:    
            self.top.listbox.focus()
            self.top.listbox.activate(0)
            self.top.listbox.select_anchor(0)
            self.top.listbox.select_set(0)
            return "break"

    def _keyEscape(self, *e):
        if self.top:
            self.conMenuHide()

    def _keyPress(self, *e):
        self.after(2, self._keyPressAfter )

    def _keyPressAfter(self, *e):
        if self.top:
            self.conMenu()

    def _tabEvent(self,*e):
        if not self.top:
            self.conMenu()
        else:
            self._InsertPath()
       
        return "break"

    def conFocusIn(self, *e):
        self._topFocused = 1


    def conMenuHideAfter(self, *e):
        self.after(200, self.conMenuHideCheck )


    def conMenuHideCheck(self, *e):
        if not self._topFocused:
            self.conMenuHide()

    def conMenuHide(self, *e):
        # print "conMenuHide"
        self._topFocused = False
        if self.top:
            self.top.destroy()
            self.top = None    

    def bind(self, key, foo, add = 1):
        Tkinter.Entry.bind(self, key, foo, add)

    def conMenu(self,*e):
        font = tkFont.nametofont(self["font"])
        fontheight = font.metrics().get("linespace")
        index = self.index(Tkinter.INSERT)
        text = self.get()
        subtxt  =text[:index]
  
        x = self.winfo_rootx()+ font.measure(subtxt) +2
        y = self.winfo_rooty() + self.winfo_height() +2

        
        if not self.top:
            top = Tkinter.Toplevel(background = "ivory3")
            self.top = top
            top.title("About this application...")
            top.overrideredirect(1)
            
            top.bind("<FocusOut>", self.conMenuHide)
            top.bind("<FocusIn>", self.conFocusIn)
            top.bind("<Escape>", self._keyEscape)
            top.bind("<Return>", self._InsertPath)
           

            scrollbar = Tkinter.Scrollbar(top)
            scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
            

            lb = Tkinter.Listbox(top)
            lb.pack(fill=Tkinter.BOTH, expand=1)
            lb.bind('<Button-1>', self._ListboxB1)



            lb.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=lb.yview)
            self.top.listbox = lb

            # for i in range(150):
            #     lb.insert(Tkinter.END,"z%s"%i)
        self.top.geometry('200x200+%d+%d'%( x,y))
        self.top.listbox.delete(0, Tkinter.END)
        curDirdirname = unicode(os.path.dirname(subtxt ))
        curDirStart=    os.path.basename(subtxt ).lower()
        firstDir = None
        # print "curDirdirname",[curDirdirname]
        if not curDirdirname:
            dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            drives  = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]
            for dd in drives:
                self.top.listbox.insert(Tkinter.END, dd)

        else:
            for dirname, dirnames, filenames in os.walk(curDirdirname):
                for dd in dirnames:
                    if dd.lower().startswith(curDirStart):
                        self.top.listbox.insert(Tkinter.END, dd)
                break


        self.top.listbox.activate(0)
        self.top.listbox.see(0)
        self.top.listbox.select_anchor(0)
        self.top.listbox.select_set(0)


                





if __name__ == '__main__':
   
    
    root = Tkinter.Tk()
    appHighlightFont = tkFont.Font(family='Helvetica', size=14)
    Tkinter.Label(root,text = "sadasdasd").pack()
      

    w = wEntry(root, width = 105, font = appHighlightFont)
    w.pack()
    w.focus()

    wEntry(root).pack(side = Tkinter.LEFT)
    # wEntry(root).pack(side = Tkinter.LEFT)
    wEntry(root).pack(side = Tkinter.TOP)
    # wEntry(root).pack(side = Tkinter.TOP)
    # wEntry(root).pack(side = Tkinter.BOTTOM)
    # wEntry(root).pack(side = Tkinter.BOTTOM)
    # wEntry(root).pack(side = Tkinter.BOTTOM)
    # wEntry(root).pack(side = Tkinter.LEFT)

    Tkinter.Label(text = "sadasdasd").pack(side = Tkinter.LEFT)
    Tkinter.Label(text = "sadawdadawdawdasdasd2").pack(side = Tkinter.TOP)
    root.mainloop()
