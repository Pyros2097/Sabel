from PyQt4.QtCore import Qt, SIGNAL, QEvent
from PyQt4.QtGui import QGraphicsItem, QGraphicsTextItem, QMatrix, QFont, QAction, QMenu
from globals import Icons

class TextItem(QGraphicsTextItem):
    def __init__(self, text, position, font=QFont("Times", 10), matrix=QMatrix()):
        QGraphicsTextItem.__init__(self,text)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setFont(font)
        self.setPos(position)
        self.setMatrix(matrix)
        self.connected = False

    def setConnected(self,bool):
        self.connected = bool
        
    def isConnected(self):
        return self.connected
        
    def itemChange(self, change, variant):
        if change != QGraphicsItem.ItemSelectedChange:
            global Dirty
            Dirty = True
        return QGraphicsTextItem.itemChange(self, change, variant)

    
    '''Solved static problem by calling base or super function'''
    def mousePressEvent(self, event):
        self.emit(SIGNAL("current"),self)
        QGraphicsTextItem.mousePressEvent(self,event)
        
    def mouseDoubleClickEvent(self,event):
        event.ignore()
        QGraphicsTextItem.mouseDoubleClickEvent(self,event)
        
    def mouseReleaseEvent(self, event):
        event.ignore()
        QGraphicsTextItem.mouseReleaseEvent(self,event)
    
    def mouseMoveEvent(self, event):
        self.emit(SIGNAL("move"),self.pos().toPoint())
        QGraphicsTextItem.mouseMoveEvent(self,event)
        
        
    def setText(self,text):
        self.setPlainText(text)
    def setSize(self,size):
        font = QFont(self.font().family(),int(size))
        self.setFont(font)
        
    def contextMenuEvent(self, event):
        menu = QMenu()
        copy = QAction(Icons.file_obj,'Copy',menu)
        cut = QAction(Icons.cut_edit,'Cut',menu)
        paste = QAction(Icons.paste_edit,'Paste',menu)
        delete = QAction(Icons.trash,'Delete',menu)
        copy.triggered.connect(self.copy)
        cut.triggered.connect(self.cut)
        paste.triggered.connect(self.paste)
        delete.triggered.connect(self.delete)
        menu.addAction(copy)
        menu.addAction(cut)
        menu.addAction(paste)
        menu.addSeparator()
        menu.addAction(delete)
        menu.exec_(event.screenPos())
        
    def copy(self):
        self.emit(SIGNAL("copy"),self)
    
    def cut(self):
        self.emit(SIGNAL("cut"),self)
    
    def paste(self):
        self.emit(SIGNAL("paste"),self)
    
    def delete(self):
        self.emit(SIGNAL("delete"),self)