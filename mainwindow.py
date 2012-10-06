from PyQt4.QtGui import (QApplication,QPixmap,QSplashScreen,QMessageBox,
                         QIcon,QAction,QCheckBox,QFileDialog)
from PyQt4.QtCore import SIGNAL,Qt,QStringList,QString
from window import Window
from Widget import Editor,PyInterp,Adb,Ant,Parser,Command,Audio,Image,Tool
from globals import (ospathsep,ospathjoin,ospathbasename,workDir,config,workSpace,
                     iconSize,iconDir,ospathexists,os_icon)
import sys

class MainWindow(Window):
    def __init__(self, parent = None):
        Window.__init__(self,parent)
	#Important must be empty this is a reference
        self.files = []
        self.recent = None
        self.dirty = None
        self.isFull = False
        self.adb = Adb(self)
        self.parser = Parser(self)
        self.command = Command(self)
        self.ant = Ant(self)

    def init(self):
        self.toolBar = Tool(self)
        self.addToolBar(self.toolBar)
        self.initConfig()
        self.treeWidget.initProjects()
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTabs)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.treeWidget.itemDoubleClicked.connect(self.treeItemClicked)
        self.outlineWidget.itemDoubleClicked.connect(self.gotoLine)
        self.errorTree.itemDoubleClicked.connect(self.errorLine)
        self.connect(self.treeWidget,SIGNAL("openFileClicked"),self.treeItemClicked)
        self.connect(self.treeWidget,SIGNAL("create"), lambda x:self.ant.create(x))
        self.connect(self.treeWidget,SIGNAL("build"), lambda x:self.ant.build(x))
        self.connect(self.treeWidget,SIGNAL("buildRun"), lambda x:self.ant.buildRun(x))
        self.connect(self.treeWidget,SIGNAL("clean"), lambda x:self.ant.clean(x))
        self.connect(self.treeWidget,SIGNAL("run"), lambda x:self.ant.run(x))
        #self.initInterpreter()

    def initConfig(self): 
        self.recent = config.recent()
        self.dirty = []
        if(config.files() != None):
            if(len(config.files()) != 0):
                for i in config.files():
                    self.createTab(i)
          
    def treeItemClicked(self,item):
        if(item.isFile()):
            if(item.isDoc()):
                self.createTab(item.getPath())
            elif(item.isPic()):
                self.openImage(item.getPath())
            elif(item.isAudio()):
                self.openAudio(item.getPath())
        
    def initInterpreter(self):
        self.ipy = PyInterp(self)
        self.ipy.initInterpreter(locals())
        self.tabWidget_3.addTab(self.ipy, "Python")

    '''Must go through this only'''
    def createTab(self,nfile):
        if(nfile != None):
            if(self.files != None):
                if(len(self.files) != 0):
                        if(nfile in self.files):
                            #print "File Already Open\n"+nfile
                            self.tabWidget.setCurrentIndex(self.files.index(nfile))
                            return False
                if(ospathexists(nfile)):
                        self.openEditor(nfile)  
                        return True    
                else:
                    if(nfile in self.files):
                        self.files.remove(nfile)
                    config.setFile(self.files)
                    QMessageBox.about(self,"Can't Open","File Does Not Exist\n"+nfile) 
                    return False
                           
    def createTabs(self,links):
        if(links != None):
            if(len(links) != 0):
                for i in links:
                    self.createTab(i)
            
    def openEditor(self,nfile):
        text = ""
        try:
            infile = open(nfile, 'r')
            tt = infile.read()
            text = unicode(tt,"utf-8")#must add utf-8 for it to work

            #infile.close()
            self.files.append(nfile)
            config.setFile(self.files) 
            self.dirty.append(False)
            #print len(self.files)
            tab = Editor(self,text,self.syntax(nfile),self.colorStyle) 
            self.tabWidget.addTab(tab,ospathbasename(nfile))
            tab.textChanged.connect(lambda:self.setDirty(nfile))  
            if(self.files != None):
                if(len(self.files)) != 0:
                    #This line sets the opened file to display first Important not checked
                    self.tabWidget.setCurrentIndex(len(self.files)-1)
            return True
        except:
            if(nfile in self.files):
                self.files.remove(nfile)
            config.setFile(self.files)
            QMessageBox.about(self,"Can't Open","File is Being Used\n"+nfile)
            return False
        finally:
            if(infile != None):
                infile.close()
            
               
    def openImage(self,nfile):
        if(ospathexists(nfile)):
            form = Image(self,nfile)
            form.show()
            return True
        else:
            QMessageBox.about(self,"Can't Open","File Does Not Exist\n"+nfile)
            return False
        #print nfile
        #self.tiler.addImage(nfile)
        #self.tiler.show()
        
    def openAudio(self,nfile):
        if(ospathexists(nfile)):
            form = Audio(self,nfile)
            form.show()
            return True
        else:
            QMessageBox.about(self,"Can't Open","File Does Not Exist\n"+nfile)
            return False
            
    def closeTab(self,index):
        '''Boolean result invocation method.'''
        done = True
        if self.dirty[index]:
            reply = QMessageBox.question(self,
                    "Sabel IDE - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                done = False
            elif reply == QMessageBox.Yes:
                done = self.fileSave(index)
            elif reply == QMessageBox.No:
                self.clearDirty(index)
                done = True
        if(done):
            #print index
            '''Must set the editor text to None to gc the memory used by text'''
            self.files.remove(self.files[index])
            config.setFile(self.files)
            self.tabWidget.removeTab(index)

    def setDirty(self,file):
        '''On change of text in textEdit window, set the flag
        "dirty" to True'''
        index = self.files.index(file)
        if self.dirty[index]:
            return True
        self.dirty[index] = True
        flbase = ospathbasename(self.files[index])
        self.tabWidget.setTabText(index,"*"+flbase)

    def clearDirty(self,index):
        '''Clear the dirty.'''
        self.dirty[index] = False
        flbase = ospathbasename(self.files[index])
        self.tabWidget.setTabText(index,flbase)

    def fileOpen(self):
        fname = str(QFileDialog.getOpenFileName(self,"Open File", '.', "Files (*.*)"))
        if not (fname == ""):
            if self.files != None:
                if len(self.files) != 0:
                        if(fname in self.files):
                            self.createTab(fname)
                            return True
                        else:
                            QMessageBox.about(self, "Already Open","File Already Open")
                            return False
                else:
                    self.createTab(fname)
            else:
                self.files = []
                self.createTab(fname)

    def fileSave(self):
        if(self.files != None):
            if len(self.files) != 0:
                index = self.tabWidget.currentIndex()
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                try:
                    fl = open(fname, 'w')
                    self.statusSaving()
                    self.progressStart()
                    tempText = unicode(self.tabWidget.widget(index).text())
                    if tempText:
                        fl.write(tempText.encode("utf-8"))
                        fl.close()
                        self.clearDirty(index)
                    else:
                        QMessageBox.about(self, "Can't Save","Failed to save ...")
                except:
                    QMessageBox.about(self, "Can't Save","File is Locked")
                self.statusWriting()
                self.progressStop()
                self.parser.run(self.files[index])
                #must implement for all files

    def fileSaveAll(self):
        def fileSaveIndex(index):
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                try:
                    fl = open(fname, 'w')
                    self.statusSaving()
                    self.progressStart()
                    tempText = unicode(self.tabWidget.widget(index).text())
                    if tempText:
                        fl.write(tempText.encode("utf-8"))
                        fl.close()
                        self.clearDirty(index)
                    else:
                        QMessageBox.about(self, "Can't Save","Failed to save ...")
                    self.statusWriting()
                    self.progressStop()
                except:
                    QMessageBox.about(self, "Can't Save","File is Locked")
        if(self.files != None):
            if len(self.files) != 0:
                for file in self.files:
                    fileSaveIndex(self.files.index(file))


    def closeEvent(self, event):
        #check this adb.exe process is always on
        self.adb.close()
        self.parser.close()
        self.command.close()
        self.ant.close()
        notSaved = False
        for files in self.dirty:
            if files == True:
                notSaved = True
        if notSaved:
            reply = QMessageBox.question(self,
                                             "Sabel - Unsaved Changes",
                                             "Save unsaved changes?",
                                             QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                    pass
            elif reply == QMessageBox.Yes:
                    self.fileSaveAll()
        sys.exit()
                    
    def syntax(self,nfile):
        lang = 0
        if nfile.endswith(".py"):
            lang = 0
        elif (nfile.endswith(".cpp") or nfile.endswith(".h") or nfile.endswith(".c") or nfile.endswith(".hpp")):
            lang = 1
        elif nfile.endswith(".nut"):
            lang = 2
        elif nfile.endswith(".neko"):
            lang = 2
        return lang
