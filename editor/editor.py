from globals import (ospathjoin,os_pixmap,apiDir,config,Auto,eol, Encoding)
from PyQt4.QtCore import SIGNAL,QString,QEvent
from PyQt4.QtGui import QFontMetrics, QFont, QPixmap, QColor, QPalette,QWidget
from PyQt4.Qsci import (QsciScintilla, QsciAbstractAPIs, QsciLexerPython ,QsciAPIs ,
                        QsciLexerCPP, QsciLexerJavaScript)
from format import Format

from cpp import CPP
from csharp import CSharp
from css import CSS
from html import HTML
from java import Java
from javascript import JavaScript
from lua import Lua
from neko import Neko
from python import Python
from sql import SQL
from squirrel import Squirrel
from xml import XML
from yaml import YAML

class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    def __init__(self,parent,text,nfile):
        QsciScintilla.__init__(self,parent)
        self.parent = parent
        self.errorLines = []
        self.setText(text)
        if(config.encoding() == Encoding.ASCII):
            self.setUtf8(False)
            #print "ascii set"
        else:
            self.setUtf8(True)
            #print "unicode set"
        if(eol == 0):
            self.setEolMode(self.EolWindows)
        elif(eol == 1):
            self.setEolMode(self.EolUnix)
        else:
            self.setEolMode(self.EolMac)
        if(config.whiteSpace()):
            self.setWhitespaceVisibility(True)
            
        self.cursorPositionChanged.connect(self.parent.updateLine)
        #self.linesChanged.connect(self.changeMarginWidht())           
        #Indicator
        #self.setIndicatorForegroundColor(self.colorStyle.color)
        #self.setIndicatorOutlineColor(self.colorStyle.paper)
        #Marker
        self.markerDefine(QsciScintilla.RightArrow,self.ARROW_MARKER_NUM)
        self.markerDefine(Auto.auto_error,0)
        self.font = QFont(config.fontName(),config.fontSize())
        #self.font.setFixedPitch(True)
        self.setFont(self.font)
        self.fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        
        # Margin 0 is used for line numbers
        self.setMarginSensitivity(0, True)
        #self.connect(self,SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),self.on_margin_clicked)
        self.setCaretLineVisible(True)
        #Code-Complete
        self.registerImage(0,Auto.auto_class2)
        self.registerImage(1,Auto.auto_method)
        self.registerImage(2,Auto.auto_field)
        self.registerImage(3,Auto.auto_package)
        self.setAutoCompletionThreshold(config.thresh())
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setBackspaceUnindents(True)
        self.setAutoCompletionCaseSensitivity(True)
        self.setIndentationsUseTabs(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setMargin(config.margin())
        self.setIndent(config.indent())
        self.setTabWidth(config.tabwidth())
        #self.copyAvailable.connect(self.highlightWord)
        #self.indicatorClicked.connect(self.indicate)
        self.setIndicatorOutlineColor(QColor("#000000"))
        self.indicatorDefine(self.INDIC_BOX)
        #self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        #self.setAutoCompletionSource(QsciScintilla.AcsAll)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        #self.setIndentation(5,25)
        #self.setSelectionBackgroundColor()
        #self.setSelectionForegroundColor()
        #self.SendScintilla(QsciScintilla.SCI_MARKERSETBACK,11,QColor(220,220,220))
        self.setLanguage(nfile)
        self.setEditorStyle() #important must not change this position
        self.setApi("emo")
        
    def setApi(self, text):
        self.api = QsciAPIs(self.lexer)
        self.api.load(ospathjoin(apiDir,text+".api"))
        self.api.prepare()
        self.lexer.setAPIs(self.api) #Very important do not change line otherwise gg
        self.setLexer(self.lexer) #Very important do not change line otherwise gg
        editStyle = config.readStyle()
        self.setMarginsBackgroundColor(QColor(editStyle["margin"]))
        '''This is done cause the margin color is set only when lexer is set 
            dont know maybe a bug'''
        
        
        
        
    def setEditorStyle(self):
        ''' Bolldy some problem here the margin bg color is not set when init'ed '''
        ''' But when i change it in the styles menu it changes sad'''
        editStyle = config.readStyle()
        self.setCaretLineBackgroundColor(QColor(editStyle["caret"]))
        self.setMarginsBackgroundColor(QColor(editStyle["margin"]))
        self.setMarkerBackgroundColor(QColor(editStyle["marker"]),self.ARROW_MARKER_NUM)
        self.lexer.setColors(editStyle)
        
    def setLanguage(self,nfile):
        ext = Format.get(nfile)
        if ext == 0:
           self.lexer = CPP(self)
        elif ext == 1:
             self.lexer = CSharp(self)    
        elif ext == 2:
            self.lexer = CSS(self)
        elif ext == 3:
            self.lexer = HTML(self)
        elif ext == 4:
            self.lexer = Java(self)
        elif ext == 5:
            self.lexer = JavaScript(self)
        elif ext == 6:
            self.lexer = Lua(self)
        elif ext == 7:
            self.lexer = Neko(self)
        elif ext == 8:
            self.lexer = Python(self)
        elif ext == 9:
            self.lexer = SQL(self)
        elif ext == 10:
            self.lexer = Squirrel(self)
        elif ext == 11:
            self.lexer = XML(self)
        elif ext == 12:
            self.lexer = YAML(self)
        else:
            self.lexer = Squirrel(self)
        self.lexer.setDefaultFont(self.font)
        
                     
    def highlightWord(self, bool):
        if(bool):
            print "yes"
            
    def indicate(self, line, index , key):
        print line
          
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
            
            
        #fix this lines not showing properly
    def addError(self,lineno):
        '''First delete all present markers then add new lines or errors'''
        '''sqc can only find out 1 error line just like an interpreter'''
        if(len(self.errorLines) == 0):
                self.errorLines.append(lineno-1)
                self.markerAdd(lineno-1, 0)
            #print self.errorLines

        #if self.markersAtLine() != 0:
        #     self.markerDelete(self.errorLines.pop(i), 0)
        #    for i in range(len(self.errorLines)):
        #        #if self.markersAtLine(self.errorLines.pop(i)) != 0:
        #            self.markerDelete(self.errorLines.pop(i), 0)
                    
        #assert self.errorLines == []
        
    def reset(self):
         if(len(self.errorLines) != 0):
             for i in self.errorLines:
                self.markerDelete(i, 0)
             self.errorLines[:] = []
        
    def setNewFont(self,font):
        self.setFont(font)
        self.lexer.setFont(font)
        
    def setFontSize(self):
        self.font.setPointSize(config.fontSize())
        self.lexer.setFont(self.font)
        
    def setMargin(self,mar):
        if(mar == 1):
            self.setMarginLineNumbers(1, True)
            if(self.lines()<1000):
                self.setMarginWidth(1, QString("-----"))
            else:
                self.setMarginWidth(1, QString("---------"))
        else:
            self.setMarginLineNumbers(1, False)
            ''' Because of white margin color cant show it'''
            self.setMarginWidth(1, QString("---"))
            
    def setMarginHide(self,bool):
        if(bool):
            self.setMarginWidth(1, QString(""))
        else:
            self.setMarginWidth(1, QString("---"))
            
    def setIndent(self,val):
        if(val == 0):
            self.setIndentationGuides(False)
        else:
            self.setIndentationGuides(True)
        
        
    def setThreshold(self,val):
        self.setAutoCompletionThreshold(val)
        
    def setLine(self,lineno):
        self.setFocus(True)
        ''' lineno -1 is for parser which points to next line'''
        self.setCursorPosition(int(lineno)-1,0)
        self.setCaretLineVisible(True)
        
    def getLine(self):
        print self.getCursorPosition()
       
        
            
            
    """
    findFirst     (     const QString &      expr,
        bool      re,
        bool      cs,
        bool      wo,
        bool      wrap,
        bool      forward = true,
        int      line = -1,
        int      index = -1,
        bool      show = true,
        bool      posix = false 
    )         [virtual]
    """
    def findText(self,text,re,cs,wo,bk):
        if(text != ''):
            done = self.findFirst(text,re,cs,wo,True,not bk)
            return done
     
    def replaceText(self,text):
        self.replace(text)
        
    def replaceFindText(self,text):
        self.replace(text)
        

