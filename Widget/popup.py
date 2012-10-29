from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Popup(QWidget):
    def __init__(self,  parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.Tool| Qt.X11BypassWindowManagerHint  | Qt.FramelessWindowHint)
        #self.setFrameStyle(QFrame.Box| QFrame.Plain)
        r = QApplication.desktop().geometry()
        self.setGeometry(QRect(r.right() - 290,r.bottom() - 230,300,50))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.anim = QPropertyAnimation(self, "geometry")
        self.anim.setDuration(300)
        
        ''' X ,Y position of Widget 
            W ,H of the widget '''
        self.anim.setStartValue(QRect(r.right() - 290,r.bottom() - 230,300,50))
        self.anim.setEndValue(QRect(r.right() - 290,r.bottom() - 200,300,150))
        #, 
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        #self.layoutWidget = QWidget()
        #self.layoutWidget.setGeometry(QRect(r.right() - 290,r.bottom() - 200,300,150))
        self.vb = QVBoxLayout()
        self.vb.setMargin(8)
        self.vb.setSpacing(0)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignLeft)
        #self.label.setGeometry(QRect(r.right() - 290,r.bottom() - 200,100,100))
        #self.label.setGeometry(0, 0, 300,150)
        self.label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.label.setOpenExternalLinks(True)
        self.btn = QPushButton()
        self.btn.setText("Start")
        self.btn.clicked.connect(self.start)
        self.vb.addWidget(self.label)
        #self.vb.addWidget(self.layoutWidget)
        self.vb.addWidget(self.btn)
        self.setLayout(self.vb)
        
    def start(self):
        self.emit(SIGNAL("download"))
        self.hide()
        
    def hideBtn(self):
        self.btn.hide()
    def showBtn(self):
        if(self.btn.isHidden()):
            self.btn.show()
        
    def showPopup(self):
        self.anim.start()
        self.show()
        
    def setInfo(self, info):
        text = "<b><u>Update</u></b>: "+"v"
        #print text
        for i in info:
            text = text + str(i) + "<br>"
        text = text + "<br><b>Check Out</b>:    <br><a href='http://code.google.com/p/sabel-ide/'>Sabel</a>" + "<br>"
        self.label.setText(text)
        
    def mousePressEvent(self, e):
        geom = self.geometry()
        pos = e.pos()
        pos = self.mapToParent(pos)
        #print pos
        if(geom.contains(pos)):
            self.hide()
            self.emit(SIGNAL("cancel"))