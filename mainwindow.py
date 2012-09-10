from PyQt4.QtGui import (QApplication,QPixmap,QSplashScreen,QMessageBox,
                         QIcon,QAction,QCheckBox,QFileDialog)
from PyQt4.QtCore import SIGNAL,Qt,QStringList,QString
from window import Window
from Widget import Editor,PyInterp,Adb,Ant,Parser,Command,Audio,Image
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
        self.initToolBar()
        self.initConfig()
        self.treeWidget.initProjects()
        self.connect(self, SIGNAL('triggered()'), self.closeEvent)
        self.connect(self.tabWidget,SIGNAL("dropped"), self.createTabs)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.treeWidget.itemDoubleClicked.connect(self.treeItemClicked)
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

    def createTab(self,nfile):
        if(nfile != None):
            if(self.files != None):
                if(len(self.files) != 0):
                        if(nfile in self.files):
                            #print "File Already Open\n"+nfile
                            self.tabWidget.setCurrentIndex(self.files.index(nfile))
                if(ospathexists(nfile)):
                    self.openEditor(nfile)          
                else:
                    #dont know must check this the last file is not removed executes only
                    #1 when it has to remove 2 files
                    #check sel.files 
                    #print len(config.files())
                    print "removing"+nfile
                    self.files.remove(nfile)
                    config.setFile(self.files)
                    QMessageBox.about(self,"Can't Open","File Does Not Exist\n"+nfile) 
                           
    def createTabs(self,links):
        for i in links:
            self.createTab(i)
            
    def openEditor(self,nfile):
        text = ""
        try:
            infile = open(nfile, 'r')
            text = infile.read()
            infile.close()
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
        except:
            #print "removing"+nfile
            self.files.remove(nfile)
            config.setFile(self.files)
            QMessageBox.about(self,"Can't Open","File is Being Used\n"+nfile)
               
    def openImage(self,nfile):
        form = Image(self,nfile)
        form.show()
        #print nfile
        #self.tiler.addImage(nfile)
        #self.tiler.show()
        
    def openAudio(self,nfile):
        form = Audio(self,nfile)
        form.show()
            
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
                            return
                        else:
                            QMessageBox.about(self, "Already Open","File Already Open")
                            return
                else:
                    self.createTab(fname)
            else:
                #print "not"
                #this is when the files list is empty and None type
                self.files = []
                self.createTab(fname)

    def fileSave(self):
        if(self.files != None):
            if len(self.files) != 0:
                index = self.tabWidget.currentIndex()
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                fl = open(fname, 'w')
                tempText = self.tabWidget.widget(index).text()
                if tempText:
                    fl.write(tempText)
                    fl.close()
                    self.clearDirty(index)
                    self.parser.run(self.files[index])
                else:
                    QMessageBox.about(self, "Can't Save","Failed to save ...")
                    self.statusBar().showMessage('Failed to save ...', 5000)

    def fileSaveAll(self):
        def fileSaveIndex(index):
                if not self.dirty[index]:
                    return
                fname = self.files[index]
                fl = open(fname, 'w')
                tempText = self.tabWidget.widget(index).text()
                if tempText:
                    fl.write(tempText)
                    fl.close()
                    self.clearDirty(index)
                else:
                    QMessageBox.about(self, "Can't Save","Failed to save ...")
                    self.statusBar().showMessage('Failed to save ...', 5000)
        if(self.files != None):
            if len(self.files) != 0:
                for file in self.files:
                    fileSaveIndex(self.files.index(file))


    def closeEvent(self, event):
        #check this ine adb.exe process is always on
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
                                             "Simple Editor - Unsaved Changes",
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
        elif (nfile.endswith(".cpp") or nfile.endswith(".h") or nfile.endswith(".c")):
            lang = 1
        elif nfile.endswith(".nut"):
            lang = 2
        return lang
            
    def options(self):
        pass
