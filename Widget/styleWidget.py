from PyQt4.QtGui import (QWidget, QHBoxLayout, QPushButton, QColorDialog, QLabel, QColor)
from globals import config
from PyQt4.QtCore import Qt, SIGNAL

'''
2 connections for btn one is to self set btnColor 
another is to change config and lexer'''

class StyleWidget(QWidget):
    def __init__(self,parent,text,color):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.hb = QHBoxLayout()
        self.color = color
        self.text = text
        #self.hb.setMargin(8)
        #self.hb.setSpacing(0)
        #self.setStyleSheet(popbg)
        '''
        QLabel{
            /*background: qlineargradient(x1: 0, y1: 1, x2: 0.08, y2: 0.05,stop: 0.2 #e8f2fe, stop: 0.9 #d8f2dd);*/
            border: 1px solid gray;
            font-size: 12px;
            padding-left: 15px;
            padding-top: 5px;
            border-radius: 30px;
        }
        '''
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setText(self.text+":"+self.color)
        self.btn = QPushButton()
        self.btn.setText("Color")
        self.setBtnColor()
        
        self.btn.clicked.connect(self.setColor)
        self.hb.addWidget(self.label)
        self.hb.addWidget(self.btn)
        self.setLayout(self.hb)
        
    def setBtnColor(self):
        sheet = '''
        QPushButton {
            background-color: %s /*QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c)*/;
            border-width: 1px;
            border-color: #339;
            border-style: solid;
            border-radius: 7;
            padding: 3px;
            font-size: 10px;
            padding-left: 5px;
            padding-right: 5px;
            min-width: 50px;
            max-width: 50px;
            min-height: 13px;
            max-height: 13px;
        }
        '''%(self.color)
        self.btn.setStyleSheet(sheet)
        
    def setColor(self):
        colorDialog = QColorDialog(self)
        colorDialog.setOption(QColorDialog.ShowAlphaChannel)
        #list = QColor().colorNames()
        #for i in list:
        #    print(i)
        self.color = colorDialog.getColor()
        self.color = self.color.name()
        self.label.setText(self.text+":"+self.color)
        self.setBtnColor()
        self.emit(SIGNAL("colorChange"),str(self.text),str(self.color))