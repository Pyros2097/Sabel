from PyQt4.QtGui import (QAction,QIcon,QMessageBox,QWidgetAction,QMenu,QWidget,
                         QHBoxLayout,QVBoxLayout,QTabWidget,QToolBar,QTextEdit,
                         QLineEdit,QPushButton,QToolButton,QSplitter,QStatusBar,
                         QMainWindow,QPalette,QColor,QSlider,QFontDialog,QLabel,
                         QFont,QComboBox,QFileDialog,QInputDialog)              
from PyQt4.QtCore import QSize,Qt,QStringList
from Widget import (Tab,ProjectTree,ErrorTree,OutlineTree,DialogAndroid,DialogAbout,
                    DialogAnt,DialogSquirrel)
from Widget.style import Styles
from stylesheet import *

from globals import (ospathsep,ospathjoin,ospathbasename,workDir,config,workSpace,
                     iconSize,iconDir,styleIndex,adblist,Icons,os_icon,threshold,
                     fontName,fontSize,cmds)

class Window(QMainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setStyleSheet(mainstyl)
        self.resize(758, 673)
        self.setWindowTitle("Sabel")
        self.setWindowIcon(Icons.sabel)
        self.centralwidget = QWidget(self)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setMargin(0)
        self.styleIndex = styleIndex
        self.cmdList =cmds
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
        self.treebar.addAction(action_Folder)
        self.treebar.addAction(action_Android)
        self.treebar.addAction(action_Ant)
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
        self.combo.activated.connect(self.addCmd)
        for text in self.cmdList:
            self.combo.addItem(text)
        self.combo.setItemIcon(0,Icons.add)
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.inputLayout.addWidget(QLabel("Input:"))
        self.inputLayout.addWidget(self.combo)
        self.inputLayout.addWidget(self.runEdit)
        self.inputLayout.addWidget(self.fileButton)
        self.inputLayout.addWidget(self.runButton)
        self.horizontalLayout_2.addLayout(self.inputLayout)
        
        #Error
        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_7)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.errorTree = ErrorTree(self.tab_7)
        self.errorTree.setObjectName("textEdit_2")
        self.horizontalLayout_4.addWidget(self.errorTree)
        
        #Find
        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit = QLineEdit(self.tab_8)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QLineEdit(self.tab_8)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.findClose = QPushButton(self.tab_8)
        self.findClose.setIcon(Icons.close_view)
        self.findClose.setFlat(True)
        self.findClose.clicked.connect(self.findBarShow)
        self.find = QPushButton(self.tab_8)
        self.find.setText("Find")
        self.find.clicked.connect(self.findCurrentText)
        self.replacefind = QPushButton(self.tab_8)
        self.replacefind.setText("Replace/Find")
        self.replace = QPushButton(self.tab_8)
        self.replace.setText("Replace")
        self.replace.clicked.connect(self.replaceCurrentText)
        self.replaceAll = QPushButton(self.tab_8)
        self.replaceAll.setText("Replace All")
        self.replaceAll.clicked.connect(self.replaceAllText)
        self.caseSensitive = QToolButton(self.tab_8)
        self.caseSensitive.setText("cs")
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
        self.statusbar.setObjectName("statusbar")
        self.aboutButton = QPushButton(self)
        self.aboutButton.setFlat(True)
        self.aboutButton.setIcon(Icons.anchor)
        self.aboutButton.clicked.connect(self.about)
        self.cmdButton = QPushButton(self)
        self.cmdButton.setFlat(True)
        self.cmdButton.setIcon(Icons.console_view)
        self.cmdButton.clicked.connect(self.cmd)
        self.cmdButton.setShortcut('Ctrl+O')
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
        
    def findBarShow(self):
        if(self.tab_8.isHidden()):
            self.tab_8.show()
        else:
            self.tab_8.hide()

    def initToolBar(self):
        self.action_NewProject = QAction(Icons.newprj, 'Project', self)
        self.action_NewProject.setShortcut('Ctrl+P')
        self.action_NewProject.triggered.connect(self.newProject)
        self.action_NewProject.setToolTip("Create a New Project")
        self.action_NewProject.setStatusTip("Create a New Project")

        self.action_Open = QAction(Icons.open, 'Open', self)
        self.action_Open.setShortcut('Ctrl+O')
        self.action_Open.triggered.connect(self.fileOpen)
        self.action_Open.setToolTip("Open File")
        self.action_Open.setStatusTip("Open File")

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
        #self.action_Todo.triggered.connect(self.stop)
        #Only variation CHeck Later
        men = QMenu()
        self.threshSlider = QSlider()
        self.threshSlider.setStyleSheet(slisty)
        self.threshSlider.setTickPosition(QSlider.TicksLeft)
        self.threshSlider.setOrientation(Qt.Horizontal)
        self.threshSlider.setValue(threshold)
        self.threshSlider.setMinimum(0)
        self.threshSlider.setMaximum(5)
        self.threshSlider.valueChanged.connect(self.setThreshold)
        #self.threshSlider.setInvertedAppearance(True)
        self.threshSliderAction = QWidgetAction(men)
        self.threshSliderAction.setDefaultWidget(self.threshSlider)
        
        men.addAction(QAction("Ident",self))
        men.addAction(QAction("Edit",self))
        men.addAction(QAction("Paste",self))
        men.addAction(QAction("Tabs",self))
        men.addSeparator()
        men.addAction(QAction("Threshold",self))
        men.addAction(self.threshSliderAction)
        
        self.action_Options = QAction(Icons.cmpC_pal, 'Options', self)
        self.action_Options.setMenu(men)
        self.action_Options.triggered.connect(self.options)
        
        
        self.action_Full = QAction(Icons.fullscreen, 'Full', self)
        self.action_Full.setShortcut('Shift+Enter')
        self.action_Full.triggered.connect(self.full)

        
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
        
    def about(self):
        form = DialogAbout(self)
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
        pass
            
    def cmd(self):
        if(self.tabWidget_3.isHidden()):
            self.tabWidget_3.show()
        else:
            self.tabWidget_3.hide()
            
    def closeConsole(self,no):
        if(no == 2):
            if(self.tabWidget_3.isHidden()):
                self.tabWidget_3.show()
                #self.tabWidget_3.setCurrentIndex(1)
            else:
                self.tabWidget_3.hide()
            
            
    def findCurrentText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())
        
    def replaceCurrentText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        done = edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())
        if(done):
            edt.replaceText(self.lineEdit_2.text())
        else:
            QMessageBox.about(self, "About Sabel IDE","Could Not Find Text")
        return done
            
    def replaceAllText(self):
        edt = self.tabWidget.widget(self.tabWidget.currentIndex())
        while(edt.findText(self.lineEdit.text(),self.regex.isChecked(),self.caseSensitive.isChecked(),self.wholeWord.isChecked(),self.backward.isChecked())):
            edt.replaceText(self.lineEdit_2.text())
            
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
            self.tabWidget.widget(i).setThreshold(val)
            
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
            
    def getFile(self):
        fname = str(QFileDialog.getOpenFileName(self,"Open File", '.', "Files (*.*)"))
        if not (fname == ""):
            self.runEdit.setText(fname)
            
    def addCmd(self,index):
        if(index == 0):
            text, ok = QInputDialog.getText(self, 'Add Command', 'Command:')
            if(ok):
                if(str(text) != ''):
                    cmd = str(text)
                    self.cmdList.append(cmd)
                    #print self.cmdList
                    self.combo.addItem(cmd)
                    config.setCmd(self.cmdList)
                
    def delCmd(self,index):
        pass
        