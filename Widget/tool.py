from PyQt4.QtGui import (QWidget, QHBoxLayout, QPushButton, QColorDialog, QToolBar, QMenu, QAction, QActionGroup ,QSlider, QWidgetAction,
                         QFont, QFontComboBox, QComboBox, QLabel)
from PyQt4.QtCore import SIGNAL, Qt, QSize
from PyQt4 import Qsci
from globals import config, Icons, Encoding, oslistdir, apiDir
from styleWidget import StyleWidget
    
class Tool(QToolBar):
    def __init__(self,parent):
        QToolBar.__init__(self,parent)
        self.parent = parent
        self.action_NewProject = QAction(Icons.newprj, 'Project', self)
        self.action_NewProject.triggered.connect(self.parent.treeWidget.newProject)
        self.action_NewProject.setToolTip("Create a New Project")

        self.action_Open = QAction(Icons.open, 'Open', self)
        self.action_Open.triggered.connect(self.parent.fileOpen)
        self.action_Open.setToolTip("Open File")

        self.action_Save = QAction(Icons.save, 'Save', self)
        self.action_Save.setShortcut('Ctrl+S')
        self.action_Save.triggered.connect(self.parent.fileSave)
        self.action_Save.setToolTip("Save Current File")

        self.action_SaveAll = QAction(Icons.saveall, 'SaveAll', self)
        self.action_SaveAll.setShortcut('Ctrl+A')
        self.action_SaveAll.triggered.connect(self.parent.fileSaveAll)
        self.action_SaveAll.setToolTip("Save All Files")
        
        
        
        self.action_Build = QAction(Icons.thread_view, 'Build', self)
        self.action_Build.setShortcut('Ctrl+B')
        self.action_Build.triggered.connect(self.parent.build_project)
        self.action_Debug = QAction(Icons.debug_exec, 'Debug', self)
        self.action_Refresh = QAction(Icons.refresh_tab, 'Refresh', self)
        self.action_Refresh.triggered.connect(self.parent.treeWidget.refreshCurrentProject)
        
        self.action_Run = QAction(Icons.run, 'Run', self)
        self.action_Run.setShortcut('Ctrl+R')
        self.action_Run.triggered.connect(self.parent.adb.run)
        self.action_RunFile = QAction(Icons.go, 'Cmd', self)
        self.action_RunFile.triggered.connect(self.parent.openCommand)
        self.parent.runButton.clicked.connect(self.parent.command.setCmdLine)
        self.action_Stop = QAction(Icons.stop, 'Stop', self)
        self.action_Stop.setShortcut('Ctrl+Q')
        self.action_Stop.triggered.connect(self.parent.adb.stop)
        self.action_Design = QAction(Icons.color_palette, 'Design', self)
        self.action_Design.triggered.connect(self.parent.design)
        self.action_Level = QAction(Icons.cmpC_pal, 'Level', self)
        self.action_Level.triggered.connect(self.parent.level)
        self.action_Todo = QAction(Icons.task_set, 'Todo', self)
        self.action_Todo.triggered.connect(self.parent.todo)
        
        self.action_Help = QAction(Icons.toc_open, 'Help', self)
        self.action_Help.triggered.connect(self.parent.help)
        self.action_Full = QAction(Icons.fullscreen, 'Full', self)
        self.action_Full.triggered.connect(self.parent.full)

        self.action_Stop.setDisabled(True)
        self.setToolLabel()
        self.setAllowedAreas(Qt.AllToolBarAreas)
        #self.setFixedHeight(40)
        #self.setIconSize(QSize(config.iconSize(),config.iconSize()))

        ''' Adding all Actions '''
        self.addAction(self.action_NewProject)
        self.addAction(self.action_Open)
        self.addAction(self.action_Save)
        self.addAction(self.action_SaveAll)
        #self.addAction(self.action_Refresh)
        self.addSeparator()
        self.addAction(self.action_Build)
        self.addAction(self.action_Run)
        #self.addAction(self.action_RunFile)
        self.addAction(self.action_Stop)
        self.addAction(self.action_Debug)
        self.addSeparator()
        self.addAction(self.action_Design)
        self.addAction(self.action_Level)
        self.addAction(self.action_Todo)
        self.initOptionsMenu()
        self.addSeparator()
        self.initStyleMenu()
        self.initLexerMenu()
        self.initApiMenu()
        #self.addAction(self.action_Help)
        #self.addAction(self.action_Full)
        self.addSeparator()
        self.initModeMenu()
            
    def colorChange(self, text, color):
        #print "colorChange ",text,color
        editStyle = config.readStyle()
        editStyle[text] = color
        config.writeStyle(editStyle)
        for i in range(len(self.parent.files)):
            self.parent.tabWidget.widget(i).setEditorStyle()
            
    def setColors(self,action):
        print action.text()
        
    def changeAll(self):
        self.colorChange("base", "#ffffff")
            
    def setIcon(self,val):
        config.setIconSize(val)
        self.setIconSize(QSize(val,val))
        
        
    def setToolLabel(self):
        if (config.toolLabel()):
            self.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.setIconSize(QSize(24,24))
        else:
            self.setIconSize(QSize(16,16))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
    '''Important for multiple callbacks in for loop'''
    def make_callback(self, text):
        return lambda:self.colorChange(text)
    
    ''' Options Menu '''
    def initOptionsMenu(self):
        men = QMenu()
        
        #Threshold Slider
        self.threshSlider = QSlider()
        self.threshSlider.setTickPosition(QSlider.TicksLeft)
        self.threshSlider.setOrientation(Qt.Horizontal)
        self.threshSlider.setValue(config.thresh())
        self.threshSlider.setMinimum(0)
        self.threshSlider.setMaximum(5)
        self.threshSlider.valueChanged.connect(self.parent.setThreshold)
        self.threshSliderAction = QWidgetAction(men)
        self.threshSliderAction.setDefaultWidget(self.threshSlider)
        
        #TabsWidth Slider
        self.tabsSlider = QSlider()
        self.tabsSlider.setTickPosition(QSlider.TicksLeft)
        self.tabsSlider.setOrientation(Qt.Horizontal)
        self.tabsSlider.setValue(config.tabwidth())
        self.tabsSlider.setMinimum(0)
        self.tabsSlider.setMaximum(8)
        self.tabsSlider.valueChanged.connect(self.parent.setTabWidth)
        self.tabsSliderAction = QWidgetAction(men)
        self.tabsSliderAction.setDefaultWidget(self.tabsSlider)
        
        #iconSize Slider
        self.iconSlider = QSlider()
        self.iconSlider.setTickPosition(QSlider.TicksLeft)
        self.iconSlider.setOrientation(Qt.Horizontal)
        self.iconSlider.setValue(config.iconSize())
        self.iconSlider.setMinimum(16)
        self.iconSlider.setMaximum(32)
        self.iconSlider.setSingleStep(2)
        self.iconSlider.valueChanged.connect(self.setIcon)
        self.iconSliderAction = QWidgetAction(men)
        self.iconSliderAction.setDefaultWidget(self.iconSlider)
        
        '''Font Button'''
        self.fontCombo = QFontComboBox()
        self.fontCombo.currentFontChanged.connect(self.parent.setFont)
        self.fontCombo.setCurrentFont(QFont(config.fontName()))
        self.fontComboMenu = QWidgetAction(men)
        self.fontComboMenu.setDefaultWidget(self.fontCombo)
        
        '''Font Size'''
        self.fontSizeCombo = QComboBox()
        for size in range(1,40):
            self.fontSizeCombo.addItem(str(size))
        self.fontSizeCombo.setCurrentIndex(config.fontSize())
        self.fontSizeCombo.currentIndexChanged.connect(self.parent.setFontSize)
        self.fontSizeComboMenu = QWidgetAction(men)
        self.fontSizeComboMenu.setDefaultWidget(self.fontSizeCombo)
        
        
        action_Android = QAction(Icons.android,'Android', self)
        action_Android.triggered.connect(self.parent.android)
        action_Ant = QAction(Icons.ant_view,'Ant', self)
        action_Ant.triggered.connect(self.parent.antt)
        action_Squirrel = QAction(Icons.nut,'Squirrel', self)
        action_Squirrel.triggered.connect(self.parent.squirrel)
        action_Ios1 = QAction(Icons.ios,'iOS', self)
        action_Update = QAction(Icons.update,"Update",self)
        action_Update.triggered.connect(self.parent.update)
        
        action_explorer = QAction("Explorer",self)
        action_explorer.triggered.connect(self.parent.exp)
        action_explorer.setCheckable(True)
        action_explorer.setChecked(True)
        action_console = QAction("Console",self)
        action_console.triggered.connect(self.parent.cmd)
        action_console.setCheckable(True)
        action_console.setChecked(False)
        #action_designer = QAction("Designer",self)
        #action_designer.triggered.connect(self.parent.design)
        action_Indentation = QAction("Indentation Guides",self)
        action_Indentation.triggered.connect(self.parent.setIndent)
        action_Indentation.setCheckable(True)
        action_Indentation.setChecked(config.indent())
        action_WhiteSpace = QAction("WhiteSpace",self)
        action_WhiteSpace.triggered.connect(self.parent.setWhiteSpace)
        action_WhiteSpace.setCheckable(True)
        action_WhiteSpace.setChecked(config.whiteSpace())
        action_EndLine = QAction("End of Lines",self)
        action_EndLine.triggered.connect(self.parent.setEndLine)
        action_EndLine.setCheckable(True)
        action_Margin = QAction("Line Numbers",self)
        action_Margin.triggered.connect(self.parent.setMargin)
        action_Margin.setCheckable(True)
        action_Margin.setChecked(config.margin())
        action_ToolLabel = QAction("Tool Labels",self)
        action_ToolLabel.triggered.connect(self.setToolLabel)
        action_ToolLabel.setCheckable(True)
        #action_ToolLabel.setChecked(config.toolLabel())
        
        '''Encoding'''
        encodingGroup = QActionGroup(self)
        encodingGroup.setExclusive(True)
        action_Ascii = QAction("Ascii",encodingGroup)
        action_Ascii.setCheckable(True)
        action_Unicode = QAction("Unicode",encodingGroup)
        action_Unicode.setCheckable(False)
        encodingGroup.addAction(action_Ascii)
        encodingGroup.addAction(action_Unicode)
        encodingGroup.selected.connect(self.parent.setEncoding)
        if(config.encoding() == Encoding.ASCII):
            action_Ascii.setChecked(True)
        else:
            action_Unicode.setChecked(True)
        men.addAction(action_Update)
        men.addAction(self.action_Help)
        men.addAction(self.action_Full)
        men.addSeparator()
        men.addAction(action_Android)
        men.addAction(action_Ant)
        men.addAction(action_Squirrel)
        men.addAction(action_Ios1)
        
        men.addSeparator()
        men.addAction(action_explorer)
        men.addAction(action_console)
        #men.addAction(action_designer)
        men.addSeparator()
        men.addAction(action_Indentation)
        men.addAction(action_WhiteSpace)
        men.addAction(action_EndLine)
        men.addAction(action_Margin)
        men.addAction(action_ToolLabel)
        men.addSeparator()
        men.addActions(encodingGroup.actions())
        men.addSeparator()
        head_font = QLabel("Font---------------------")
        fnt = head_font.font()
        fnt.setBold(True)
        head_font.setFont(fnt)
        head_fontWidgetAction = QWidgetAction(men)
        head_fontWidgetAction.setDefaultWidget(head_font)
        men.addAction(head_fontWidgetAction)
        men.addAction(self.fontComboMenu)
        men.addAction(self.fontSizeComboMenu)
        men.addSeparator()
        men.addAction(QAction("TabWidth",self))
        men.addAction(self.tabsSliderAction)
        men.addSeparator()
        men.addAction(QAction("Threshold",self))
        men.addAction(self.threshSliderAction)
        #men.addAction(QAction("Icon Size",self))
        #men.addAction(self.iconSliderAction)
        
        self.action_Options = QAction(Icons.emblem_system, 'Options', self)
        self.action_Options.setMenu(men)
        self.addAction(self.action_Options)
    
    ''' Mode Menu '''
    def initModeMenu(self):
        self.modeGroup = QActionGroup(self)
        self.modeGroup.setExclusive(True)
        self.modeGroup.selected.connect(self.parent.setMode)
        self.action_Squirrel = QAction(Icons.nut, 'Squ', self.modeGroup)
        self.action_Squirrel.setCheckable(True)
        self.action_Emo = QAction(Icons.emo, 'Emo', self.modeGroup)
        self.action_Emo.setCheckable(True)
        self.action_And = QAction(Icons.android, 'Android', self.modeGroup)
        self.action_And.setCheckable(True)
        self.action_Ios = QAction(Icons.ios, 'ios', self.modeGroup)
        self.action_Ios.setCheckable(True)
        self.modeGroup.addAction(self.action_Squirrel)
        self.modeGroup.addAction(self.action_Emo)
        self.modeGroup.addAction(self.action_And)
        self.modeGroup.addAction(self.action_Ios)
        self.addActions(self.modeGroup.actions())
        if(config.mode() == 0):
            self.action_Squirrel.setChecked(True)
            self.action_Build.setEnabled(False)
            self.action_Run.setEnabled(False)
        elif(config.mode() == 1):
            self.action_Emo.setChecked(True)
            self.action_Build.setEnabled(True)
            self.action_Run.setEnabled(True)
        elif(config.mode() == 2):
            self.action_And.setChecked(True)
            self.action_Build.setEnabled(True)
            self.action_Run.setEnabled(True)
        elif(config.mode() == 3):
            self.action_Ios.setChecked(True)
            self.action_Build.setEnabled(False)
            self.action_Run.setEnabled(False)
        
    
    ''' Style Menu '''
    def initStyleMenu(self):
        editStyle = config.readStyle()
        self.action_Style = QAction(Icons.style, 'Style', self) 
        men = QMenu(self)
        men1 = QMenu()
        self.base = StyleWidget(self,"base",editStyle["base"])
        self.back = StyleWidget(self,"back",editStyle["back"])
        self.caret = StyleWidget(self,"caret",editStyle["caret"])
        self.margin = StyleWidget(self,"margin",editStyle["margin"])
        self.marker = StyleWidget(self,"marker",editStyle["marker"])
        self.comment = StyleWidget(self,"comment",editStyle["comment"])
        self.number = StyleWidget(self,"number",editStyle["number"])
        self.keyword = StyleWidget(self,"keyword",editStyle["keyword"])
        self.string = StyleWidget(self,"string",editStyle["string"])
        self.operator = StyleWidget(self,"operator",editStyle["operator"])
        self.connect(self.base, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.back, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.caret, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.margin, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.marker, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.comment, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.number, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.keyword, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.string, SIGNAL("colorChange"),self.colorChange)
        self.connect(self.operator, SIGNAL("colorChange"),self.colorChange)
        self.baseMenu = QWidgetAction(men)
        self.baseMenu.setDefaultWidget(self.base)
        self.backMenu = QWidgetAction(men)
        self.backMenu.setDefaultWidget(self.back)
        self.caretMenu = QWidgetAction(men)
        self.caretMenu.setDefaultWidget(self.caret)
        self.marginMenu = QWidgetAction(men)
        self.marginMenu.setDefaultWidget(self.margin)
        self.markerMenu = QWidgetAction(men)
        self.markerMenu.setDefaultWidget(self.marker)
        self.commentMenu = QWidgetAction(men)
        self.commentMenu.setDefaultWidget(self.comment)
        self.numberMenu = QWidgetAction(men)
        self.numberMenu.setDefaultWidget(self.number)
        self.keywordMenu = QWidgetAction(men)
        self.keywordMenu.setDefaultWidget(self.keyword)
        self.stringMenu = QWidgetAction(men)
        self.stringMenu.setDefaultWidget(self.string)
        self.operatorMenu = QWidgetAction(men)
        self.operatorMenu.setDefaultWidget(self.operator)
        self.styleGroup = QActionGroup(self)
        self.styleGroup.setExclusive(True)
        self.styleGroup.selected.connect(self.setColors)
        self.style1 = QAction("All Hallow's Eve",self.styleGroup)
        self.style1.setCheckable(True)
        self.style2 = QAction("Amy",self.styleGroup)
        self.style2.setCheckable(True)
        self.style3 = QAction("Aptana Studio",self.styleGroup)
        self.style3.setCheckable(True)
        self.style4 = QAction("Bespin",self.styleGroup)
        self.style4.setCheckable(True)
        self.style5 = QAction("Blackboard",self.styleGroup)
        self.style5.setCheckable(True)
        self.style6 = QAction("Choco",self.styleGroup)
        self.style6.setCheckable(True)
        self.style7 = QAction("Cobalt",self.styleGroup)
        self.style7.setCheckable(True)
        self.style8 = QAction("Dawn",self.styleGroup)
        self.style8.setCheckable(True)
        self.style9 = QAction("Eclipse",self.styleGroup)
        self.style9.setCheckable(True)
        self.styleGroup.addAction(self.style1)
        self.styleGroup.addAction(self.style2)
        self.styleGroup.addAction(self.style3)
        self.styleGroup.addAction(self.style4)
        self.styleGroup.addAction(self.style5)
        self.styleGroup.addAction(self.style6)
        self.styleGroup.addAction(self.style7)
        self.styleGroup.addAction(self.style8)
        self.styleGroup.addAction(self.style9)
        men1.addAction(self.baseMenu)
        men1.addAction(self.backMenu)
        men1.addAction(self.caretMenu)
        men1.addAction(self.marginMenu)
        men1.addAction(self.markerMenu)
        men1.addAction(self.commentMenu)
        men1.addAction(self.numberMenu)
        men1.addAction(self.keywordMenu)
        men1.addAction(self.stringMenu)
        men1.addAction(self.operatorMenu)
        men1.addSeparator()
        men2 = QMenu(self)
        men2.setTitle("Styles")
        men2.addActions(self.styleGroup.actions())
        men1.addMenu(men2)
        self.action_Style.setMenu(men1)
        self.addAction(self.action_Style)
       
    ''' Lexer Menu'''
    def make_action_lex(self, text):
        action = QAction(text, self.lexGroup)
        action.setCheckable(True)
        return action
   
    def initLexerMenu(self):
        self.action_Lexer = QAction(Icons.file_obj, 'Lexer', self)
        men = QMenu()
        self.lexGroup = QActionGroup(self)
        self.lexGroup.setExclusive(True)
        self.lexGroup.selected.connect(self.parent.setLexer)
        #langs = [i for i in dir(Qsci) if i.startswith('QsciLexer')]
        langs = ['Bash', 'Batch', 'CMake', 'CPP', 'CSS', 'C#','HTML','Java', 'JavaScript', 'Lua', 'Makefile','Python', 'SQL', 'XML', 'YAML']
        for l in langs:
            act = self.make_action_lex(l)
            self.lexGroup.addAction(act)
            if(langs.index(l) == 8): #For javascript
                act.setChecked(True)
            #print l[9:] # we don't need to print "QsciLexer" before each name
        men.addActions(self.lexGroup.actions())
        self.action_Lexer.setMenu(men)
        self.addAction(self.action_Lexer)
        
    
        
    ''' Api Menu '''
    def make_action_api(self, text):
        action = QAction(text, self.apiGroup)
        action.setCheckable(True)
        return action
    
    def initApiMenu(self):
        self.action_Api = QAction(Icons.lib, 'Api', self)
        men = QMenu()
        self.apiGroup = QActionGroup(self)
        self.apiGroup.setExclusive(True)
        self.apiGroup.selected.connect(self.parent.setApi)
        list = oslistdir(apiDir)
        apis = []
        if(list != None):
            for i in list:
                if i.endswith("api"):
                    apis.append(i.replace(".api", ""))
        if(apis != None):
            for i in apis:
                act = self.make_action_api(i)
                self.apiGroup.addAction(act)
                if(i == "emo"): #For emo
                    act.setChecked(True)
        men.addActions(self.apiGroup.actions())
        self.action_Api.setMenu(men)
        self.addAction(self.action_Api)
        
        