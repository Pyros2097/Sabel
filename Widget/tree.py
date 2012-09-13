from PyQt4.QtGui import (QTreeWidgetItem,QTreeWidget,QMessageBox,
                         QIcon,QDrag,QMenu,QAction,QInputDialog,QCursor,QToolBar,
                         QHeaderView,QFileDialog)
from PyQt4.QtCore import SIGNAL,Qt,QMimeData,QUrl,QPoint
from globals import (oslistdir,ospathisdir,ospathsep,ospathjoin,ospathexists,
                     ospathbasename,os_icon,osremove,osrename,ospathdirname,
                     recycle,ospathnormpath,oswalk,Icons,config)


class Dir(QTreeWidgetItem):
    def __init__(self,parent,name,path):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(path,name)
        self.setText (0, name)
        self.setIcon(0,Icons.foldej)
    
    def getPath(self):
        return self.path
    def isProject(self):
        return False
    def isDir(self):
        return True
    def isFile(self):
        return False

class File(QTreeWidgetItem):
    ext = [".txt",".nut",".py",".cpp",".c",".h"]
    def __init__(self,parent,name,path):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(path,name)
        self.setText (0, name)
        self.doc = False
        self.pic = False
        self.audio = False
        #mime = QMimeData()
        #mime.setUrls([QUrl.fromLocalFile(self.path)])
        #print self.path+":"+str(mime.hasUrls())
        self.setIcon(0,Icons.file_obj)
        self.Doc(name)
        self.Pic(name)
        self.Audio(name)
        
    def Doc(self,name):
        for e in self.ext:
            if name.endswith(e):
                self.setIcon(0,Icons.file_obj)
                self.doc = True
            
    def Pic(self,name):
        if(name.endswith(".png") or name.endswith(".gif") or name.endswith(".jpg")):
            self.setIcon(0,Icons.image)
            self.pic = True
            
    def Audio(self,name):
        if(name.endswith(".wav") or name.endswith(".mp3") or name.endswith(".ogg")):
            self.setIcon(0,Icons.image)
            self.audio = True
        
    def getPath(self):
        return self.path
    def isProject(self):
        return False
    def isDir(self):
        return False
    def isFile(self):
        return True
    def isDoc(self):
        return self.doc
    def isPic(self):
        return self.pic
    def isAudio(self):
        return self.audio
        
class Project(QTreeWidgetItem):
    Count = -1
    def __init__(self,parent,startDir,closed = False):
        QTreeWidgetItem.__init__(self,parent)
        self.path = ospathjoin(startDir)
        self.closed = closed
        if(self.closed):
            self.setIcon(0,Icons.cprj)
        else:
            self.setIcon(0,Icons.prj)
        self.setText (0, ospathbasename(ospathnormpath(startDir))) # set the text of the first 0
        self.setToolTip(0,startDir)
        self.Count += 1
        self.setExpanded(True)
        
        
    
    def getPath(self):
        return self.path
    
    def isProject(self):
        return True
    def isDir(self):
        return False
    def isFile(self):
        return False
    def isClosed(self):
        return self.closed
        
class ProjectTree(QTreeWidget):
    def __init__(self,parent = None):
        QTreeWidget.__init__(self,parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setColumnCount(1)
        self.header().close()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self,SIGNAL("customContextMenuRequested(const QPoint &)"), self.doMenu)
        self.connect(self, SIGNAL("dropped"), self.addItem)
        self.projects = []
        self.closed = config.closedProjects()
        if(self.closed == None):
            self.closed = []
        self.header().setStretchLastSection(False)
        self.header().setResizeMode(QHeaderView.ResizeToContents)
        #self.setColumnWidth(0,280)
        
    def initProjects(self):
        for pro in config.projects():
            self.createProject(pro)
            
    def readDir(self,parent,path):
        for d in oslistdir(path):
            if  ospathisdir(ospathjoin(path,d)):
                if not ospathjoin(d).startswith('.'):
                    i = Dir(parent,d,path)
                    self.readFiles(i,ospathjoin(path,d))
                    
    def readMainDir(self,parent,path):
        for d in oslistdir(path):
            if  ospathisdir(ospathjoin(path,d)):
                if not ospathjoin(d).startswith('.'):
                    i = Dir(parent,d,path)
                    self.readMainFiles(i,ospathjoin(path,d))
        
    def readFiles(self,parent,path):
        for f in oslistdir(path):
            if ospathisdir(ospathjoin(path,f)):
                d = Dir(parent,f,path)
                self.readFiles(d,ospathjoin(path,f))    
            else:
                if not ospathjoin(f).startswith('.'):
                        File(parent,f,path)
                        
                        
    def readMainFiles(self,parent,path):
        for f in oslistdir(path):
            if not ospathisdir(ospathjoin(path,f)):
                if not ospathjoin(f).startswith('.'):
                        File(parent,f,path)
                        
                        
    def newProject(self):
        fname = str(QFileDialog.getExistingDirectory(self,"Open Project Folder"))
        if not (fname == ""):
            fname = fname+"/"
            if len(self.projects) != 0:
                if(fname in self.projects):
                    QMessageBox.about(self, "Already Open","Project Already Open\n"+fname)
                else:
                    self.createProject(fname)
            else:
                self.createProject(fname)
    
    #Important all projects must go through this          
    def createProject(self,startDir):
        if(ospathexists(startDir)):
            self.projects.append(startDir)
            self.addProject(startDir)
            config.setProject(self.projects)
            #print "adding"+startDir
        else:
            #print "removing"+startDir
            self.projects.remove(startDir)
            config.setProject(self.projects)
            QMessageBox.about(self,"Can't Open Project","Project Does Not Exist %s"%startDir)
    
                
                
    def addProject(self,startDir):
        if(len(self.closed) == len(self.projects)):
            self.closed.append(0)
        if(self.closed[self.projects.index(startDir)] == 0):
            i = Project(self,startDir)
            self.addTopLevelItem(i)
            self.readDir(i,startDir)
            self.readMainFiles(i,startDir)
        else:
            i = Project(self,startDir,True)
            self.addTopLevelItem(i)    
            
    def addClosedProject(self,startDir):
        if(ospathexists(startDir)):
            self.closed[self.projects.index(startDir)] = 1
            i = Project(self,startDir,True) 
            self.addTopLevelItem(i)
            config.setClosedProjects(self.closed)
        else:
            QMessageBox.about(self,"Can't Close Project","Project Does Not Exist %s"%startDir)
    
    def removeProject(self,item):
        itemPath = item.getPath()
        self.closed.pop(self.projects.index(itemPath))
        config.setClosedProjects(self.closed)
        self.projects.remove(itemPath)
        config.setProject(self.projects)
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        
        
      
    def addItem(self,links):
        print links
                
    def startDrag(self, dropAction):
        # create mime data object
        mime = QMimeData()
        mime.setData('text/xml', '???')
        # start drag 
        drag = QDrag(self)
        drag.setMimeData(mime)        
        drag.start(Qt.CopyAction | Qt.CopyAction)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()    

    def dropEvent(self, event): 
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
                #item = File(self)
                #item.setText(0, ospathbasename(str(url.toLocalFile())))
                #self.addTopLevelItem(item)
            self.emit(SIGNAL("dropped"), links)      
        else:
            event.ignore()    
                
    def doMenu(self, pos):
        index = self.indexAt(pos)

        if not index.isValid():
            return

        item = self.itemAt(pos)
        menu = QMenu(self)
        action_Folder = QAction(Icons.newfolder,'New Folder', self)
        action_Folder.triggered.connect(lambda:self.newFolder(item))
        action_File = QAction(Icons.new_file,'New File', self)
        action_File.triggered.connect(lambda:self.newFile(item))
        action_Open = QAction('Open', self)
        action_Open.triggered.connect(lambda:self.openProject(item))
        action_Close = QAction('Close', self)
        action_Close.triggered.connect(lambda:self.closeProject(item))
        
        action_OpenFile = QAction(Icons.open,'Open', self)
        action_OpenFile.triggered.connect(lambda:self.openFile(item))
        action_RunFile = QAction(Icons.go,'Python Run', self)
        action_RunFile.triggered.connect(lambda:self.runFile(item))
        action_CopyFile = QAction(Icons.file_obj,'Copy', self)
        action_CopyFile.triggered.connect(lambda:self.copyFile(item))
        action_CopyDir = QAction(Icons.file_obj,'Copy', self)
        action_CopyDir.triggered.connect(lambda:self.copyDir(item))
        action_PasteFile = QAction(Icons.paste_edit,'Paste', self)
        action_PasteFile.triggered.connect(lambda:self.pasteFile(item))
        action_PasteDir = QAction(Icons.paste_edit,'Paste', self)
        action_PasteDir.triggered.connect(lambda:self.pasteDir(item))
        action_RefreshProject = QAction(Icons.refresh_tab,'Refresh', self)
        action_RefreshProject.triggered.connect(lambda:self.refreshProject(item))
        action_RemoveProject = QAction('Remove', self)
        action_RemoveProject.triggered.connect(lambda:self.removeProject(item))
        action_RenameProject = QAction('Rename...', self)
        action_RenameProject.triggered.connect(lambda:self.renameProject(item))
        action_RenameDir = QAction('Rename...', self)
        action_RenameDir.triggered.connect(lambda:self.renameDir(item))
        action_RenameFile = QAction('Rename...', self)
        action_RenameFile.triggered.connect(lambda:self.renameFile(item))
        action_DeleteFile = QAction(Icons.trash,'Delete', self)
        action_DeleteFile.triggered.connect(lambda:self.deleteFile(item))
        action_DeleteDir = QAction(Icons.trash,'Delete', self)
        action_DeleteDir.triggered.connect(lambda:self.deleteDir(item))
        action_DeleteProject = QAction(Icons.trash,'Delete', self)
        action_DeleteProject.triggered.connect(lambda:self.deleteProject(item))
        
        action_CreateProject = QAction('Create', self)
        action_CreateProject.triggered.connect(lambda:self.create(item))
        action_BuildProject = QAction('Build', self)
        action_BuildProject.triggered.connect(lambda:self.build(item))
        action_BuildRunProject = QAction('Build and Run', self)
        action_BuildRunProject.triggered.connect(lambda:self.buildRun(item))
        action_CleanProject = QAction('Clean', self)
        action_CleanProject.triggered.connect(lambda:self.clean(item))
        action_RunProject = QAction('Run', self)
        action_RunProject.triggered.connect(lambda:self.run(item))
        if(item.isProject()):
            if not(item.isClosed()):
                menu.addAction(action_Folder)
                menu.addAction(action_File)
                menu.addSeparator()
                menu.addAction(action_CreateProject)
                menu.addAction(action_BuildProject)
                menu.addAction(action_BuildRunProject)
                menu.addAction(action_RunProject)
                menu.addAction(action_CleanProject)
                menu.addSeparator()
                menu.addAction(action_RenameProject)
                menu.addAction(action_RemoveProject)
                menu.addAction(action_DeleteProject)
                menu.addSeparator()
                menu.addAction(action_RefreshProject)
                menu.addAction(action_Close)
            else:
                menu.addAction(action_Open)
        else:
            if(item.isDir()):
                menu.addAction(action_Folder)
                menu.addAction(action_File)
                menu.addSeparator()
                menu.addAction(action_CopyDir)
                menu.addAction(action_PasteDir)
                menu.addAction(action_RenameDir)
                menu.addAction(action_DeleteDir)      
            else:
                menu1 = QMenu(self)
                menu1.setTitle("Run As")
                menu1.addAction(action_RunFile)
                
                menu.addAction(action_OpenFile)
                menu.addMenu(menu1)
                menu.addSeparator()
                menu.addAction(action_CopyFile)
                menu.addAction(action_PasteFile)
                menu.addAction(action_RenameFile)
                menu.addAction(action_DeleteFile)
                
        menu.popup(QCursor.pos())
        
    def openProject(self,item):
        itempath = item.getPath()
        self.closed[self.projects.index(itempath)] = 0
        config.setClosedProjects(self.closed)
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addProject(itempath)
        
    def closeProject(self,item):
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addClosedProject(item.getPath())
        #print self.indexOfTopLevelItem(item)
        #self.closed[self.indexOfTopLevelItem(item)] = 1
        #config.addClosedProjects(self.closed)
    
    def refreshProject(self,item):
        #must check this
        itempath = item.getPath()
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        self.addProject(itempath)
        
    def refreshAllProjects(self):
        for pro in self.projects:
            ind = self.projects.index(pro)
            #self.takeTopLevelItem(ind)
            if(self.closed[ind]):
                print ind+pro
                self.addClosedProject(pro)
            else:
                print ind+pro
                self.addProject(pro)
        
    
    def newFolder(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","Name:")
        if (ok and text != ''):
            fname = ospathdirname(item.getPath())
            try:
                print fname+'/'+text
                #osmkdir(fname+'/'+text,0755)
            except:
                QMessageBox.about(self,"Error","Could Not Create The File")
    def newFile(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","Name:") 
        if (ok and text != ''):
            fname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                nfile = open(fname,'w')
                nfile.close()
                f = File(item,ospathbasename(fname),ospathdirname(fname))
                item.addChild(f)
            except:
                QMessageBox.about(self,"Error","Could Not Create The File")
    
    def openFile(self,item):
        self.emit(SIGNAL("openFileClicked"),item)
                
    def runFile(self,item):
        pass
                
    def copyFile(self,item):
        pass
    
    def copyDir(self,item):
        pass
    
    def pasteFile(self,item):
        pass
    
    def pasteDir(self,item):
        pass
    
    def create(self,item):
        self.emit(SIGNAL("create"),item)
    def build(self,item):
        self.emit(SIGNAL("build"),item)
    def buildRun(self,item):
        self.emit(SIGNAL("buildRun"),item)
    def clean(self,item):
        self.emit(SIGNAL("clean"),item)
    def run(self,item):
        self.emit(SIGNAL("run"),item)
        
    def renameProject(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath))
            try:
                print itempath
                print newname
                #osrename(itempath,newname)
                #self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                #self.addProject(newname)
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
    
    def renameDir(self,item):
        itempath = item.getPath()
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                print newname
                osrename(itempath,newname)
                p = item.parent()
                p.removeChild(item)
                #self.refreshAllProjects()
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
        
    def renameFile(self,item):
        text,ok = QInputDialog.getText(self,"QInputDialog::getText()","New Name:")
        itempath = item.getPath()
        if (ok and text != ''):
            newname = ospathjoin(ospathdirname(itempath),str(text))
            try:
                #print newname
                osrename(itempath,newname)
                p = item.parent()
                p.removeChild(item)
                f = File(p,ospathbasename(newname),ospathdirname(newname))
                p.addChild(f)
            except:
                QMessageBox.about(self,"Error","Could Not Rename The File")
                
    def deleteDir(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                pass
            #implement
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")
                
    def deleteProject(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                pass
            #implement
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")
        
    def deleteFile(self,item):
        reply = QMessageBox.question(self,
                    "Delete",
                    "Are you sure you want to Delete,This Will Send To Recycle Bin?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            return
        elif reply == QMessageBox.Yes:
            try:
                itempath = item.getPath()
                p = item.parent()
                p.removeChild(item)
                recycle(itempath)
            except:
                QMessageBox.about(self,"Error","Could Not Delete The File")
                
                
class Error(QTreeWidgetItem):
    def __init__(self,parent,line,text):
        QTreeWidgetItem.__init__(self,parent)
        self.closed = False
        if(self.closed):
            self.setIcon(0,Icons.error)
        else:
            self.setIcon(0,Icons.error)
        self.setText(0,"Line: "+line)
        self.setText(1,text)
        
class ErrorTree(QTreeWidget):
    def __init__(self,parent = None):
        QTreeWidget.__init__(self,parent)
        self.errorCount = 0
        self.setColumnCount(2)
        self.setHeaderLabels(["Line","Error"])
        
    def addError(self,errorlist):
        self.errorCount+=1
        i = Error(self,errorlist[0],errorlist[2])
        self.addTopLevelItem(i)
        
    def reset(self):
        #print self.topLevelItemCount()
        if(self.topLevelItemCount() != 0):
            self.clear()
        self.errorCount = 0
        
class OutlineTree(QTreeWidget):
    def __init__(self,parent = None):
        QTreeWidget.__init__(self,parent)
        self.setColumnCount(1)
        self.header().close()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
 