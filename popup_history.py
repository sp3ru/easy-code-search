


import Tkinter as tk
import screen_utils
import os

class PopupDialog:

    def __init__(self, parent, posx, posy, lastPaths = None, allPaths = None, callback = None):
        self.callback = callback
        top = self.top = tk.Toplevel(parent, pady= 2, padx= 2)
        self.addPaths(lastPaths, allPaths)
        posx,posy = self.getBestPosition(posx,posy)
        top.geometry('+%d+%d'%(posx,posy))  
        top["bg"] = "#080000"
       
        
        top.overrideredirect(1) 
        top.focus()
        top.focus_set()
        top.bind("<FocusOut>", self.FocusOut)



    def addPaths(self, lastPaths, allPaths):
        allPaths.sort()

        self.btns = []
        lastData = []

        for p in lastPaths:
           lastData = self._addStr( p, lastData)

        tk.Frame(self.top, bg = "black").pack()

        for p in allPaths:
           lastData = self._addStr( p, lastData)


        lastData = []

    def _addStr(self, path, lastData):
        path =os.path.normpath(path)
        data = path.split(os.path.sep)
        t = tk.Text(self.top, height= 1,font = 11, borderwidth =0,autoseparators =0, padx = 2, pady= 3)
        t["bg"] = "#F8F8F8"
        t.pack()
        t.bind("<Button-1>", lambda e,path=path:self.onClick(e,path)  )
        t.bind("<Enter>", self.onEnterBtn)
        self.btns.append(t)
        t.tag_config("here",  foreground="#B0B0B0")
        t.tag_config("slesh",  foreground="#B0B0C0", font = ("verbana",10,"bold"))

        for i,text in enumerate(data):
            if len(lastData)>i and text == lastData[i]:
                t.insert("end",text, "here")
            else:
                t.insert("end",text)

            t.insert("end","/", "slesh")



        return data








    def onClick(self, e, data):
        print data
        self.top.destroy()

    def onEnterBtn(self, e):
        for t in self.btns:
            t["bg"] = "#F8F8F8"
        e.widget["bg"] = "#6699CC"




    def getBestPosition(self, x,y, ofset = 10):
        warea = screen_utils.getWorkAreaByPosition(x,y)
        if not warea:
            print "not found work area display  for pos", x,y
            return x,y

        # hack: pack top and get w/h
        self.top.attributes("-alpha", 0)  
        self.top.update()   
        self.top.attributes("-alpha", 1) 

        w = self.top.winfo_width()
        h = self.top.winfo_height()
        minw,minh,maxw, maxh = warea

        if x + w > maxw:
            x = maxw - w - ofset
       
        if y + h > maxh:
            y = maxh - h - ofset
       

      
        return x,y



    def FocusOut(self, *e):
        print "FocusOut"
        self.top.destroy()



if __name__ == '__main__':
        
    def onClick(event):
        print "root coordinates: %s/%s" % (event.x_root, event.y_root)
        lastPaths = [r"C:\Users\sp3b\Desktop\easy-code-search\easy-code-search",
                    r"C:\Users\sp3b\Desktop\easy-code-search\bbbb",
                    r"C:\Users\sp3b/Desktop",
                    ] 

        allPaths = [r"C:\Users\sp3b\Desktop\easy-code-search\easy-code-search",
                    r"C:\Users\sp3b\Desktop\easy-code-searc1h\bbbb",
                    r"C:\Users\sp3b\Desktop\easy-code-search\bbbb12",
                    r"C:\Users\sp3b\Desktop\easy-code-search\script",
                    r"C:\Users\sp3b\Desktop\easy-code-search\data",
                    r"C:\Users\sp3b\Desktop\cdata",
                    r"C:\Users\sp3b/Desktop",
                    ] 


        inputDialog = PopupDialog(root,
                                event.x_root, event.y_root,
                                lastPaths = lastPaths,
                                allPaths = allPaths)
        root.wait_window(inputDialog.top)
       
    root = tk.Tk()
    mainLabel = tk.Label(root, text='Example for pop up input box')
    mainLabel.pack()

    root.bind("<Button-3>", onClick)
    root.geometry('200x200+100+500')

    root.mainloop()