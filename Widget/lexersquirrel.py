from PyQt4.Qsci import QsciLexerCustom,QsciStyle,QsciScintilla,QsciLexerPython
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFont, QColor
from globals import fontName, fontSize

class LexerSquirrel(QsciLexerPython):
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
        
    def __init__(self,colorStyle, parent = None):
        QsciLexerPython.__init__(self, parent)
        #self.parent = parent
        #self.sci = self.parent
        #print self.FunctionMethodName
        self.colorStyle = colorStyle
        self.plainFont = QFont()
        self.plainFont.setFamily(fontName)
        self.plainFont.setFixedPitch(True)
        self.plainFont.setPointSize(fontSize)
        self.marginFont = QFont()
        self.marginFont.setPointSize(10)
        self.marginFont.setFamily("MS Dlg")
        self.boldFont = QFont(self.plainFont)
        self.boldFont.setBold(True)
        """    
        enum {
          Default = 0, Comment = 1, Number = 2,
          DoubleQuotedString = 3, SingleQuotedString = 4, Keyword = 5,
          TripleSingleQuotedString = 6, TripleDoubleQuotedString = 7, ClassName = 8,
          FunctionMethodName = 9, Operator = 10, Identifier = 11,
          CommentBlock = 12, UnclosedString = 13, HighlightedIdentifier = 14,
          Decorator = 15
        }
        enum IndentationWarning {
          NoWarning = 0, Inconsistent = 1, TabsAfterSpaces = 2,
          Spaces = 3, Tabs = 4
        } 
        """
        self.styles = [
          #index description color paper font eol
          QsciStyle(0, QString("base"), self.colorStyle.color, self.colorStyle.paper, self.plainFont, True),
          QsciStyle(1, QString("comment"), QColor("#008000"), self.colorStyle.paper, self.plainFont, True),
          QsciStyle(2, QString("number"), QColor("#008000"), self.colorStyle.paper, self.boldFont, False),
          QsciStyle(3, QString("DoubleQuotedString"), QColor("#008000"), self.colorStyle.paper, self.plainFont, True),
          QsciStyle(4, QString("SingleQuotedString"), QColor("#008000"), self.colorStyle.paper, self.plainFont, True),
          QsciStyle(5, QString("Keyword"), QColor("#00003f"), self.colorStyle.paper, self.boldFont, True),
          QsciStyle(6, QString("TripleSingleQuotedString"), QColor("#ffd0d0"),self.colorStyle.paper, self.plainFont, True),
          QsciStyle(7, QString("TripleDoubleQuotedString"),QColor("#001111"),self.colorStyle.paper, self.plainFont, False),
          QsciStyle(8, QString("ClassName"), QColor("#000000"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(9, QString("FunctionMethodName"), QColor("#000000"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(10, QString("Operator"), QColor("#ff00ff"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(11, QString("Identifier"), QColor("#000000"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(12, QString("CommentBlock"), QColor("#000000"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(13, QString("UnclosedString"), QColor("#010101"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(14, QString("HighlightedIdentifier"), QColor("#0000ff"), self.colorStyle.paper, self.plainFont, False),
          QsciStyle(15, QString("Decorator"), QColor("#ff00ff"), self.colorStyle.paper, self.plainFont, False)
          #QsciStyle(7, QString("MultiComment_start"), QColor("#ff00ff"), QColor("#001111"), self.plainFont, False),
          #QsciStyle(8, QString("MultiComment"), QColor("#ff00ff"), QColor("#001111"), self.plainFont, False),
          #QsciStyle(9, QString("MultiComment_stop"), QColor("#ff00ff"), QColor("#001111"), self.plainFont, False)
        ]
        self._foldcompact = True
        
    def setColorStyle(self,cs):
        self.colorStyle = cs
        for i in self.styles:
            i.setPaper(self.colorStyle.paper)
        self.styles[0].setColor(self.colorStyle.color)
        
        
    def language(self):
        return 'Squirrel'
    
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
        return QsciLexerCustom.defaultColor(self, ix)

    def defaultFont(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.font()
        return QsciLexerCustom.defaultFont(self, ix)

    def defaultPaper(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.paper()
        return QsciLexerCustom.defaultPaper(self, ix)

    def defaultEolFill(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.eolFill()
        return QsciLexerCustom.defaultEolFill(self, ix)
    
    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        GETFOLDLEVEL = QsciScintilla.SCI_GETFOLDLEVEL
        SETFOLDLEVEL = QsciScintilla.SCI_SETFOLDLEVEL
        HEADERFLAG = QsciScintilla.SC_FOLDLEVELHEADERFLAG
        LEVELBASE = QsciScintilla.SC_FOLDLEVELBASE
        NUMBERMASK = QsciScintilla.SC_FOLDLEVELNUMBERMASK
        WHITEFLAG = QsciScintilla.SC_FOLDLEVELWHITEFLAG
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return
           
        compact = self.foldCompact()
        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)
        if index > 0:
            pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index - 1)
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)
        else:
            prevState = self.styles[0]
            
        self.startStyling(start, 0x1f)
        for line in source.splitlines(True):
          #  print line
            length = len(line)
            # We must take care of empty lines.This is done here.
            if length == 1:
                if prevState == self.styles[8] or prevState == self.styles[7]:
                    newState = self.styles[8]
                else:
                    newState = self.styles[0]
            #if line.startswith('#'):
            #    newState = self.styles[3]
            #elif line.startswith('\t+') or line.startswith('    +'):
            #    newState = self.styles[3]
            #We work with a non empty line.
            else:
                if line.startswith('@'):
                    newState = self.styles[7]
                elif line.startswith('@'):
                    if prevState == self.styles[8] or prevState == self.styles[7]:
                        newState = self.styles[9]
                    else:
                        newState = self.styles[0]
                #elif line.startswith('//'):
                #    if prevState == self.styles[8] or prevState == self.styles[7]:
                #        newState = self.styles[8]
                #    else:
                #        newState = self.styles[8]
                elif prevState == self.styles[8] or prevState == self.styles[7]:
                    newState = self.styles[8]
                else:
                    newState = self.styles[0]
            #set_style(length, newState)
                pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                i = 0
                while i < length:
                    wordLength = 1
                    
                    self.startStyling(i + pos, 0x1f)
                    newState = self.styles[0]
                    
                    for word in self.words2:
                        if line[i:].startswith(word):
                                newState = self.styles[4]
                                wordLength = len(word)
                        
                    
                    if chr(line[i]) in '0123456789':
                        newState = self.styles[4]
                    else:
                        if line[i:].startswith("class"):
                                newState = self.styles[2]
                                wordLength = len('class')
                        elif line[i:].startswith('function'):
                                newState = self.styles[3]
                                wordLength = len('function')
                        elif line[i:].startswith(' if'):
                                newState = self.styles[4]
                                wordLength = len(' if')
                        elif line[i:].startswith('#'):
                                newState = self.styles[4]
                                wordLength = length
                        elif line[i:].startswith('//'):
                                newState = self.styles[4]
                                wordLength = length
                        elif line[i:].startswith('/*'):
                                newState = self.styles[4]
                                wordLength = length
                        elif line[i:].startswith('*/'):
                                newState = self.styles[4]
                                wordLength = length
                        #else:
                            #newState = self.styles[0]
                    
                         
                    i += wordLength
                    set_style(wordLength, newState)
                newState = None
            
            if newState:
                set_style(length, newState)
                
            #Folding
            # folding implementation goes here
            #levelFolder = editor.SendScintilla(editor.SCI_GETFOLDLEVEL, index-1)
            #if line.startswith('+'):
            #     SCI(SETFOLDLEVEL, index, levelFolder + 1)
            #     #editor.SendScintilla(editor.SCI_SETFOLDLEVEL, index, levelFolder + 1)
            #elif line.startswith('function'):
            #     SCI(SETFOLDLEVEL, index, levelFolder + 1)
                 #editor.SendScintilla(editor.SCI_SETFOLDLEVEL, index, levelFolder + 1)
            """
            if newState == self.styles[7]:
                if prevState == self.styles[8]:
                    level = LEVELBASE + 1
                else:
                    level = LEVELBASE | HEADERFLAG
            elif newState == self.styles[8] or newState == self.styles[9]:
                level = LEVELBASE + 1
            else:
                level = LEVELBASE

            SCI(SETFOLDLEVEL, index, level)

            pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index)
            prevState = SCI(QsciScintilla.SCI_GETSTYLEAT, pos)"""
            index += 1


"""
import sys
from PyQt4 import QtCore, QtGui, Qsci

class MainWindow(QtGui.QMainWindow):
     def __init__(self):
         QtGui.QMainWindow.__init__(self)
         self.setWindowTitle('Custom Lexer Example')
         self.setGeometry(QtCore.QRect(50,200,400,400))
         self.editor = Qsci.QsciScintilla(self)
         self.editor.setUtf8(True)
         self.editor.setMarginWidth(2, 15)
         self.editor.setFolding(True)
         self.setCentralWidget(self.editor)
         self.lexer = CustomLexer(self.editor)
         self.editor.setLexer(self.lexer)
         self.editor.setText('\n# sample source\n\nfoo = 1\nbar = 2\n')

class CustomLexer(Qsci.QsciLexerCustom):
     def __init__(self, parent):
         Qsci.QsciLexerCustom.__init__(self, parent)
         self._styles = {
             0: 'Default',
             1: 'Comment',
             2: 'Key',
             3: 'Assignment',
             4: 'Value',
             }
         for key,value in self._styles.iteritems():
             setattr(self, value, key)

     def description(self, style):
         return self._styles.get(style, '')

     def defaultColor(self, style):
         if style == self.Default:
             return QtGui.QColor('#000000')
         elif style == self.Comment:
             return QtGui.QColor('#C0C0C0')
         elif style == self.Key:
             return QtGui.QColor('#0000CC')
         elif style == self.Assignment:
             return QtGui.QColor('#CC0000')
         elif style == self.Value:
             return QtGui.QColor('#00CC00')
         return Qsci.QsciLexerCustom.defaultColor(self, style)

     def styleText(self, start, end):
         editor = self.editor()
         if editor is None:
             return

         # scintilla works with encoded bytes, not decoded characters.
         # this matters if the source contains non-ascii characters and
         # a multi-byte encoding is used (e.g. utf-8)
         source = ''
         if end > editor.length():
             end = editor.length()
         if end > start:
             if sys.hexversion >= 0x02060000:
                 # faster when styling big files, but needs python 2.6
                 source = bytearray(end - start)
                 editor.SendScintilla(
                     editor.SCI_GETTEXTRANGE, start, end, source)
             else:
                 source = unicode(editor.text()
                                 ).encode('utf-8')[start:end]
         if not source:
             return

         # the line index will also be needed to implement folding
         index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
         if index > 0:
             # the previous state may be needed for multi-line styling
             pos = editor.SendScintilla(
                       editor.SCI_GETLINEENDPOSITION, index - 1)
             state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
         else:
             state = self.Default

         set_style = self.setStyling
         self.startStyling(start, 0x1f)

         # scintilla always asks to style whole lines
         for line in source.splitlines(True):
             length = len(line)
             if line.startswith('#'):
                 state = self.Comment
             else:
                 # the following will style lines like "x = 0"
                 pos = line.find('=')
                 if pos > 0:
                     set_style(pos, self.Key)
                     set_style(1, self.Assignment)
                     length = length - pos - 1
                     state = self.Value
                 else:
                     state = self.Default
             set_style(length, state)
             # folding implementation goes here
             levelFolder = editor.SendScintilla(editor.SCI_GETFOLDLEVEL, index-1)
             if line.startswith('+ '):
                 editor.SendScintilla(editor.SCI_SETFOLDLEVEL, index, levelFolder + 1)
             index += 1

if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                 QtCore.SLOT('quit()'))
     win = MainWindow()
     win.show()
     sys.exit(app.exec_())
"""