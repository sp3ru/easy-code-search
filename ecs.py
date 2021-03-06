# 
# -*- coding: utf-8 -*-
#



import sys
import copy 
# hack подменяю пути до либ, я криво их поставил
sys.path = [z.replace("Python264","Python27") for z in sys.path]
 




from speedwalk import walk
from history import History, ExtNotify
# from tkLinks import HyperlinkManager
import textWidget
import subprocess
import re 
import chardet 
import pickle 
import chardet 
import os 
from time import time
import Tkinter as tk
import tkFileDialog
import tkFont
from wEntry import wEntry
from popup_history import PopupDialog
from widgetBack import WidgetBackText, WidgetBackEntry

toIDE = {
"notepad++" : r'"C:\Program Files (x86)\Notepad++\notepad++.exe" "{fname}" -n{line} -c{column}',
# "sublime" : r'"C:\Program Files\Sublime Text 2\sublime_text.exe" "{fname}":{line}:{column}',
"sublime3" : r'"C:\Program Files (x86)\Sublime Text 3\sublime_text.exe" "{fname}":{line}:{column}',
"komodo" : r'"C:\Program Files (x86)\ActiveState Komodo Edit 8\komodo.exe" "{fname}" -l {line} -c{column}',
}
defIDE = "sublime3"

history = History(  savePath=os.getenv('USERPROFILE'),
                    savePathCoding=os.getenv('USERPROFILE'),
                    maxHistory=30)

extvalidator  = ExtNotify()

pathlast = history.getlsitPathsLast(1)

path = pathlast[0] if pathlast else ""
word =  history.getlsitWords()[-1] if history.getlsitWords() else ""
savedext =history.getExt()
# print  history.getlsitPaths()


def searhInStrWholeWorld(string,patern, ignoreCase = True, addpos = 0):
    lenw = len(patern)
    lens = len(string)
    if ignoreCase:
        string = string.lower()
    lastIndex = 0
    if not string: return
    while True:
        index = string.find(patern, lastIndex, lens )
        lastIndex = index+1    
        if index == -1:
            return None

        if index != 0:
            preSymbol = string[index-1]
            if preSymbol.isalpha() or preSymbol == "_" or preSymbol.isdigit():
                continue
        
        
        if index+lenw < lens:
            afterSymbol = string[index+lenw]
            if afterSymbol.isalpha() or afterSymbol == "_" or afterSymbol.isdigit():
                continue

        return [(index+addpos, index+addpos+lenw,index+1 )]


def searhInStr(string,patern,ignoreCase = True,regex=False, addpos = 0):
    if regex:
        return [(m.start(0)+addpos, m.end(0)+addpos, m.start(0)+1) for m in re.finditer(patern, string)]
    else:
        if ignoreCase:
            string = string.lower() 
        index = string.find(patern)
        if index == -1:
            return None
        return [(index+addpos, index+addpos+len(patern),index+1 )]
 

def find(path, patern, settings):
    maxsize = settings["maxsize"]
    autoEncoding = settings["autoEncoding"]
    ignoreCase = settings["ignoreCase"]
    regex = settings["regex"]
    wholeWorld = settings["wholeWorld"]
    addStrUp,addStrDown = settings["addStr"]
    out = []
    countall = 0
    countallvalid = 0
    allmath = 0
    if ignoreCase and not regex:
            patern = patern.lower()
    allFilesLenght = 0

    def genAnim():
        while True:
            for x in range(6):
                yield '*'*x
    getAnim = genAnim()
    tprefound= time()
    tlastTick= time()
    if not settings["fname"]:
        root.title("calculate...")
        for proot, dirs, files in walk(path):
            for fname, st in files:
                allFilesLenght += 1  
                if allFilesLenght % 300 == 0 and time() - tlastTick > 0.6:
                    tlastTick= time()
                    root.title("calculate" + getAnim.next())
                    root.update()

    print "allFilesLenght:", allFilesLenght, "t",time() - tprefound

    for proot, dirs, files in walk(path):
        if settings["fname"]:
            for folder, st in dirs:
                if wholeWorld and not regex:
                    subs = searhInStrWholeWorld(folder,patern,ignoreCase, addpos = len(proot)+1)
                else:
                    subs = searhInStr(folder,patern,ignoreCase,regex, addpos = len(proot)+1)

                if subs:
                    dictFound = { "fullname": os.path.normpath(os.path.join(proot, folder)),
                            "subsfullname":subs,
                            "isDir":1,
                            "encoding":None,
                            "subs":[],
                            "addStrUp":{},
                            "addStrDown":{},
                             "encoding" :   "",   
                            "size": 0
                        }
                    out.append(dictFound) 


                
        for fname, st in files:
            countall += 1
             # print "\r",
            # print countall,
            if not settings["fname"]:
                if countall%200 == 0:
                    proc = float(countall)/allFilesLenght * 100
                    root.title("%d%% : %s/%s"%(proc, countall, allFilesLenght))
                    root.update() 
                       

            if maxsize and maxsize <  st.st_size:
                continue

            if not extvalidator.isvalid(fname):
                continue

            fullname = os.path.normpath(os.path.join(proot, fname))
            dictFound = { "fullname":fullname,
                            "isDir": 0,
                            "subsfullname":None,
                            "encoding":None,
                            "subs":[],
                            "addStrUp":{},
                            "addStrDown":{},
                             "encoding" :   "",   
                            "size": st.st_size 
                        }

            if wholeWorld and not regex:
               subs = searhInStrWholeWorld(fname,patern,ignoreCase, addpos = len(proot)+1)
            else:            
                subs = searhInStr(fname,patern,ignoreCase,regex, addpos = len(proot)+1)
            if subs:
                dictFound["subsfullname"] = subs

            if settings["fname"]:
                if subs:
                    out.append(dictFound)  
                continue

            text = open(fullname,"r").read()
           
            #encoding = "utf8"
            encoding = "cp1251"
            if autoEncoding and st.st_size:
                encoding =  history.checkEncoding(fullname)
                if not encoding:
                    d = chardet.detect(text)
                    encoding = d["encoding"]
                    if not encoding:
                        print "auto encoding error",d,fullname
                        encoding = "utf8"
                    history.setEncoding(fullname,encoding)
            try:
                text = text.decode(encoding) 
            except:        
                print "decode encoding error",encoding,fullname
                if autoEncoding:
                    d = chardet.detect(text)
                    encoding = d["encoding"]
                    print "chardet again", d
                    history.setEncoding(fullname,encoding)
                else:    
                    encoding = "utf8"
                try:
                    text = text.decode(encoding,"ignore") 
                except:
                    print "encoding error,continue",encoding,fullname
                    continue
            dictFound["encoding"] =   encoding        
            countallvalid += 1  
            isfound = False
            text = text.split('\n')
            for sindex , string in enumerate(text,1):
                indexstr = "%4d|"%sindex
                if wholeWorld and not regex:
                    subs = searhInStrWholeWorld(string,patern,ignoreCase, len(indexstr))
                else:
                    subs = searhInStr(string,patern,ignoreCase,regex,len(indexstr))
                if subs:
                    sub_addStrUp, sub_addStrDown = {},{}
                    isfound = True
                    allmath += len(subs)
                    if addStrUp:
                        for i in range(addStrUp):
                            addind = sindex-i-1
                            if addind>=1:
                                sub_addStrUp[addind] = "%4d|"%addind + text[addind-1]


                    if addStrDown:
                        for i in range(addStrDown):
                            addind = sindex+i+1
                            if addind<=  len(text):
                                sub_addStrDown[addind] = "%4d|"%addind + text[addind-1]

                    dictFound["subs"].append([indexstr + string,sindex,subs,sub_addStrUp, sub_addStrDown ])


            if isfound or dictFound["subsfullname"]:
                out.append(dictFound)
    history.saveCoding()
    return out, countallvalid,countall, allmath


def startFind(*e):

    maxsize = inputMaxSize.get().lower()
    maxsize = maxsize.replace(" ","")
    maxsize = maxsize.replace("mb","")
    if not maxsize or not maxsize.isdigit():
        blink(inputMaxSize)  
        return
    maxsize = int(maxsize) * 1024*1024

    addStr = inputAddStr.get().lower()
        
    if not addStr.replace(" ","").isdigit():
        blink(inputAddStr)  
        return
    addStr = map(int,addStr.split())

    settings = {"maxsize":maxsize,
            "ignoreCase": ignCASEvar.get(),
            "fname":fnamevar.get(),
            "regex":chrevar.get(),
            "wholeWorld":wholeWorldVar.get(),
            "autoEncoding":autoEncodvar.get(),
            "addStr":addStr}
    



    path = unicode(epath.get())
    path = os.path.normpath(path)  
    patern = strpatern= unicode(eword.get())  
    
    if not patern:
        blink(eword, backcolor= "AliceBlue")  
        return

    if settings["regex"]    :
        flags =  re.IGNORECASE if settings["ignoreCase"] else 0
        try:
            patern =re.compile(patern, flags )
        except Exception, e:
            blink(chre)  
            blink(eword, backcolor= "AliceBlue") 
            print "re.compile error" , e
            return


    if not extvalidator.update(ext_wiget.get('0.0', "end")):
        blink(ext_wiget)  
        return

    if not os.path.isdir(path):
        blink(epath)  
        return

    path2 = unicode(epath_second.get())
    path2 = [os.path.normpath(p.strip())  for p in path2.split(";") if p.strip() and not p.strip().startswith("#")]  
    for p in  path2:       
        if not os.path.isdir(p):
            blink(epath_second)  
            return

    allpath = set(path2+[path])         

    history.setExt(ext_wiget.get("0.0","end")) 
    history.addVal(strpatern,path,path2) 
    wtext.delete("0.0","end")

    allout = []
    tsearh = time()
    gcountallvalid = 0
    gcountall = 0
    gallmath = 0
    but["bg"] = "DarkKhaki"
    for path in allpath:
            
        wtext.insert('end',"search in %s"%path) 
        root.update()

        

        out, countallvalid,countall, allmath = find(path, patern, settings)
        wtext.insert('end',"   %s in %s/%s[%s] --%s\n"%( allmath ,len(out),countallvalid,countall,time() - tsearh )) 
        gcountallvalid += countallvalid
        gcountall += countall
        gallmath += allmath
        allout.extend(out)

    tsearh =time() - tsearh 
    # wtext.delete("0.0","end")
    wtext.insert('end','\n' ) 
    if settings["wholeWorld"]:
        wtext.insert('end','settings: whole World = True\n' ) 
    if settings["maxsize"]:
        wtext.insert('end','settings: maxsize file = %s byte\n'%maxsize ) 

    wtext.insert('end','found %s   in %s files '%( gallmath ,len(allout) ))
    wtext.insert('end','[%s-valid] [%s-all] \nSearch time %s sec\n'%(gcountallvalid,gcountall,tsearh) )
    root.title("Draw...")


    for d in allout:
        wtext.addEnt(d)

    root.title("")        
    wtext.insert('end','\n\n//done' )         
    blink(but,  "green",  backcolor = "AliceBlue")          


def drawNum(stroke):
    num,_ = stroke.split("|",1)    
    line, column = wtext.index('insert').split('.')
    end = len(num) +1
    wtext.tag_add("number", "%s.%s"%(line,0),"%s.%s"%(line,end))

def init():
    f2 = tkFont.Font(wtext, wtext.cget("font"))
    f2.configure(underline = 0)
    f2.configure(weight = "bold")
    f2.configure(size = 16)
    wtext.tag_config("here",  foreground="blue", font = f2,background="DarkKhaki")                
    wtext.tag_config("folder", background="green", foreground="black")  
    wtext.tag_config("number", foreground="grey")  
    f = tkFont.Font(wtext, wtext.cget("font"))
    f.configure(underline = True)
   
    # wtext.tag_config("fname", foreground="black", font = f)    
    wtext.tag_config("fname", foreground="blue")    






#### GUI #################

def blink(wiget, color = "red", backcolor = "SystemWindow"):
    # wiget.config("background" = color)
    def foored(*e):
        # wiget["background"] = color
        wiget.config(background = color)
    def foowhite(*e):
        # wiget["background"] = backcolor
        wiget.config(background = backcolor)

    foored()   
    root.after(200,foowhite)
    root.after(300,foored)
    root.after(500,foowhite)
    # root.after(600,foo)


def insert2eword(*e):

    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    print "from Clipboard",[data]
    setvalentry(eword,data)

try:
    import win32clipboard
except ImportError:
    insert2eword = lambda *e:0



def opendirdialog(*w):
    from_path  = epath.get().strip()

    print "from_path",from_path
    fpath = tkFileDialog.askdirectory(initialdir = from_path,mustexist = False)   
    if fpath:
        epath.delete(0,"end")
        epath.insert(0,fpath)


def setvalentry(entryName,val):
    entryName.delete(0,"end")
    entryName.insert(0,val)





def pathHistory(event):
    inputDialog = PopupDialog(root,
                event.x_root, event.y_root,
                lastPaths = history.getlsitPathsLast(3),
                allPaths  = history.getlsitPaths(),
                callback = lambda path:setvalentry(epath,path))
    root.wait_window(inputDialog.top)



def wordHistory(event):
    popup = tk.Menu(root, tearoff=0)
    for word in history.getlsitWords()[::-1]:
        popup.add_command(label=word , command=lambda word=word:setvalentry(eword,word)) 
  

    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()

        
def epathKey(event):
    curDir = epath.get()
    ##print dir(event)
    x,y=event.widget.winfo_pointerxy()
    print x,y
    index =  event.widget.index(tk.INSERT)

    # print dir(event.widget)
    x =event.widget.winfo_rootx() + index * 12
    y =event.widget.winfo_rooty() + 12
   
    

    popup = tk.Menu(root, tearoff=0)
    #print dir(popup)
    curDirdirname = unicode(os.path.dirname(curDir ))
    curDirStart=    os.path.basename(curDir ).lower()
    firstDir = None
    for dirname, dirnames, filenames in os.walk(curDirdirname):
        for dd in dirnames:
            if not firstDir: firstDir = os.path.join(curDirdirname,dd,"")
            #dd = dd.decode("cp1251")
            if dd.lower().startswith(curDirStart):
                popup.add_command(label=dd , command=lambda newword=os.path.join(curDirdirname,dd,""):setvalentry(epath,newword)) 

        break

    # for word in ["xx",'yy','xxxxxz']:
    #     popup.add_command(label=word , command=lambda newword=os.path.join(curDir,word):setvalentry(epath,newword)) 
    popup.bind("<Return>", lambda e:setvalentry(epath,firstDir))

    try:
        # popup.tk_popup(x, y, 0)
        popup.post(x, y)
        # print "focus"
        popup.focus()
    except Exception as e:
        print e
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()
               

def callback_variable_ide(*to):
    notepad = toIDE[variable_ide.get()]
    wtext.setIDE(notepad)
    historyClick.setIDE(notepad)



def hideInhide(*e):
    global frame1_visble
    if frame1_visble:
        frame1.pack_forget()
        butHide.place(relx=1, x=-19, y=2, anchor=tk.NE)
        # tk.Grid.columnconfigure(wtext,0,weight=1)
        # tk.Grid.columnconfigure(vscrollbar,1,weight=2)
    else:
        butHide.place(relx=1, x=-5, y=2, anchor=tk.NE)
        vscrollbar.pack_forget()
        hscrollbar.pack_forget()
        wtext.pack_forget()

        frame1.pack(side="top",fill= 'x')
        vscrollbar.pack(side = "right",fill = "y",expand=0)
        hscrollbar.pack(side = "bottom",fill = "x",expand=0)
        wtext.pack(side = "right",fill = tk.BOTH,expand=1)
    frame1_visble = not frame1_visble
   
def eventIgnore(*e):
    return "break"

root = tk.Tk()
frame1 = tk.Frame(root)
# frame1.grid(row = 0 ,column =0, sticky='n')
frame1_visble = 1


frame1.pack(side="top",fill= 'x')
# wtext = tk.Text(root,wrap = 'none', font = ("courier",14),tabs =("0.4i"))
wtext = textWidget.TextWidget(root,wrap = 'none', font = ("courier",14),tabs =("0.4i"))

# hyperlink = HyperlinkManager(wtext)



import historyWidget

historyClick = historyWidget.HistoryClickManager()
# historyClick.setIDE(toIDE[variable_ide.get()])

def saveTohistoryClick(data):
    historyClick.addEnt(data)

wtext.setClickCallback(saveTohistoryClick)




frame_path = tk.Frame(frame1)
frame_path.grid(row = 0 ,column =1,columnspan = 4)

# epath = tk.Entry(frame_path,width = 105, font = ("courier",14) )
epathFont = tkFont.Font(family='courier', size=14)
epathFontSmall = tkFont.Font(family='courier', size=10)
epath = wEntry(frame_path,width = 86, font = epathFont )
epath.insert(0,path)
epath.bind("<Down>",lambda e:eword.focus())
epath.bind("<Button-3>",pathHistory)
epath.bind("<Return>",startFind)
# epath.bind("<Control-space>",epathKey)
epath.grid(row = 0 ,column =1,columnspan = 4,  sticky='w')

# epath_second = tk.Entry(frame_path,width = 120, font = ("courier",10) )
epath_second = wEntry(frame_path,width = 120, font = epathFontSmall )
epath_second.grid(row = 1 ,column = 1,columnspan = 4,  sticky='w')
epath_second.insert(0,";".join(history.getlsitPaths2())+";")

class WE(tk.Entry, WidgetBackEntry):
    def __init__(self,root,*w,**kw):
        tk.Entry.__init__(self,root,*w,**kw )
        WidgetBackEntry.__init__(self,root,*w,**kw )


eword = WE(frame1,width = 70, font = ("courier",14), bg= "AliceBlue" )
eword.insert(0,word)
eword.bind("<Button-2>",insert2eword)
eword.bind("<ButtonRelease-2>",eventIgnore)

eword.bind("<Button-3>",wordHistory)
eword.bind("<Return>",startFind)
eword.bind("<Down>",lambda e:ext_wiget.focus())
eword.bind("<Up>",lambda e:epath.focus())

extvalidator  = ExtNotify()
# ext_wiget = tk.Entry(frame1,width = 50, font = ("courier",14) )
# ext_wiget.insert(0,savedext)
# ext_wiget.bind("<Return>",startFind)
# ext_wiget.bind("<Up>",lambda e:eword.focus())

def parseEx(txt):
    status = ""
    out = []
    lastchar = ""
    start = 0
    word = ""
    for i, char in enumerate(txt):
        if char.isspace():
            if status:
                if word:
                    out.append([status, start, i,word])
                    status = ""
                    word = ""
                else:
                    out.append(["error", start, 999,word])
                    return out
            word = ""

        elif char == "+":
            if status or word:
                out.append(["error", i, 999,word])
                return out
            start = i
            status = "include"

        elif char == "-":
            if status or word:
                out.append(["error", i, 999,word])
                return out

            start = i
            status = "exclude"

        else:
            if not status:
                out.append(["error", i, 999,word])
                return out
            word = word + char

    if status:
        if word:
            out.append([status, start, i+1,word])
        else:
            out.append(["error", i, 999,word])


    return out


def ext_wiget_Return(e):
    startFind()
    return "break"

def ext_wiget_key(e):
    txt = ext_wiget.get("0.0", "end")
    if not e or (e.char and txt and "\n" in txt[:-1]):
        ext_wiget.delete("0.0","end")
        txt = txt.replace("\n", "")
        ext_wiget.insert("0.0",txt)

    ext_wiget.tag_remove("include", "0.0", tk.END)
    ext_wiget.tag_remove("exclude", "0.0", tk.END)
    ext_wiget.tag_remove("error",   "0.0", tk.END)

    for res in parseEx(txt):
        ext_wiget.tag_add(res[0], "1.%s"%res[1],"1.%s"%res[2])



class WT(tk.Text, WidgetBackText):
    def __init__(self,root,*w,**kw):
        tk.Text.__init__(self,root,*w,**kw )
        WidgetBackText.__init__(self,root,*w,**kw )
   

ext_wiget = WT(frame1,wrap = 'none', font = ("courier",14),tabs =("0.2i"),height=1)
ext_wiget.delete("0.0","end")
ext_wiget.insert("0.0",savedext)
ext_wiget.initHist()

ext_wiget.bind("<KeyRelease>",ext_wiget_key)
ext_wiget.bind("<Return>",ext_wiget_Return)
ext_wiget.bind("<Up>",lambda e:eword.focus())
# ext_wiget.tag_config("here",  foreground="blue",background="DarkKhaki")   
ext_wiget.tag_config("include",  foreground="blue")   
ext_wiget.tag_config("exclude",  foreground="red")   
ext_wiget.tag_config("error",  foreground="black",background="red")   
# eword2.tag_add("here", "1.1","2.5")
ext_wiget_key(None)




tk.Label(frame1,text = "PATH", font = ("courier",10) ).grid(row = 0 ,column =0, sticky='w')
tk.Label(frame1,text = "WORD", font = ("courier",10) ).grid(row = 1 ,column =0, sticky='w')
tk.Label(frame1,text = "EXT ", font = ("courier",10) ).grid(row = 3 ,column =0, sticky='w')


eword.grid(row = 1 ,column =1, sticky='w')
ext_wiget.grid(row = 3 ,column =1, sticky='w')

ob_dir = tk.Button(frame1,text = "..",command=opendirdialog)
ob_dir.grid(row = 0 ,column =5)

ob_h = tk.Button(frame1,text = "H",command=lambda: historyClick.show())
ob_h.grid(row = 0 ,column =6)

but = tk.Button(frame1,command = startFind,text = "FIND")
but.grid(row = 1 ,column =2, sticky='ew')
chrevar = tk.IntVar()
chre = tk.Checkbutton(frame1,text='re', variable=chrevar)
chre.grid(row = 1 ,column =3, sticky='ew')

fnamevar = tk.IntVar()
chfname = tk.Checkbutton(frame1,text='fname', variable=fnamevar)
chfname.grid(row = 1 ,column =4, sticky='ew')

ignCASEvar = tk.IntVar()
wignCASE = tk.Checkbutton(frame1,text='ignCASE', variable=ignCASEvar)
wignCASE.grid(row = 1 ,column =5, sticky='ew')

wholeWorldVar = tk.IntVar()
cbWholeWorld = tk.Checkbutton(frame1,text='"w"', variable=wholeWorldVar)
cbWholeWorld.grid(row = 1 ,column =6, sticky='s')

autoEncodvar = tk.IntVar()
autoEncod = tk.Checkbutton(frame1,text='aЁ', variable=autoEncodvar)
autoEncod.grid(row = 3 ,column =2, sticky='ew')


inputAddStr = tk.Entry(frame1,width = 8, font = ("courier",8) )
inputAddStr.insert(0,"0 0")
inputAddStr.grid(row = 3 ,column =3)
inputAddStr.bind("<Return>",startFind)

variable_ide =tk.StringVar(frame1)
variable_ide.trace("w", callback_variable_ide)
variable_ide.set(defIDE) # default value

choise_ide = tk.OptionMenu(frame1, variable_ide, "sublime", "notepad++", "komodo")
choise_ide.grid(row = 3 ,column =4, sticky='ew')


inputMaxSize = tk.Entry(frame1,width = 5, font = ("courier",14) )
inputMaxSize.insert(0,"0 MB")
inputMaxSize.grid(row = 3 ,column =5, sticky='ew')
inputMaxSize.bind("<Return>",startFind)


def resetColor(*e):
    eword["bg"] = "SystemWindow"

def insertFromTxt(*e):
    try:
        select = wtext.selection_get()
    except:
        return eventIgnore(*e)
    setvalentry(eword,select)    
    return eventIgnore(*e)

def selectAll(*e):
    wtext.tag_add(tk.SEL, "1.0", tk.END)
    wtext.mark_set(tk.INSERT, "1.0")
    wtext.see(tk.INSERT)
    return 'break'

def copyToBufer(e):
    select = wtext.selection_get()
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(select)
    win32clipboard.CloseClipboard()



wtext.bind("<Button-2>",insertFromTxt)
wtext.bind("<Control-a>",selectAll)
wtext.bind("<Control-A>",selectAll)
eword.bind("<ButtonRelease-2>",eventIgnore)

vscrollbar = tk.Scrollbar(root,orient='vert', command=wtext.yview)
wtext['yscrollcommand'] = vscrollbar.set
hscrollbar = tk.Scrollbar(root,orient='hor', command=wtext.xview)
wtext['xscrollcommand'] = hscrollbar.set

vscrollbar.pack(side = "right",fill = "y",expand=0)
hscrollbar.pack(side = "bottom",fill = "x",expand=0)
wtext.pack(side = "right",fill = tk.BOTH,expand=1)


init()
root.bind("<F1>",lambda e: chrevar.set(not chrevar.get()))
root.bind("<Alt-r>",lambda e: chrevar.set(not chrevar.get()))
root.bind("<Control-r>",lambda e: chrevar.set(not chrevar.get()))

root.bind("<F2>",lambda e: fnamevar.set(not fnamevar.get()))
root.bind("<Alt-f>",lambda e: fnamevar.set(not fnamevar.get()))
root.bind("<Control-f>",lambda e: fnamevar.set(not fnamevar.get()))

root.bind("<F3>",lambda e: ignCASEvar.set(not ignCASEvar.get()))
root.bind("<Alt-i>",lambda e: ignCASEvar.set(not ignCASEvar.get()))
root.bind("<Control-i>",lambda e: ignCASEvar.set(not ignCASEvar.get()))

root.bind("<F4>",lambda e: autoEncodvar.set(not autoEncodvar.get()))
root.bind("<Alt-a>",lambda e: autoEncodvar.set(not autoEncodvar.get()))
root.bind("<Control-a>",lambda e: autoEncodvar.set(not autoEncodvar.get()))

root.bind("<F5>",lambda e: wholeWorldVar.set(not wholeWorldVar.get()))
root.bind("<Alt-w>",lambda e: wholeWorldVar.set(not wholeWorldVar.get()))
root.bind("<Control-w>",lambda e: wholeWorldVar.set(not wholeWorldVar.get()))

def focusSearch(*e):
    eword.select_range(0, 'end')
    eword.icursor("end")
    eword.focus()

root.bind("<F6>",focusSearch)
root.bind("<Alt-f>",focusSearch)
root.bind("<Control-f>",focusSearch)

root.bind("<Alt-Up>", hideInhide)
root.bind("<Alt-Down>",hideInhide)
# root.bind("<F5>",startFind)

butHide = tk.Button(root,command = hideInhide,text = "^")
butHide.place(relx=1, x=-5, y=2, anchor=tk.NE)


autoEncodvar.set(1)
ignCASEvar.set(1)
eword.focus()




class MyStd(object):
    def __init__(self):
        self.f = open("log.txt","a")

    def write(self, string):
        self.f.write( string)
        try:
        	original_stdout.write(string)
        except Exception, e:
        	self.f.write( "original_stdout.write ERROR: %s"%str(e))

    def close(self):
        self.f.close()

    def flush(self):
        self.f.flush()






# original_stderr = sys.stderr
# original_stdout = sys.stdout
# myWriter = MyStd()
# sys.stderr = myWriter
# sys.stdout = myWriter


# eword2 = tk.Text(frame1,wrap = 'none', font = ("courier",14),tabs =("0.4i"),height=1)
# eword2.grid(row = 3 ,column =1, sticky='w')
# eword2.insert('0.0',word+'jfrfgghhgfffffff')
# eword2.tag_config("here",  foreground="blue",background="DarkKhaki")   
# eword2.tag_add("here", "1.1","2.5")



root.mainloop()


