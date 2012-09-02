from PyQt4.QtGui import (QAction,QIcon,QMessageBox,QWidgetAction,QMenu,QWidget,
                         QHBoxLayout,QVBoxLayout,QTabWidget,QToolBar,QTextEdit,
                         QLineEdit,QPushButton,QToolButton,QSplitter,QStatusBar,
                         QMainWindow,QPalette,QColor,QSlider,QFontDialog,QLabel,
                         QFont,QComboBox,QFileDialog,QInputDialog)      
from PyQt4.QtCore import QSize,Qt,QStringList
from Widget import (Tab,ProjectTree,ErrorTree,OutlineTree,DialogAndroid,DialogAbout,
                    DialogAnt,DialogSquirrel,DialogTodo)
from Widget.style import Styles
from stylesheet import *

from globals import (ospathsep,ospathjoin,ospathbasename,workDir,config,workSpace,
                     iconSize,iconDir,adblist,Icons,os_icon,
                     fontName,fontSize,cmds)

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
        self.cmdList =cmds
        self.mode = config.mode()
        
        #TabWidgets
        self.tab_1 = QWidget(self)
        self.tab_1.setMinimumWidth(800)
        self.tabWidget = Tab(self.tab_1)
        self.VericalLayout = QVBoxLayout(self.tab_1)
        self.VericalLayout.setMargin(0)
        self.VericalLayout.addWidget(self.tabWidget)
        
        self.tabWidget_2 = QTabWidget(self)
        #self.tabWidget_2.setMaximumWidth(200)
        self.tabWidget_3 = QTabWidget(self)
        self.tabWidget_3.setMaximumHeight(200)#260
        
        
        self.tabWidget.tabBar().setStyleSheet(stletabb)
         
        #Tree
        self.tab_5 = QWidget()
        #self.tab_5.setMaximumWidth(200)
        self.VerticalLayout_2 = QVBoxLayout(self.tab_5)#QHBoxLayout(self.tab_5)
        self.VerticalLayout_2.setMargin(0)
        self.treeWidget = ProjectTree(self.tab_5)
        self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.treeWidget.horizontalScrollBar().show()
        self.treebar = QToolBar()
        action_Folder = QAction(Icons.newfolder,'New Folder', self)
        action_Folder.triggered.connect(self.about)
        action_Android = QAction(Icons.android,'Android', self)
        action_Android.triggered.connect(self.android)
        action_Ant = QAction(Icons.ant_view,'Ant', self)
        action_Ant.triggered.connect(self.ant)
        action_Squirrel = QAction(Icons.nut,'Squirrel', self)
        action_Squirrel.triggered.connect(self.squirrel)
        self.treebar.addAction(action_Folder)
        self.treebar.addAction(action_Android)
        self.treebar.addAction(action_Ant)
        self.treebar.addAction(action_Squirrel)
        self.treebar.setIconSize(QSize(16,16))
        self.VerticalLayout_2.addWidget(self.treebar)
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
        self.runEdit = QLineEdit()
        self.fileButton = QPushButton()
        self.fileButton.setText("File")
        self.fileButton.clicked.connect(self.getFile)
        self.runButton = QPushButton()
        self.runButton.setFlat(True)
        self.runButton.setIcon(Icons.go)
        self.combo = QComboBox()
        self.comboAdd = QPushButton()
        self.comboAdd.setIcon(Icons.add)
        self.comboAdd.setFlat(True)
        self.comboAdd.clicked.connect(self.addCmd)
        self.comboDel = QPushButton()
        self.comboDel.setIcon(Icons.close_view)
        self.comboDel.setFlat(True)
        #self.comboDel.clicked.connect(self.delCmd)
        for text in self.cmdList:
            self.combo.addItem(text)
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.inputLayout.addWidget(QLabel("Input:"))
        self.inputLayout.addWidget(self.combo)
        self.inputLayout.addWidget(self.comboAdd)
        self.inputLayout.addWidget(self.comboDel)
        self.inputLayout.addWidget(self.runEdit)
        self.inputLayout.addWidget(self.fileButton)
        self.inputLayout.addWidget(self.runButton)
        self.horizontalLayout_2.addLayout(self.inputLayout)
        
        #Error
        self.tab_7 = QWidget()
        self.horizontalLayout_4 = QHBoxLayout(self.tab_7)
        self.horizontalLayout_4.setMargin(0)
        self.errorTree = ErrorTree(self.tab_7)
        self.horizontalLayout_4.addWidget(self.errorTree)
        
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
        
        
        
        #Tab Widget Init
        self.tabWidget_2.addTab(self.tab_5,"Projects")
        self.tabWidget_2.addTab(self.tab_2,"Outline")
        self.tabWidget_2.addTab(QWidget(self),"")
        self.tabWidget_2.setTabIcon(2,Icons.close_view)
        self.tabWidget_2.currentChanged.connect(self.closeExplorer)
        
        self.tabWidget_3.addTab(self.tab_7,"Error")
        self.tabWidget_3.addTab(self.tab_6,"Output")
        self.tabWidget_3.addTab(QWidget(self),"")
        self.tabWidget_3.setTabIcon(0,Icons.error)
        self.tabWidget_3.setTabIcon(1,Icons.console_view)
        self.tabWidget_3.setTabIcon(2,Icons.close_view)
        self.tabWidget_3.currentChanged.connect(self.closeConsole)
        
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabShape(0)
        
        
        #Splitters
        self.split1 = QSplitter(Qt.Horizontal)
        self.split1.addWidget(self.tabWidget_2)
        self.split1.addWidget(self.tab_1)
        #self.split1.addWidget(self.tab_5)
        
        self.split2 = QSplitter(Qt.Vertical)
        self.split2.addWidget(self.split1)
        self.split2.addWidget(self.tabWidget_3)
        self.tabWidget_3.hide()
        self.horizontalLayout.addWidget(self.split2)
        
        
        #Status
        self.statusbar = QStatusBar(self)
        self.aboutButton = QPushButton(self)
        self.aboutButton.setFlat(True)
        self.aboutButton.setIcon(Icons.anchor)
        self.aboutButton.clicked.connect(self.about)
        self.cmdButton = QPushButton(self)
        self.cmdButton.setFlat(True)
        self.cmdButton.setIcon(Icons.console_view)
        self.cmdButton.clicked.connect(self.cmd)
        self.cmdButton.setShortcut('Ctrl+D')
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
        self.fontButton = QPushButton(self)
        self.fontButton.setFlat(True)
        self.fontButton.setIcon(Icons.font)
        self.fontButton.clicked.connect(self.setFont)
        self.statusbar.addWidget(self.aboutButton)
        self.statusbar.addWidget(self.cmdButton)
        self.statusbar.addWidget(self.findButton)
        self.statusbar.addWidget(self.zoominButton)
        self.statusbar.addWidget(self.zoomoutButton)
        self.statusbar.addWidget(self.fontButton)
        #self.statusbar.setFixedHeight(18)
        
        #Init colorstyling
        self.colorStyle = None
        self.initColorStyle()
        #Init
        self.setCentralWidget(self.centralwidget)
        self.setStatusBar(self.statusbar)
        self.textEdit.setReadOnly(True)
        self.fontName = fontName
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
    def initToolBar(self):
        self.action_NewProject = QAction(Icons.newprj, 'Project', self)
        self.action_NewProject.triggered.connect(self.newProject)
        self.action_NewProject.setToolTip("Create a New Project")

        self.action_Open = QAction(Icons.open, 'Open', self)
        self.action_Open.setShortcut('Ctrl+O')
        self.action_Open.triggered.connect(self.fileOpen)
        self.action_Open.setToolTip("Open File")

        self.action_Save = QAction(Icons.save, 'Save', self)
        self.action_Save.setShortcut('Ctrl+S')
        self.action_Save.triggered.connect(self.fileSave)
        self.action_Save.setToolTip("Save Current File")

        self.action_SaveAll = QAction(Icons.saveall, 'SaveAll', self)
        self.action_SaveAll.setShortcut('Ctrl+A')
        self.action_SaveAll.triggered.connect(self.fileSaveAll)
        self.action_SaveAll.setToolTip("Save All Files")
        
        self.action_Help = QAction(Icons.toc_open, 'Help', self)
        self.action_Help.triggered.connect(self.help)
        self.action_Run = QAction(Icons.run, 'Run', self)
        self.action_Run.setShortcut('Ctrl+R')
        self.action_Run.triggered.connect(self.adb.run)
        self.action_RunFile = QAction(Icons.go, 'Cmd', self)
        self.action_RunFile.triggered.connect(self.command.setCmd)
        self.runEdit.returnPressed.connect(self.command.setCmdLine)
        self.runButton.clicked.connect(self.command.setCmdLine)
        self.action_Stop = QAction(Icons.stop, 'Stop', self)
        self.action_Stop.setShortcut('Ctrl+Q')
        self.action_Stop.triggered.connect(self.adb.stop)
        self.action_Design = QAction(Icons.color_palette, 'Design', self)
        self.action_Todo = QAction(Icons.task_set, 'Todo', self)
        self.action_Todo.triggered.connect(self.todo)
        
        men = QMenu()
        #Threshold Slider
        self.threshSlider = QSlider()
        self.threshSlider.setTickPosition(QSlider.TicksLeft)
        self.threshSlider.setOrientation(Qt.Horizontal)
        self.threshSlider.setValue(config.thresh())
        self.threshSlider.setMinimum(0)
        self.threshSlider.setMaximum(5)
        self.threshSlider.valueChanged.connect(self.setThreshold)
        #self.threshSlider.setInvertedAppearance(True)
        self.threshSliderAction = QWidgetAction(men)
        self.threshSliderAction.setDefaultWidget(self.threshSlider)
        
        #TabsWidth Slider
        self.tabsSlider = QSlider()
        self.tabsSlider.setTickPosition(QSlider.TicksLeft)
        self.tabsSlider.setOrientation(Qt.Horizontal)
        self.tabsSlider.setValue(config.tabwidth())
        self.tabsSlider.setMinimum(0)
        self.tabsSlider.setMaximum(8)
        self.tabsSlider.valueChanged.connect(self.setTabWidth)
        self.tabsSliderAction = QWidgetAction(men)
        self.tabsSliderAction.setDefaultWidget(self.tabsSlider)
        
        
        action_explorer = QAction("Show Explorer",self)
        action_explorer.triggered.connect(lambda x=2:self.closeExplorer(2))
        men.addAction(action_explorer)
        action_console = QAction("Show Console",self)
        action_console.triggered.connect(lambda x=2:self.closeConsole(2))
        men.addAction(action_console)
        men.addAction(QAction("Idents",self))
        men.addSeparator()
        men.addAction(QAction("TabWidth",self))
        men.addAction(self.tabsSliderAction)
        men.addSeparator()
        men.addAction(QAction("Threshold",self))
        men.addAction(self.threshSliderAction)
        
        self.action_Options = QAction(Icons.cmpC_pal, 'Options', self)
        self.action_Options.setMenu(men)
        self.action_Options.triggered.connect(self.options)
        
        
        self.action_Full = QAction(Icons.fullscreen, 'Full', self)
        self.action_Full.setShortcut('Shift+Enter')
        self.action_Full.triggered.connect(self.full)
        
        self.action_Squirrel = QAction(Icons.nut, 'Squirrel', self)
        self.action_Squirrel.setCheckable(True)
        self.action_Squirrel.triggered.connect(self.sq)
        self.action_Emo = QAction(Icons.emo, 'Emo', self)
        self.action_Emo.setCheckable(True)
        self.action_Emo.triggered.connect(self.emo)
        self.action_Ios = QAction(Icons.ios, '', self)
        self.action_Ios.setCheckable(True)
        self.action_Ios.triggered.connect(self.ios)

        
        self.action_Style = QAction(Icons.style, 'Style', self)
        men1 = QMenu()
        self.styleslist = []
        self.style1 = QAction("All Hallow's Eve",self)
        self.style1.triggered.connect(lambda:self.style_clicked(1))
        self.style1.setCheckable(True)
        self.style2 = QAction("Amy",self)
        self.style2.triggered.connect(lambda:self.style_clicked(2))
        self.style2.setCheckable(True)
        self.style3 = QAction("Aptana Studio",self)
        self.style3.triggered.connect(lambda:self.style_clicked(3))
        self.style3.setCheckable(True)
        self.style4 = QAction("Bespin",self)
        self.style4.triggered.connect(lambda:self.style_clicked(4))
        self.style4.setCheckable(True)
        self.style5 = QAction("Blackboard",self)
        self.style5.triggered.connect(lambda:self.style_clicked(5))
        self.style5.setCheckable(True)
        self.style6 = QAction("Choco",self)
        self.style6.triggered.connect(lambda:self.style_clicked(6))
        self.style6.setCheckable(True)
        self.style7 = QAction("Cobalt",self)
        self.style7.triggered.connect(lambda:self.style_clicked(7))
        self.style7.setCheckable(True)
        self.style8 = QAction("Dawn",self)
        self.style8.triggered.connect(lambda:self.style_clicked(8))
        self.style8.setCheckable(True)
        self.style9 = QAction("Eclipse",self)
        self.style9.triggered.connect(lambda:self.style_clicked(9))
        self.style9.setCheckable(True)
        self.styleslist.append(self.style1)
        self.styleslist.append(self.style2)
        self.styleslist.append(self.style3)
        self.styleslist.append(self.style4)
        self.styleslist.append(self.style5)
        self.styleslist.append(self.style6)
        self.styleslist.append(self.style7)
        self.styleslist.append(self.style8)
        self.styleslist.append(self.style9)
        men1.addActions(self.styleslist)
        self.action_Style.setMenu(men1)
        self.styleslist[self.styleIndex].setChecked(True)


        self.action_Stop.setDisabled(True)
        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.setIconSize(QSize(16,16))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.setAllowedAreas(Qt.AllToolBarAreas)
        #self.toolbar.setFixedHeight(40)

        self.toolbar.addAction(self.action_NewProject)
        self.toolbar.addAction(self.action_Open)
        self.toolbar.addAction(self.action_Save)
        self.toolbar.addAction(self.action_SaveAll)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Run)
        self.toolbar.addAction(self.action_RunFile)
        self.toolbar.addAction(self.action_Stop)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Design)
        self.toolbar.addAction(self.action_Todo)
        self.toolbar.addAction(self.action_Options)
        self.toolbar.addAction(self.action_Style)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Help)
        self.toolbar.addAction(self.action_Full)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_Squirrel)
        self.toolbar.addAction(self.action_Emo)
        self.toolbar.addAction(self.action_Ios)
        if(self.mode == 0):
            self.action_Squirrel.setChecked(True)
        else:
            self.action_Emo.setChecked(True)
            
   
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
            self.action_Squirrel.setChecked(False)
        else:
            self.action_Squirrel.setChecked(True)
            
    def ios(self):
        print "Nonr"
        
    
    def sq(self):
        if(self.mode == 1):
            self.mode = 0
            self.action_Emo.setChecked(False)
        else:
            self.action_Emo.setChecked(True)
     
    def about(self):
        form = DialogAbout(self)
        
    def todo(self):
        form = DialogTodo(self)
        form.show()

    def help(self):
        QMessageBox.about(self, "About Simple Editor","This is The Help")
        
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
    
    def ant(self):
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
    
    def cmd(self):
        if(self.tabWidget_3.isHidden()):
            self.tabWidget_3.show()
        else:
            self.tabWidget_3.hide()
            
    def closeConsole(self,no = 2):
        if(no == 2):
            if(self.tabWidget_3.isHidden()):
                self.tabWidget_3.show()
            else:
                self.tabWidget_3.setCurrentIndex(1)
                self.tabWidget_3.hide()
    def closeExplorer(self,no = 2):
        if(no == 2):
            if(self.tabWidget_2.isHidden()):
                self.tabWidget_2.show()
            else:
                self.tabWidget_2.setCurrentIndex(0)
                self.tabWidget_2.hide()
                
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
             
    '''Font Functions'''       
    def zoomin(self):
        for i in range(len(self.files)):
            self.tabWidget.widget(i).zoomin()
    def zoomout(self):
        for i in range(len(self.files)):
            self.tabWidget.widget(i).zoomout()       
    def setFont(self):
        font = QFont()
        font.setFamily(self.fontName)
        fdialog = QFontDialog(self)
        fdialog.show()
        fdialog.setCurrentFont(font)
        fdialog.accepted.connect(lambda:self.setFontName(fdialog.currentFont()))
    def setFontName(self,font):
        #print "accepted"
        #print font.family()
        self.fontName = str(font.family())
        config.setFontName(self.fontName)
        for i in range(len(self.files)):
            self.tabWidget.widget(i).setFontName(self.fontName)      
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
            
    '''Command Functions'''
    def getFile(self):
        fname = str(QFileDialog.getOpenFileName(self,"Open File", '.', "Files (*.*)"))
        if not (fname == ""):
            self.runEdit.setText(fname)
            
    def addCmd(self,index):
        text, ok = QInputDialog.getText(self, 'Add Command', 'Command:')
        if(ok):
            if(str(text) != ''):
                cmd = str(text).upper()
                self.cmdList.append(cmd)
                #print self.cmdList
                self.combo.addItem(cmd)
                config.setCmd(self.cmdList)
                
    def delCmd(self,index):
        pass
        