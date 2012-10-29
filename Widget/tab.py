from PyQt4.QtGui import (QTabWidget, QMenu, QDrag, QApplication,
                        QTabBar, QShortcut, QKeySequence, QWidget,
                        QHBoxLayout, QLabel, QPixmap, QScrollArea, 
                        QPalette, QColor)
from PyQt4.QtCore import SIGNAL, Qt, QPoint, QMimeData, QByteArray

from globals import ossep,ospathbasename,Icons

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
            print self.tabAt(event.pos())
        
    def enterEvent(self,event):
        print("Enter")
        #self.setStyleSheet("background-color:#45b545;")

    def leaveEvent(self,event):
        #self.setStyleSheet("background-color:yellow;")
        print("Leave")

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