# 
# -*- coding: utf-8 -*-
#


import Tkinter
import tkFont
import os


class WidgetBack(object):
	def __init__(self, *e, **kw):
		self.__histback = []
		self.__current = ""
		self.__histforward = []
		self.bind("<Control-z>",self.__Back)
		self.bind("<Control-y>",self.__Forward)
		self.bind("<Key>", self.__keyPress)


	def initHist(self):
		self.__keyPressAfter()
		
	def getText(self):
		raise ValueError

	def setText(self, text):
		raise ValueError

	def __keyPress(self, *e):
		self.after(2, self.__keyPressAfter )

	def __keyPressAfter(self, *e):
		text = self.getText()
		if self.__current == text:
			return
		if self.__histback and self.__histback[-1] == self.__current:
			return
		if self.__histforward and self.__histforward[-1] == self.__current:
			return
		self.__histback.append(self.__current)
		self.__current = text

	def __Back(self, *e):
		if not self.__histback:
			return
		text =  self.__histback.pop()
		self.__histforward.append(self.__current)
		self.setText(text)
		self.__current = text

	def __Forward(self, *e):
		if not self.__histforward:
			return
		text =  self.__histforward.pop()
		self.__histback.append(self.__current)
		self.setText(text)
		self.__current = text

 
class WidgetBackText(WidgetBack):
	def getText(self):
		return self.get("0.0", "end").strip()

	def setText(self, text):
		self.delete("0.0","end")
		self.insert("0.0",text)


class WidgetBackEntry(WidgetBack):
	def getText(self):
		return self.get().strip()

	def setText(self, text):
		self.delete(0, Tkinter.END)
		self.insert(Tkinter.END, text )

								





if __name__ == '__main__':
   
	
	root = Tkinter.Tk()
	appHighlightFont = tkFont.Font(family='Helvetica', size=14)
	class WE(Tkinter.Entry, WidgetBackEntry):
		def __init__(self,root,*w,**kw):
			Tkinter.Entry.__init__(self,root,*w,**kw )
			WidgetBack.__init__(self,root,*w,**kw )

	class W(Tkinter.Entry, WidgetBackEntry):
		def __init__(self,root,*w,**kw):
			Tkinter.Entry.__init__(self,root,*w,**kw )
			WidgetBackEntry.__init__(self,root,*w,**kw )
			
	class WT(Tkinter.Text, WidgetBackText):
		def __init__(self,root,*w,**kw):
			Tkinter.Text.__init__(self,root,*w,**kw )
			WidgetBackText.__init__(self,root,*w,**kw )
			
			


	Tkinter.Label(root,text = "sadasdasd").pack()
	  

	w = WE(root, width = 105, font = appHighlightFont)
	w.pack()
	w.focus()
	w = WT(root, width = 105, font = appHighlightFont)
	w.pack()
	w.focus()

	WE(root).pack(side = Tkinter.LEFT)
	# wEntry(root).pack(side = Tkinter.LEFT)
	WE(root).pack(side = Tkinter.TOP)
	# wEntry(root).pack(side = Tkinter.TOP)
	# wEntry(root).pack(side = Tkinter.BOTTOM)
	# wEntry(root).pack(side = Tkinter.BOTTOM)
	# wEntry(root).pack(side = Tkinter.BOTTOM)
	# wEntry(root).pack(side = Tkinter.LEFT)

	Tkinter.Label(text = "sadasdasd").pack(side = Tkinter.LEFT)
	Tkinter.Label(text = "sadawdadawdawdasdasd2").pack(side = Tkinter.TOP)
	root.mainloop()
