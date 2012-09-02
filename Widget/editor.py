from globals import (fontSize,fontName,ospathjoin,os_pixmap,apiDir,config
                     ,Auto,eol)
from PyQt4.QtCore import SIGNAL,QString,QEvent
from PyQt4.QtGui import QFontMetrics, QFont, QPixmap, QColor, QPalette,QWidget
from PyQt4.Qsci import QsciScintilla, QsciLexerPython ,QsciAPIs ,QsciLexerCPP
from lexersquirrel import LexerSquirrel
        
class Editor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    #fontSize = fontSize
    def __init__(self,parent,text,lang,colorStyle):
        QsciScintilla.__init__(self,parent)
        self.parent = parent
        self.lang = lang
        self.fontSize = fontSize
        self.colorStyle = colorStyle
        self.errorLines = []
        self.setText(text)
        if(eol == 0):
            self.setEolMode(self.EolWindows)
        elif(eol == 1):
            self.setEolMode(self.EolUnix)
        else:
            self.setEolMode(self.EolMac)
        self.init()
        self.setTabWidth(1)
        #self.installEventFilter(self)
        
    #def eventFilter(self, widget, event):
    #    if (event.type() == QEvent.ShortcutOverride and widget is self):
    #        #if event.type
    #        event.accept()
    #        return True
    #    return QWidget.eventFilter(self, widget, event)
    
    def init(self):
        #Margin
        #print self.marginType(self.SymbolMargin)
        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.setMarginsBackgroundColor(self.colorStyle.margin)
        self.connect(self,SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),self.on_margin_clicked)
        # Margin 0 is used for line numbers
        #self.setMarginLineNumbers(0, True)
        #self.setMarginWidth(0, self.fontmetrics.width("0000") + 6)
        self.setMarginLineNumbers(0, True)
        if(self.lines()<1000):
            self.setMarginWidth(0, QString("-------"))
        else:
            self.setMarginWidth(0, QString("---------"))   
        #self.linesChanged.connect(self.changeMarginWidht())   
                 
        #Caret
        self.setCaretLineBackgroundColor(self.colorStyle.caret)
        self.setCaretLineVisible(True)
        
        #Indicator
        #self.setIndicatorForegroundColor(self.colorStyle.color)
        #self.setIndicatorOutlineColor(self.colorStyle.paper)
        
        #Marker
        self.markerDefine(QsciScintilla.RightArrow,self.ARROW_MARKER_NUM)
        self.markerDefine(Auto.auto_error,0)
        self.setMarkerBackgroundColor(self.colorStyle.marker,self.ARROW_MARKER_NUM)
        
        #Code-Complete
        self.registerImage(0,Auto.auto_class2)
        self.registerImage(1,Auto.auto_method)
        self.registerImage(2,Auto.auto_field)
        self.setAutoCompletionThreshold(config.thresh())
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        
        #Property
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setBackspaceUnindents(True)
        self.setEolMode(self.EolWindows)
        #self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        #self.setAutoCompletionSource(QsciScintilla.AcsAll)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        
        self.font = QFont()
        self.font.setFamily(fontName)
        #self.font.setFixedPitch(True)
        self.font.setPointSize(self.fontSize)
        self.setFont(self.font)
        self.fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        
        if self.lang == 0:
            self.lexer = QsciLexerPython()
        elif self.lang == 1:
            self.lexer = QsciLexerCPP()
        elif self.lang == 2:
            self.lexer = LexerSquirrel(self.colorStyle,self)
        self.lexer.setDefaultFont(self.font)
        self.api = QsciAPIs(self.lexer)
        self.api.load(ospathjoin(apiDir,"emo.api"))
        self.api.prepare()
        self.lexer.setAPIs(self.api) #Very important do not change line otherwise gg
        self.setLexer(self.lexer) #Very important do not change line otherwise gg
        
        
    def setColorStyle(self,colorStyle):
        self.colorStyle = colorStyle
        self.setCaretLineBackgroundColor(self.colorStyle.caret)
        self.setMarginsBackgroundColor(self.colorStyle.margin)
        self.setMarkerBackgroundColor(self.colorStyle.marker,self.ARROW_MARKER_NUM)
        if self.lang == 2:
            self.lexer.setColorStyle(self.colorStyle)
            self.lexer.setColor(QColor("#008000"),0)       
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
            
            
        #fix this lines not showing properly
    def addError(self,lineno):
        '''First delete all present markers then add new lines or errors'''
        if(len(self.errorLines) == 0):
                self.errorLines.append(lineno-1)
                self.markerAdd(lineno-1, 0)
        else:
            #print self.errorLines
            for i in self.errorLines:
                self.markerDelete(i, 0)
            self.errorLines[:] = []
            self.errorLines.append(lineno-1)
            self.markerAdd(lineno-1, 0)
            #print self.errorLines

        #if self.markersAtLine() != 0:
        #     self.markerDelete(self.errorLines.pop(i), 0)
        #    for i in range(len(self.errorLines)):
        #        #if self.markersAtLine(self.errorLines.pop(i)) != 0:
        #            self.markerDelete(self.errorLines.pop(i), 0)
                    
        #assert self.errorLines == []
        
    
    def zoomin(self):
        self.fontSize += 1
        config.setFontSize(self.fontSize)
        self.font.setPointSize(self.fontSize)
        #self.setFont(self.font)
        self.lexer.setFont(self.font)
        self.setMarginsFont(self.font)
        
    def zoomout(self):
        self.fontSize -= 1
        config.setFontSize(self.fontSize)
        self.font.setPointSize(self.fontSize)
        #self.setFont(self.font)
        self.lexer.setFont(self.font)
        self.setMarginsFont(self.font)
        
    def setFontName(self,name):
        self.font.setFamily(name)
        self.lexer.setFont(self.font)
        
    def setThreshold(self,val):
        self.setAutoCompletionThreshold(val)
            
            
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
        

