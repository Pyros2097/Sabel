from PyQt4.QtGui import (QAction,QIcon,QMessageBox,QWidgetAction,QMenu,QWidget,
                         QHBoxLayout,QVBoxLayout,QTabWidget,QToolBar,QTextEdit,
                         QLineEdit,QPushButton,QToolButton,QSplitter,QStatusBar,
                         QMainWindow,QPalette,QColor,QSlider,QLabel,
                         QFont,QComboBox,QFileDialog,QInputDialog,QProgressBar
                         )      
from PyQt4.QtCore import QSize,Qt,QStringList,SIGNAL,SLOT,QString
from Widget import (EditorTab,Tiler,TreeTab,OutputTab,
                    ProjectTree,ErrorTree,OutlineTree,
                    DialogAndroid,DialogAbout,DialogAnt,DialogSquirrel,DialogTodo,
                    DialogBrowse)
from Widget.style import Styles
from stylesheet import *

from globals import (ospathsep,ospathjoin,ospathbasename,workDir,config,workSpace,
                     iconSize,iconDir,Icons)

class Window(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setStyleSheet(mainstyl)
        self.resize(1024,768)
        self.setWindowTitle("Sabel")
        self.setWindowIcon(Icons.sabel)
        self.centralwidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setMargin(0)
        self.styleIndex = config.styleIndex()
        self.cmdList = config.cmds()
        self.paramList = config.params()
        self.mode = config.mode()
        
        #TabWidgets
        #This parent is for findbar and vetical layount do not remove
        self.tab_1 = QWidget(self)
        self.tab_1.setMinimumWidth(800)
        self.tabWidget = EditorTab(self)
        self.VericalLayout = QVBoxLayout(self.tab_1)
        self.VericalLayout.setMargin(0)
        self.VericalLayout.addWidget(self.tabWidget)
        
        self.tabWidget_2 = TreeTab(self)
        #self.tabWidget_2.setMaximumWidth(200)
        self.tabWidget_3 = OutputTab(self)
        self.tabWidget_3.setMaximumHeight(200)#260
        self.tiler = Tiler(self)
        self.tiler.setMinimumHeight(100) 
        self.tabWidget.tabBar().setStyleSheet(stletabb)
        self.tabWidget.currentChanged.connect(self.fileChanged)
        self.tabWidget_2.currentChanged.connect(self.closeExplorer)
        self.tabWidget_3.currentChanged.connect(self.closeConsole)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabShape(0)
        #self.tiler.currentChanged.connect(self.closeDesigner)
        self.tiler.setTabsClosable(True)
        self.tiler.setTabShape(0)
         
        #Tree
        self.tab_5 = QWidget()
        #self.tab_5.setMaximumWidth(200)
        self.VerticalLayout_2 = QVBoxLayout(self.tab_5)#QHBoxLayout(self.tab_5)
        self.VerticalLayout_2.setMargin(0)
        self.treeWidget = ProjectTree(self.tab_5)
        #self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #self.treeWidget.horizontalScrollBar().show()
        self.VerticalLayout_2.addWidget(self.treeWidget)
        
        #Outline
        self.tab_2 = QWidget()
        #self.tab_2.setMaximumWidth(200)
        self.VerticalLayout_3 = QVBoxLayout(self.tab_2)
        self.VerticalLayout_3.setMargin(0)
        self.outlineWidget = OutlineTree(self.tab_2)
        self.VerticalLayout_3.addWidget(self.outlineWidget)
        
        #Output
        #must check
        self.tab_6 = QWidget()
        self.horizontalLayout_2 = QVBoxLayout(self.tab_6)
        self.horizontalLayout_2.setMargin(0)
        self.textEdit = QTextEdit()
        self.inputLayout = QHBoxLayout()
        self.inputLayout.setMargin(0)
        self.fileButton = QPushButton()
        self.fileButton.setText("File")
        self.fileButton.clicked.connect(self.getFile)
        self.runButton = QPushButton()
        self.runButton.setFlat(True)
        self.runButton.setIcon(Icons.go)
        self.combo = QComboBox()
        self.combo.setFixedWidth(100)
        self.comboAdd = QPushButton()
        self.comboAdd.setIcon(Icons.add)
        self.comboAdd.setFlat(True)
        self.comboAdd.clicked.connect(self.addCmd)
        self.comboDel = QPushButton()
        self.comboDel.setIcon(Icons.close_view)
        self.comboDel.setFlat(True)
        self.comboDel.clicked.connect(self.delCmd)
        self.combo2 = QComboBox()
        self.combo2.setFixedWidth(500)
        self.combo2Add = QPushButton()
        self.combo2Add.setIcon(Icons.add)
        self.combo2Add.setFlat(True)
        self.combo2Add.clicked.connect(self.addParam)
        self.combo2Del = QPushButton()
        self.combo2Del.setIcon(Icons.close_view)
        self.combo2Del.setFlat(True)
        self.combo2Del.clicked.connect(self.delParam)
        if(self.checkHasValue(self.cmdList)):
            for cmd in self.cmdList:
                self.combo.addItem(cmd)
        else:
            self.cmdList = []
        if(self.checkHasValue(self.paramList)):
            for param in self.paramList:
                self.combo2.addItem(param)
        else:
            self.paramList = []
        
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.inputLayout.addWidget(QLabel("<b>Command:</b>"))
        self.inputLayout.addWidget(self.combo)
        self.inputLayout.addWidget(self.comboAdd)
        self.inputLayout.addWidget(self.comboDel)
        self.inputLayout.addWidget(QLabel("<b>Parameters:</b>"))
        self.inputLayout.addWidget(self.combo2)
        self.inputLayout.addWidget(self.combo2Add)
        self.inputLayout.addWidget(self.combo2Del)
        self.inputLayout.addWidget(self.fileButton)
        self.inputLayout.addWidget(self.runButton)
        self.horizontalLayout_2.addLayout(self.inputLayout)
        
        #Error
        self.tab_7 = QWidget()
        self.horizontalLayout_4 = QHBoxLayout(self.tab_7)
        self.horizontalLayout_4.setMargin(0)
        self.errorTree = ErrorTree(self.tab_7)
        self.horizontalLayout_4.addWidget(self.errorTree)
        
        #Tiler
        #self.tab_11 = QWidget()
        #self.horizontalLayout_11 = QHBoxLayout(self.tab_11)
        #self.horizontalLayout_11.setMargin(0)
        #self.horizontalLayout_11.addWidget(self.tiler)
        
        #Find
        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_8)
        self.lineEdit = QLineEdit(self.tab_8)
        self.lineEdit_2 = QLineEdit(self.tab_8)
        self.findClose = QPushButton(self.tab_8)
        self.findClose.setIcon(Icons.close_view)
        self.findClose.setFlat(True)
        self.findClose.clicked.connect(self.findBarShow)
        self.find = QPushButton(self.tab_8)
        self.find.setText("Find")
        self.find.clicked.connect(self.findCurrentText)
        self.replacefind = QPushButton(self.tab_8)
        self.replacefind.setText("Replace/Find")
        self.replacefind.clicked.connect(self.replaceFindText)
        self.replace = QPushButton(self.tab_8)
        self.replace.setText("Replace")
        self.replace.clicked.connect(self.replaceCurrentText)
        self.replaceAll = QPushButton(self.tab_8)
        self.replaceAll.setText("Replace All")
        self.replaceAll.clicked.connect(self.replaceAllText)
        self.caseSensitive = QToolButton(self.tab_8)
        self.caseSensitive.setIcon(Icons.font)
        self.caseSensitive.setCheckable(True)
        self.wholeWord = QToolButton(self.tab_8)
        self.wholeWord.setText("ww")
        self.wholeWord.setCheckable(True)
        self.regex = QToolButton(self.tab_8)
        self.regex.setText("re")
        self.regex.setCheckable(True)
        self.backward = QToolButton(self.tab_8)
        self.backward.setText("bk")
        self.backward.setCheckable(True)
        self.backward.setDisabled(True)
        self.horizontalLayout_5.addWidget(self.findClose)
        self.horizontalLayout_5.addWidget(self.find)
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.horizontalLayout_5.addWidget(self.lineEdit_2)
        self.horizontalLayout_5.addWidget(self.caseSensitive)
        self.horizontalLayout_5.addWidget(self.wholeWord)
        self.horizontalLayout_5.addWidget(self.regex)
        self.horizontalLayout_5.addWidget(self.backward)
        self.horizontalLayout_5.addWidget(self.replacefind)
        self.horizontalLayout_5.addWidget(self.replace)
        self.horizontalLayout_5.addWidget(self.replaceAll)
        self.horizontalLayout_5.setMargin(0)
        self.tab_8.setMaximumHeight(25)
        self.VericalLayout.addWidget(self.tab_8)
        self.tab_8.hide()
        
        #Tabwidgets
        self.tabWidget_2.addTab(self.tab_5,"Projects")
        self.tabWidget_2.addTab(self.tab_2,"Outline")
        self.tabWidget_2.addTab(QWidget(self),"")
        self.tabWidget_2.setTabIcon(2,Icons.close_view)
        self.tabWidget_3.addTab(self.tab_7,"Error")
        self.tabWidget_3.addTab(self.tab_6,"Output")
        self.tabWidget_3.addTab(QWidget(self),"")
        self.tabWidget_3.setTabIcon(0,Icons.error)
        self.tabWidget_3.setTabIcon(1,Icons.console_view)
        self.tabWidget_3.setTabIcon(2,Icons.close_view)
        
        #Splitters
        self.split1 = QSplitter(Qt.Horizontal)
        self.split1.addWidget(self.tabWidget_2)
        self.split1.addWidget(self.tab_1)
        #self.split1.addWidget(self.tab_5)
        
        self.split2 = QSplitter(Qt.Vertical)
        self.split2.addWidget(self.split1)
        self.split2.addWidget(self.tiler)
        self.tiler.hide()
        self.split2.addWidget(self.tabWidget_3)
        self.tabWidget_3.hide()
        self.horizontalLayout.addWidget(self.split2)
        
        
        #Status
        self.statusbar = QStatusBar(self)
        self.aboutButton = QPushButton(self)
        self.aboutButton.setFlat(True)
        self.aboutButton.setIcon(Icons.anchor)
        self.aboutButton.clicked.connect(self.about)
        self.expButton = QPushButton(self)
        self.expButton.setFlat(True)
        self.expButton.setIcon(Icons.prj)
        self.expButton.clicked.connect(self.exp)
        self.cmdButton = QPushButton(self)
        self.cmdButton.setFlat(True)
        self.cmdButton.setIcon(Icons.console_view)
        self.cmdButton.clicked.connect(self.cmd)
        self.cmdButton.setShortcut('Ctrl+D')
        self.imgButton = QPushButton(self)
        self.imgButton.setFlat(True)
        self.imgButton.setIcon(Icons.color_palette)
        self.imgButton.clicked.connect(self.design)
        self.imgButton.setShortcut('Ctrl+I')
        self.findButton = QPushButton(self)
        self.findButton.setFlat(True)
        self.findButton.setIcon(Icons.find)
        self.findButton.setShortcut("Ctrl+F")
        self.findButton.clicked.connect(self.findBarShow)
        self.zoominButton = QPushButton(self)
        self.zoominButton.setFlat(True)
        self.zoominButton.setIcon(Icons.zoomplus)
        self.zoominButton.clicked.connect(self.zoomin)
        self.zoomoutButton = QPushButton(self)
        self.zoomoutButton.setFlat(True)
        self.zoomoutButton.setIcon(Icons.zoomminus)
        self.zoomoutButton.clicked.connect(self.zoomout)

        '''Status Text, Progress Bar and Stop Button'''
        self.statusText = QLabel("Writing")
        self.statusText.setMargin(10)
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.stopButton = QPushButton(self)
        self.stopButton.setFlat(True)
        self.stopButton.setIcon(Icons.stop)
        self.stopButton.clicked.connect(self.forceStop)
        self.progressbar.hide()
        self.stopButton.hide()
        self.temp = False
        self.progress = False
        self.counter = 0
        
        '''Adding all widgets to Status Bar'''
        self.statusbar.addWidget(self.aboutButton)
        self.statusbar.addWidget(self.expButton)
        self.statusbar.addWidget(self.cmdButton)
        self.statusbar.addWidget(self.imgButton)
        self.statusbar.addWidget(self.findButton)
        self.statusbar.addWidget(self.zoominButton)
        self.statusbar.addWidget(self.zoomoutButton)
        #self.statusbar.addWidget(self.fontButton)
        self.statusbar.addWidget(self.statusText)
        self.statusbar.addWidget(self.progressbar)
        self.statusbar.addWidget(self.stopButton)
        #self.statusbar.setFixedHeight(18)
        
        ''''Initializing Coloring Style'''
        self.colorStyle = None
        self.initColorStyle()
        
        '''Adding Cental Widget and Status Bar'''
        self.setCentralWidget(self.centralwidget)
        self.setStatusBar(self.statusbar)
        self.textEdit.setReadOnly(True)
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
    def build_project(self):
        current_file = self.files[self.tabWidget.currentIndex()]
        prj = self.treeWidget.getProject(current_file)
        if(prj != None):
            self.treeWidget.build(prj)
            
    def run_project(self):
        current_file = self.files[self.tabWidget.currentIndex()]
        prj = self.treeWidget.getProject(current_file)
        if(prj != None):
            self.treeWidget.run(prj)
            
    def forceStop(self):
        self.ant.kill()
        self.progressStop()
        
#-----------------------------------------------------------------------------------#
#   Menu Actions Functions                                                          #
#-----------------------------------------------------------------------------------#
    def run(self):
        if(self.mode == 0):
            self.sq.run()
        elif(self.mode == 1):
            self.adb.run()
        elif(self.mode == 2):
            self.ios.run()
        elif(self.mode == 3):
            self.c.run()
        elif(self.mode == 4):
            self.cpp.run()
            
    def emo(self):
        if(self.mode == 0):
            self.mode = 1
            self.toolBar.action_Squirrel.setChecked(False)
        else:
            self.toolBar.action_Squirrel.setChecked(True)
            
    def ios(self):
        print "ios"
        
    
    def sq(self):
        if(self.mode == 1):
            self.mode = 0
            self.toolBar.action_Emo.setChecked(False)
        else:
            self.toolBar.action_Emo.setChecked(True)
     
    def about(self):
        form = DialogAbout(self)
        
    def todo(self):
        form = DialogTodo(self)
        form.show()

    def help(self):
        QMessageBox.about(self,"Help","This is about all The Help that i can Give you now")
        
    def full(self):
        if not self.isFull:
            self.setWindowState(Qt.WindowFullScreen)
            self.isFull = True
        else:
            self.setWindowState(Qt.WindowMaximized)
            self.isFull = False
            
    def android(self):
        form = DialogAndroid(self)
        form.show()
    
    def antt(self):
        form = DialogAnt(self)
        form.show()
        
    def squirrel(self):
        form = DialogSquirrel(self)
        form.show()
        
    def findBarShow(self):
        if(self.tab_8.isHidden()):
            self.tab_8.show()
        else:
            self.tab_8.hide()
            
    def exp(self):
        if(self.tabWidget_2.isHidden()):
            self.tabWidget_2.show()
        else:
            self.tabWidget_2.hide()
    
    def cmd(self):
        if(self.tabWidget_3.isHidden()):
            self.tabWidget_3.show()
        else:
            self.tabWidget_3.hide()
            
    def design(self):
        if(self.tiler.isHidden()):
            self.tiler.show()
        else:
            self.tiler.hide()
            
    def closeDesigner(self,no):
        pass
        '''
        if(no == self.tiler.closeIndex()):
            if(self.tiler.isHidden()):
                self.tiler.show()
            else:
                self.tiler.setCurrentIndex(1)
                self.tiler.hide()
        '''
     
    '''The current Changed idx of tabwidget_3 is passed to this a param'''   
    def closeConsole(self,no = 2):
        if(no == 2):
            if(self.tabWidget_3.isHidden()):
                self.tabWidget_3.show()
            else:
                self.tabWidget_3.setCurrentIndex(1)
                self.tabWidget_3.hide()
                
    '''The current Changed idx of tabwidget_2 is passed to this a param'''
    def closeExplorer(self,no = 2):
        if(no == 2):
            if(self.tabWidget_2.isHidden()):
                self.tabWidget_2.show()
            else:
                self.tabWidget_2.setCurrentIndex(0)
                self.tabWidget_2.hide()
        elif(no == 1):
            self.fileChanged(no)
                
    def fileChanged(self,no):
        if(self.tabWidget_2.currentIndex() == 1):
            edt = self.tabWidget.widget(self.tabWidget.currentIndex())
            source = edt.text()
            self.outlineWidget.parseText(source)
           
    def statusSaving(self):
        self.statusText.setText("Saving")   
    def statusParsing(self):
        self.statusText.setText("Parsing")   
    def statusWriting(self):
        self.statusText.setText("Writing")  
    def statusRunning(self):
        self.statusText.setText("Running")   
    def statusStopping(self):
        self.statusText.setText("Stopping")
    def statusCommand(self):
        self.statusText.setText("Command")
    def statusBuilding(self):
        self.statusText.setText("Building")
    def statusInstalling(self):
        self.statusText.setText("Installing")
    def statusCleaning(self):
        self.statusText.setText("Cleaning")
    def statusCreating(self):
        self.statusText.setText("Creating")
                
    def progressStart(self):
        self.progress == True
        self.temp == True
        if(self.progressbar.isHidden()):
            self.progressbar.show()
        if(self.stopButton.isHidden()):
            self.stopButton.show()
        self.progressbar.setValue(1)
        
    def progressStop(self):
        self.progress == False
        self.temp == False
        self.progressbar.setValue(100)
        if not(self.progressbar.isHidden()):
            self.progressbar.hide()
        if not(self.stopButton.isHidden()):
            self.stopButton.hide()
              
    def progressUpdate(self):
        if(self.progress == True):
            if(self.temp == True):
                self.counter += 1
                self.progressbar.setValue(self.counter)
                if(self.counter == 100):
                    self.temp = False
            if(self.temp == False):
                self.counter -= 1
                self.progressbar.setValue(self.counter)
                if(self.counter == 0):
                    self.temp = True
            
                
#-----------------------------------------------------------------------------------#
#   Editor Functions                                                                #
#-----------------------------------------------------------------------------------#   
    '''Search and Replace Functions'''  
    def findCurrentText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())
    def replaceCurrentText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.replaceText(self.lineEdit_2.text()) 
    def replaceFindText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.replaceText(self.lineEdit_2.text())
        self.findCurrentText()      
    def replaceAllText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        while(edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())):
            edt.replaceText(self.lineEdit_2.text())      
    def errorLine(self,error):
        index = self.tabWidget.currentIndex()
        edt = self.tabWidget.widget(index)
        edt.setLine(error.line)
    '''Font Functions'''       
    def zoomin(self):
        pass
        #for i in range(len(self.files)):
        #    self.tabWidget.widget(i).zoomin()
    def zoomout(self):
        pass
        #for i in range(len(self.files)):
        #    self.tabWidget.widget(i).zoomout()
            
    def setFontName(self,idx):
        fontName = str(self.toolBar.fontCombo.itemText(idx))
        config.setFontName(fontName)
        for i in range(len(self.files)):
            self.tabWidget.widget(i).setFontName()
            
    def setFontSize(self,idx):
        fontSize = idx+1
        config.setFontSize(fontSize)
        for i in range(len(self.files)):
            self.tabWidget.widget(i).setFontSize() 
            
    def gotoLine(self,item):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.setLine(item.line)
            
    def setMargin(self):
        mar = config.margin()
        if(mar == 0): 
            config.setMargin(1)
            for i in range(len(self.files)):
                self.tabWidget.widget(i).setMargin(1)
        else:
            config.setMargin(0)
            for i in range(len(self.files)):
                self.tabWidget.widget(i).setMargin(0)
                
    def setIndent(self):
        indent = config.indent()
        if(indent == 0): 
            config.setIndent(1)
            for i in range(len(self.files)):
                self.tabWidget.widget(i).setIndent(1)
        else:
            config.setIndent(0)
            for i in range(len(self.files)):
                self.tabWidget.widget(i).setIndent(0)
        
        
    def setThreshold(self,val):
        config.setThresh(val)
        for i in range(len(self.files)):
            #print i
            self.tabWidget.widget(i).setThreshold(val)
    def setTabWidth(self,val):
        config.setTabWidth(val)
        for i in range(len(self.files)):
            #print i
            self.tabWidget.widget(i).setTabWidth(val)
    '''style Functions'''   
    def initColorStyle(self):
        self.colorStyle = Styles[self.styleIndex]                
        pal = QPalette(self.tabWidget_2.palette())
        #print pal.color(QPalette.Base).name()
        #print pal.color(QPalette.Window).name()
        pal.setColor(QPalette.Base,self.colorStyle.paper)
        pal.setColor(QPalette.Text,self.colorStyle.color)
        self.tabWidget_2.setPalette(pal)
        self.tabWidget_3.setPalette(pal)      
    def style_clicked(self,no):
        self.styleIndex = no -1
        #print self.styleIndex
        for i in self.styleslist:
            if self.styleslist.index(i) == self.styleIndex:
                i.setChecked(True)
            else:
                i.setChecked(False)
        config.setstyleIndex(self.styleIndex)
        #self.initColorStyle()
        for i in range(len(self.files)):
            pass
            #self.tabWidget.
            #self.tabWidget.widget(i).setColorStyle(self.colorStyle)
            
#-----------------------------------------------------------------------------------#
#   Command Functions                                                               #
#-----------------------------------------------------------------------------------#   
    def getFile(self):
        self.browsedialog = DialogBrowse(self)
        self.browsedialog.tree.itemDoubleClicked.connect(self.getName)
        self.browsedialog.show()
            
    def getName(self,item):
        if(item.isFile()):
                self.browsedialog.accept()
                fname = item.getPath()
                if not (fname == ""):
                    index = self.combo2.currentIndex()
                    text = str(self.combo2.itemText(index))+" "+fname
                    self.combo2.setItemText(index,text)
                    self.paramList.pop(index)
                    self.paramList.insert(index,text)
                    config.setParam(self.paramList)
                 
    def addCmd(self,index):
        text, ok = QInputDialog.getText(self, 'Add Command', 'Command:')
        if(ok):
            if(str(text) != ''):
                cmd = str(text).upper()
                self.cmdList.append(cmd)
                #print self.cmdList
                self.combo.addItem(cmd)
                config.setCmd(self.cmdList)
                config.setParam(self.paramList)
                
    def delCmd(self):
        index = self.combo.currentIndex()
        self.combo.removeItem(index)
        self.cmdList.pop(index)
        #print self.cmdList
        config.setCmd(self.cmdList)
        
    def addParam(self,index):
        text, ok = QInputDialog.getText(self, 'Add Parameters', 'Params:')
        if(ok):
            if(str(text) != ''):
                param = str(text)
                self.paramList.append(param)
                self.combo2.addItem(param)
                config.setParam(self.paramList)
                
    def delParam(self):
        index = self.combo2.currentIndex()
        self.combo2.removeItem(index)
        self.paramList.pop(index)
        config.setParam(self.paramList)
        
    def checkHasValue(self,list):
        if(list != None and len(list) != 0):
            return True
        else:
            return False