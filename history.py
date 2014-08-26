# 
# -*- coding: utf-8 -*-
#


import traceback
import pickle
import os

class History(object):
    """docstring for History"""
    def __init__(self, savePath=".",savePathCoding=".",maxHistory=20):
        self.paths = []
        self.words = []
        self.path2 = []
        self.enCodings = {}
        self.needCodingSave = 0
        self.maxHistory = maxHistory
        self.lastExt = "-* +py +cpp +hpp +ipp +json +xml +txt"
        self.savePath = os.path.join(savePath, "findCool.pkl")
        self.savePathCoding = os.path.join(savePathCoding, "findCoolCoding.pkl")
        try:
            self.load()
        except Exception as e:
            print "History load error",e
            # traceback.print_exc()

        try:
            self.loadCoding()
        except Exception as e:
            print "History loadCoding error",e
            # traceback.print_exc()
    def setExt(self, ext):
        self.lastExt = ext

    def getExt(self):
        return self.lastExt

    def checkEncoding(self,fname):
        #fname = os.path.normpath(fname)  
        out = self.enCodings.get(fname, None)
        # if not out:
        #     self.needCodingSave = 1
        return out

    def setEncoding(self,fname, coding):  
        #fname = os.path.normpath(fname)  
        self.enCodings[fname] =coding
        self.needCodingSave = 1

    def getlsitWords(self):
        return self.words

    def getlsitPathsLast(self, lenght = 1):
        retpath = self.paths[:]
        retpath.reverse()
        return retpath[:lenght]

    def getlsitPaths(self):
        retpath = self.paths[:]
        retpath.sort()
        return retpath

    def getlsitPaths2(self):
        return self.path2 

    def addVal(self, word, path,path2):
        maxlen = self.maxHistory
        path = os.path.normpath(path)
        self.path2 = path2
        if  word in self.words:
            self.words = [w for w in self.words if w != word]
        
        self.words.append(word)


        if len(self.words) > maxlen:
            self.words = self.words[-maxlen:]

        


        if  path in self.paths:
            self.paths = [w for w in self.paths if w != path]

        self.paths.append(path) 


        if len(self.paths) > maxlen:
            self.paths = self.paths[-maxlen:]  

        self.save()  

    
    def save(self):
        fname = self.savePath
        output = open(fname, 'wb')
        data = {}
        data["paths"]  =    self.paths
        data["words"] =    self.words
        data["path2"] =    self.path2  
        data["lastExt"] =    self.lastExt
        pickle.dump(data, output)
        output.close()
        print "history save to", fname

    def load(self):
        fname = self.savePath
        pkl_file = open(fname, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()

        if type(data) != dict: # conver from old format
            self.paths, self.words,self.path2 = data 
        else:
            #new format
            self.paths =data["paths"] 
            self.words =data["words"]
            self.path2   =data["path2"]
            self.lastExt =data["lastExt"]

        print self.paths, self.words,self.path2



        # self.paths = list(set([os.path.normpath(p) for p in self.paths]))
        # self.save()


        print "history load from", fname

    def loadCoding(self):
        fname = self.savePathCoding
        pkl_file = open(fname, 'rb')
        self.enCodings = pickle.load(pkl_file)
        pkl_file.close()
        print "loadCoding from", fname, len(self.enCodings)


    def saveCoding(self):
        if not self.needCodingSave:
            print "no needCodingSave"
            return
        fname = self.savePathCoding
        output = open(fname, 'wb')
        pickle.dump(self.enCodings, output)
        output.close()
        print "Codings save to", fname
        self.needCodingSave = 0



class ExtNotify(object):
    """docstring for ExtNotify"""
    def __init__(self):
        self.modify = []

    def update(self, tags):
        self.modify = [] 
        for t in tags.lower().split():
            if not t :continue
            if len(t) < 2:
                return False
            if not t.startswith("+") and not  t.startswith("-"):
                return False

            if t[0]=="+":
                self.modify.append((1,t[1:]))
            elif t[0]=="-":
                self.modify.append((0,t[1:]))
            else :
                self.modify.append((1,t))
        if not self.modify:
            return False
        return True

    def isvalid(self,path):
        path = path.lower()
        #_,ext = os.path.splitext(path)

        #if not ext:
        #    return True

        #if ext.startswith("."):
        #    ext = ext[1:]
        # ret = 0
        # for acces, prot in self.modify:
            # if prot == "*" or prot == ext:
                # ret = acces

        ret = 0
        for acces, prot in self.modify:
            if prot == "*" or path.endswith(prot):
                ret = acces

        return ret




if __name__ == '__main__':
    h = History()