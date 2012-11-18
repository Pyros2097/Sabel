from PyQt4.QtGui import (QTabWidget, QMenu, QDrag, QApplication,
                        QTabBar, QShortcut, QKeySequence, QWidget,
                        QHBoxLayout, QLabel, QPixmap, QScrollArea, 
                        QPalette, QColor)
from PyQt4.QtCore import (SIGNAL, Qt, QPoint, QMimeData, QRect,QByteArray,
                            QTimer, QPropertyAnimation,QEasingCurve)

from globals import ossep,ospathbasename,Icons, config

class MyTabBar(QTabBar):
    """ Tabs base class with enter, leave, drag, and drop support """
    def __init__(self,parent):
        QTabBar.__init__(self,parent)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        #self.setTabButton(QTabBar.ButtonPosition)
        #self.setShape(QTabBar.RoundedSouth)
        
    def mouseMoveEvent(self, event):
        if(self.tabAt(event.pos()) != -1):
            self.emit(SIGNAL("tabno"),self.tabAt(event.pos()))
        
    def enterEvent(self,event):
        self.emit(SIGNAL("enter"))

    def leaveEvent(self,event):
        self.emit(SIGNAL("leave"))
        

class EditorTab(QTabWidget):
    def __init__(self,parent):
        QTabWidget.__init__(self,parent)
        self.setTabBar(MyTabBar(self))
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore() 
                    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"), links)
        else:
            event.ignore()     
              
class TreeTab(QTabWidget):
    def __init__(self,parent):
        QTabWidget.__init__(self,parent)
        self.setTabBar(MyTabBar(self))
        
class OutputTab(QTabWidget):
    def __init__(self,parent):
        QTabWidget.__init__(self,parent)
        self.setTabBar(MyTabBar(self))
        self.setMaximumHeight(200)#260
        self.anim = QPropertyAnimation(self, "geometry")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QRect(0,0,100,0))
        self.anim.setEndValue(QRect(0,0,100,200))
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        if(config.hide() == 1):
            #self.setFixedHeight(200)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.close)
            #self.connect(self.tabBar(), SIGNAL("tabno"),self.pop_out)
            #self.connect(self.tabBar(), SIGNAL("enter"),self.enter_show)
            #self.connect(self.tabBar(), SIGNAL("leave"),self.leave_hide)
            self.hide()
        else:
            #self.setFixedHeight(200)
            self.hide()
        
    def pop_out(self,no):
        #print "Hover Over Output tab: ",no
        if(no != 2):
            self.setCurrentIndex(no)
        
    def enter_show(self):
        self.anim.start()
        self.show()
        
    def leave_hide(self):
        self.timer.start(2000)
        
    def close(self):
        #self.setFixedHeight(30)
        self.timer.stop()    
        
        