from PyQt4.QtGui import (QComboBox, QFontComboBox, QLabel, QFrame, QWidget, QPushButton, QHBoxLayout,
                         QLineEdit, QGroupBox, QColorDialog, QColor)

from PyQt4.QtCore import Qt, SIGNAL

from globals import config, Icons, eol


class HeadingBar(QGroupBox):
    def __init__(self,parent):
        QGroupBox.__init__(self,parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(0)
        self.setTitle("Screen")
        
        lab = QLabel("Name: ")
        lab1 = QLabel("Size: ")
        lab2 = QLabel("Orientation: ")
        self.lab3 = QLabel("Background: #000000")
        
        btn = QLineEdit("Menu1",self)
        btn1 = QComboBox()
        btn1.addItem("320x240")
        btn1.addItem("480x320")
        btn1.addItem("640x480")
        btn1.addItem("720x480")
        btn1.addItem("800x480")
        btn1.addItem("852x480")
        btn1.addItem("960x540")
        btn1.currentIndexChanged.connect(self.setScreenSize)
        btn2 = QComboBox()
        btn2.addItem("Portrait")
        btn2.addItem("Landscape")
        btn2.currentIndexChanged.connect(self.parent.setOrientation)
        
        btn3 = QPushButton("Color")
        btn3.clicked.connect(self.setColor)
        
        btn4 = QPushButton("Scroll")
        btn4.clicked.connect(self.parent.setScrollBar)
        
        self.layout.addWidget(lab)
        self.layout.addWidget(btn)
        self.layout.addWidget(lab1)
        self.layout.addWidget(btn1)
        self.layout.addWidget(lab2)
        self.layout.addWidget(btn2)
        self.layout.addWidget(self.lab3)
        self.layout.addWidget(btn3)
        self.layout.addWidget(btn4)
          
    def setScreenSize(self,idx):
        if(idx == 0):
            size = (320,240)
        elif(idx == 1):
            size = (480,320)
        elif(idx == 2):
            size = (640,480)
        elif(idx == 3):
            size = (720,480)
        elif(idx == 4):
            size = (800,480)
        elif(idx == 5):
            size = (852,480)
        elif(idx == 6):
            size = (960,540)
        self.parent.setScreenSize(size)
        
        
    def setColor(self):
        colorDialog = QColorDialog(self)
        colorDialog.setOption(QColorDialog.ShowAlphaChannel)
        #list = QColor().colorNames()
        #for i in list:
        #    print(i)
        color = colorDialog.getColor()
        self.lab3.setText("Background: "+color.name())
        self.parent.setBackgroundColor(color)
        
class WidgetsBar(QGroupBox):
    def __init__(self,parent):
        QFrame.__init__(self,parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(0)
        self.setTitle("Widgets")
        
        for text, slot in (
                ("Text", self.parent.addText),
                ("Button", self.parent.addBox),
                ("Sprite", self.parent.addPixmap),
                ("SpriteSheet", self.parent.addPixmap),
                ("&Align", None)):
            button = QPushButton(text,self)
            if eol != 2:
                button.setFocusPolicy(Qt.NoFocus)
            if slot is not None:
                button.clicked.connect(slot)
            '''
            if text == "&Align":
                menu = QMenu(self)
                for text, arg in (
                        ("Align &Left", Qt.AlignLeft),
                        ("Align &Right", Qt.AlignRight),
                        ("Align &Top", Qt.AlignTop),
                        ("Align &Bottom", Qt.AlignBottom)):
                    wrapper = functools.partial(self.setAlignment, arg)
                    self.wrapped.append(wrapper)
                    menu.addAction(text, wrapper)
                button.setMenu(menu)
            '''
            self.layout.addWidget(button)
        
class PropertyBar(QGroupBox):
    def __init__(self,parent):
        QGroupBox.__init__(self,parent)
        self.parent = parent
        self.setMaximumHeight(130)
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(10)
        self.setTitle("Property")
        
        lab1 = QLabel("Text: ")
        lab2 = QLabel("Font: ")
        lab3 = QLabel("Size: ")
        
        self.lab4 = QLabel("x: ")
        self.lab5 = QLabel("y: ")
        self.lab6 = QLabel(": ")
        
        self.led1 = QLineEdit()
        self.led2 = QFontComboBox()
        self.led3 = QComboBox()
        for i in range(1,50):
            self.led3.addItem(str(i))
        
        self.layout.addWidget(lab1)
        self.layout.addWidget(self.led1)
        self.layout.addWidget(lab2)
        self.layout.addWidget(self.led2)
        self.layout.addWidget(lab3)
        self.layout.addWidget(self.led3)
        self.layout.addWidget(self.lab4)
        self.layout.addWidget(self.lab5)
        self.layout.addWidget(self.lab6)
        
    def initText(self,item):
        text = item.toPlainText()
        font = item.font()
        size = item.font().pointSize()
        pos = item.pos().toPoint()
        z = item.zValue()
        self.led1.setText(text)
        self.led2.setFont(font)
        self.led3.setCurrentIndex(size)
        self.lab4.setText("x: "+str(pos.x()))
        self.lab5.setText("y: "+str(pos.y()))
        self.lab6.setText("z: "+str(z))
        
    def setPos(self,pos):
        self.lab4.setText("x: "+str(pos.x()))
        self.lab5.setText("y: "+str(pos.y()))
        
        
    def connectText(self,item):
        self.led1.textChanged.connect(item.setText)
        self.led2.currentFontChanged.connect(item.setFont)
        self.led3.currentIndexChanged.connect(item.setSize)
        self.connect(item, SIGNAL("move"), self.setPos)
        
    def disconnectText(self,item):
        self.led1.textChanged.disconnect(item.setText)
        self.led2.currentFontChanged.disconnect(item.setFont)
        self.led3.currentIndexChanged.disconnect(item.setSize)
        self.disconnect(item, SIGNAL("move"), self.setPos)
        
        

class LevelBar(QGroupBox):
    def __init__(self,parent):
        QGroupBox.__init__(self,parent)
        self.parent = parent
        self.setMaximumHeight(100)
        self.setMaximumWidth(300)
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(10)
        self.setTitle("Map")
        
        lab1 = QLabel("Size: ")
        lab2 = QLabel("Orientation: ")
        btn1 = QComboBox()
        btn1.addItem("320x240")
        btn1.addItem("480x320")
        btn1.addItem("640x480")
        btn1.addItem("720x480")
        btn1.addItem("800x480")
        btn1.addItem("852x480")
        btn1.addItem("960x540")
        btn2 = QComboBox()
        btn2.addItem("Portrait")
        btn2.addItem("Landscape")
        
        self.layout.addWidget(lab1)
        self.layout.addWidget(btn1)
        self.layout.addWidget(lab2)
        self.layout.addWidget(btn2)
        

        
class LevelToolBox(QFrame):
    def __init__(self,parent):
        QFrame.__init__(self,parent)
        self.parent = parent
        self.setMaximumHeight(100)
        self.setMaximumWidth(600)
        self.layout = QHBoxLayout(self)
        self.layout.setMargin(10)
        self.setFrameShape(QFrame.StyledPanel)
        
        btn1 = QPushButton("New",self)
        btn2 = QPushButton("Open",self)
        
        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.layout.addWidget(btn3)
        self.layout.addWidget(btn4)