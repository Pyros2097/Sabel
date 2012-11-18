from PyQt4.Qsci import QsciLexerCPP,QsciStyle,QsciScintilla, QsciLexerJavaScript
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFont, QColor
from globals import config

class Neko(QsciLexerJavaScript):
    words1 = [
         'base','break','case','catch','class','clone',
         'continue','const','default','delete','else','enum',
         'extends','for','foreach','function',' if',' in',
         'local','null','resume','return','switch','this',
         'throw','try','typeof','while','yield','constructor',
         'instanceof','true','false','static'
        ]
        
    words2 = [
         'init', 'dest', 'onLoad', 'onDispose', 'onGainedFocus','onMotionEvent',
         'onLostFocus','onUpdate','onFps','onKeyEvent','onSensorEvent',
         'onControlEvent','onDrawFrame','onError','onLowMemory','onNetCallBack'
        ]

    words3 = [
        'rawdelete', 'rawin', 'array', 'seterrorhandler', 'setdebughook',
        'enabledebuginfo', 'getroottable', 'setroottable', 'getconsttable',
        'setconsttable', 'assert', 'print', 'compilestring', 'collectgarbage',
        'type', 'getstackinfos', 'newthread', 'tofloat', 'tostring',
        'tointeger', 'tochar', 'weakref', 'slice', 'find', 'tolower',
        'toupper', 'len', 'rawget', 'rawset', 'clear', 'append', 'push',
        'extend', 'pop', 'top', 'insert', 'remove', 'resize', 'sort',
        'reverse', 'call', 'pcall', 'acall', 'pacall', 'bindenv', 'instance',
        'getattributes', 'getclass', 'getstatus', 'ref'
        ]
        
    def __init__(self,parent):
        QsciLexerJavaScript.__init__(self, parent)
        self.parent = parent
        self.plainFont = QFont()
        self.plainFont.setFamily(config.fontName())
        self.plainFont.setFixedPitch(True)
        self.plainFont.setPointSize(config.fontSize())
        self.boldFont = QFont(self.plainFont)
        self.boldFont.setBold(True)
        self.setFoldCompact(True)
        
    def setColors(self, editStyle):
        self.base = QColor(editStyle["base"]) #This is the font color
        self.back = QColor(editStyle["back"]) #This is the bg color
        self.comment = QColor(editStyle["comment"])
        self.number = QColor(editStyle["number"])
        self.keyword = QColor(editStyle["keyword"])
        self.string =  QColor(editStyle["string"])
        self.operator =  QColor(editStyle["operator"])
        self.styles = [
          #index description color paper font eol 
          QsciStyle(0, QString("base"), self.base, self.back, self.plainFont, True),
          QsciStyle(1, QString("comment"), self.comment, self.back, self.plainFont, True),
          QsciStyle(4, QString("number"), self.number, self.back, self.plainFont, True),
          QsciStyle(5, QString("Keyword"), self.keyword, self.back, self.boldFont, True),
          QsciStyle(6, QString("String"), self.string,self.back, self.plainFont, True),
          QsciStyle(10, QString("Operator"), self.operator, self.back, self.plainFont, False)    
        ]
        
    def language(self):
        return 'Neko'
    
    def foldCompact(self):
        return self._foldcompact

    def setFoldCompact(self, enable):
        self._foldcompact = bool(enable)

    def description(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.description()
        return QString("")
    
    def defaultColor(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.color()
        return QsciLexerCPP.defaultColor(self, ix)

    def defaultFont(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.font()
        return QsciLexerCPP.defaultFont(self, ix)

    def defaultPaper(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.paper()
        return QsciLexerCPP.defaultPaper(self, ix)

    def defaultEolFill(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.eolFill()
        return QsciLexerCPP.defaultEolFill(self, ix)