from PyQt4.Qsci import QsciLexerPython,QsciStyle
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFont, QColor
from globals import config

class Python(QsciLexerPython):   
    def __init__(self,parent):
        QsciLexerPython.__init__(self, parent)
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
        return 'Python'
    
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
        return QsciLexerPython.defaultColor(self, ix)

    def defaultFont(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.font()
        return QsciLexerPython.defaultFont(self, ix)

    def defaultPaper(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.paper()
        return QsciLexerPython.defaultPaper(self, ix)

    def defaultEolFill(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.eolFill()
        return QsciLexerPython.defaultEolFill(self, ix)