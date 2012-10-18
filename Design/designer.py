from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import functools
import random
from PyQt4.QtCore import (QByteArray, QDataStream, QFile, QFileInfo,
        QIODevice, QPoint, QPointF, QRectF, QString, Qt, SIGNAL, QEvent)

from PyQt4.QtGui import (QCursor, QFileDialog, QFont,QGraphicsPixmapItem, 
        QGraphicsScene, QGraphicsView, QGridLayout,QHBoxLayout, 
        QLabel, QMatrix, QMessageBox, QPainter, QGraphicsItem,
        QPen, QPixmap, QPrintDialog, QPrinter, QVBoxLayout, QFrame, 
        QBrush, QColor, QColorDialog, QGraphicsTextItem, QGraphicsPixmapItem)

from bar import HeadingBar, WidgetsBar, PropertyBar
from text import TextItem
from button import BoxItem
from globals import eol,Icons, ospathexists

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

Magicnumber = 0x2097
FileVersion = 1
Dirty = False

class ScreenView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self,parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setAcceptDrops(True)
        self.setInteractive(True)
        #self.scale(0.99,0.99)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-item'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-item'):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore() 
                    
    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-item'):
            event.setDropAction(Qt.CopyAction)
            newText = event.mimeData().text()
            pos = event.pos()
            event.accept()
            #newText.replace("\\", "/")
            #print(newText)
            self.emit(SIGNAL("dropped"), newText, pos)
        else:
            event.ignore()
       
    def dragLeaveEvent(self, event):
        print("Item: dragLeaveEvent")
        event.ignore()
    

    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)
        self.scale(factor, factor)


class Screen(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self,parent)

        self.filename = QString()
        self.copiedItem = QByteArray()
        self.pasteOffset = 5
        self.prevPoint = QPoint()
        self.addOffset = 5
        
        self.screenSize = (320, 240)
        self.bgColor = QColor(244,244,244)
        '''0.Portrait 1.Landscape'''
        self.orientation = 0
        self.currentItem = None
        

        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageSize(QPrinter.Letter)


        '''Header'''
        self.headingBar = HeadingBar(self)
        '''WidgetsBar'''
        self.widgetsBar = WidgetsBar(self)
        '''Property'''
        self.propertyBar = PropertyBar(self)
        
        '''view'''
        viewLayoutWidget = QFrame()
        viewLayoutWidget.setFrameShape(QFrame.StyledPanel)
        viewLayout = QHBoxLayout(viewLayoutWidget)
        #viewLayout.setMargin(10)
        self.view = ScreenView(viewLayoutWidget)
        '''scene'''
        self.scene = QGraphicsScene(self)
        
        #self.scene.selectionChanged.connect(self.setConnect)
        #self.view.setStyleSheet("border: 1px solid red;")
        
        self.setBackgroundColor(self.bgColor)
        self.setScreenSize(self.screenSize)
        
        self.view.setScene(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        self.connect(self.view, SIGNAL("dropped"),self.addPixmapFile)
        self.scroll_off = 1
        self.setScrollBar()
        
        viewLayout.setMargin(0)
        viewLayout.addWidget(self.view)

        self.wrapped = [] # Needed to keep wrappers alive
        layout = QVBoxLayout(self)
        layout.addWidget(self.headingBar)
        layout.addWidget(viewLayoutWidget)
        layout.addWidget(self.widgetsBar)
        layout.addWidget(self.propertyBar)
        layout.setMargin(0)
        self.setLayout(layout)
        
    def setScrollBar(self):
        if(self.scroll_off):
            self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_off = 0
        else:
            self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_off = 1
        
    def setBackgroundColor(self,color):
        self.bgColor = color
        self.scene.setBackgroundBrush(QBrush(color))
        
    def setScreenSize(self,size):
        self.screenSize = size
        self.setOrientation(self.orientation)
        
    def setOrientation(self,idx):
        self.orientation = idx
        if(idx == 0):
            self.view.setMaximumSize(self.screenSize[1], self.screenSize[0])
            self.scene.setSceneRect(0, 0, self.screenSize[1], self.screenSize[0])
        else:
            self.view.setMaximumSize(self.screenSize[0], self.screenSize[1])
            self.scene.setSceneRect(0, 0, self.screenSize[0], self.screenSize[1])
        
    def offerSave(self):
        if (Dirty and QMessageBox.question(self,
                            "Designer - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No) == 
           QMessageBox.Yes):
            self.save()


    def position(self):
        point = self.mapFromGlobal(QCursor.pos())
        if not self.view.geometry().contains(point):
            coord = random.randint(36, 144)
            point = QPoint(coord, coord)
        else:
            if point == self.prevPoint:
                point += QPoint(self.addOffset, self.addOffset)
                self.addOffset += 5
            else:
                self.addOffset = 5
                self.prevPoint = point
        return self.view.mapToScene(point)
    
    def selectedItem(self):
        items = self.scene.selectedItems()
        if len(items) == 1:
            return items[0]
        return None
    
    def current(self,item):
        self.scene.clearSelection()
        sceneItems = self.scene.items()
        for items in sceneItems:
            if(items != item):
                item.setSelected(False)
                if(item.isConnected()):
                    self.propertyBar.disconnectText(item)
                    item.setConnected(False)
        self.currentItem = item
        self.currentItem.setConnected(True)
        self.currentItem.setSelected(True)
        self.propertyBar.connectText(self.currentItem)
        self.propertyBar.initText(self.currentItem)


    def addText(self):
        item = TextItem("SomeText", self.position())
        self.connect(item, SIGNAL("current"),self.current)
        self.connect(item, SIGNAL("copy"),self.copy)
        self.connect(item, SIGNAL("cut"),self.cut)
        self.connect(item, SIGNAL("paste"),self.paste)
        self.connect(item, SIGNAL("delete"),self.delete)
        #self.current(item)
        self.scene.addItem(item)
        
    def addBox(self):
        btn = BoxItem(self.position())
        self.scene.clearSelection()
        self.scene.addItem(btn)
        
    def addPixmapFile(self,nfile, pos): 
        if(nfile.isEmpty()):
            return
        else:
            #print(nfile)
            if(ospathexists(nfile)):
                self.createPixmapItem(QPixmap(nfile),self.view.mapToScene(pos))#self.position())

    def addPixmap(self):
        path = (QFileInfo(self.filename).path() if not self.filename.isEmpty() else ".")
        fname = QFileDialog.getOpenFileName(self, "Designer - Add Image", path,"Pixmap Files (*.png)")
        if fname.isEmpty():
            return
        self.createPixmapItem(QPixmap(fname), self.position())
        

    def createPixmapItem(self, pixmap, position, matrix=QMatrix()):
        item = QGraphicsPixmapItem(pixmap)
        item.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable)
        item.setPos(position)
        item.setMatrix(matrix)
        self.scene.clearSelection()
        self.scene.addItem(item)
        item.setSelected(True)

    def copy(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copiedItem.clear()
        self.pasteOffset = 5
        stream = QDataStream(self.copiedItem, QIODevice.WriteOnly)
        self.writeItemToStream(stream, item)


    def cut(self):
        item = self.selectedItem()
        if item is None:
            return
        self.copy()
        self.scene.removeItem(item)
        del item


    def paste(self):
        if self.copiedItem.isEmpty():
            return
        stream = QDataStream(self.copiedItem, QIODevice.ReadOnly)
        item = self.readItemFromStream(stream, self.pasteOffset)
        self.pasteOffset += 5
        #self.scene.addItem(item)
        
    def delete(self):
        items = self.scene.selectedItems()
        if (len(items) and QMessageBox.question(self,
                "Designer - Delete",
                "Delete {0} item{1}?".format(len(items),
                "s" if len(items) != 1 else ""),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
                
    def readItemFromStream(self, stream, offset=0):
        type = QString()
        position = QPointF()
        matrix = QMatrix()
        stream >> type >> position >> matrix
        if offset:
            position += QPointF(offset, offset)
        if type == "Text":
            text = QString()
            font = QFont()
            stream >> text >> font
            self.scene.addItem(TextItem(text, position, font, matrix))
        elif type == "Box":
            rect = QRectF()
            stream >> rect
            style = Qt.PenStyle(stream.readInt16())
            self.scene.addItem(BoxItem(position, style, matrix))
        elif type == "Pixmap":
            pixmap = QPixmap()
            stream >> pixmap
            self.scene.addItem(self.createPixmapItem(pixmap, position, matrix))


    def writeItemToStream(self, stream, item):
        if isinstance(item, QGraphicsTextItem):
            stream << QString("Text") << item.pos() \
                   << item.matrix() << item.toPlainText() << item.font()
        elif isinstance(item, QGraphicsPixmapItem):
            stream << QString("Pixmap") << item.pos() \
                   << item.matrix() << item.pixmap()
        elif isinstance(item, BoxItem):
            stream << QString("Box") << item.pos() \
                   << item.matrix() << item.rect
            stream.writeInt16(item.style)


    def setAlignment(self, alignment):
        # Items are returned in arbitrary order
        items = self.scene.selectedItems()
        if len(items) <= 1:
            return
        # Gather coordinate data
        leftXs, rightXs, topYs, bottomYs = [], [], [], []
        for item in items:
            rect = item.sceneBoundingRect()
            leftXs.append(rect.x())
            rightXs.append(rect.x() + rect.width())
            topYs.append(rect.y())
            bottomYs.append(rect.y() + rect.height())
        # Perform alignment
        if alignment == Qt.AlignLeft:
            xAlignment = min(leftXs)
            for i, item in enumerate(items):
                item.moveBy(xAlignment - leftXs[i], 0)
        elif alignment == Qt.AlignRight:
            xAlignment = max(rightXs)
            for i, item in enumerate(items):
                item.moveBy(xAlignment - rightXs[i], 0)
        elif alignment == Qt.AlignTop:
            yAlignment = min(topYs)
            for i, item in enumerate(items):
                item.moveBy(0, yAlignment - topYs[i])
        elif alignment == Qt.AlignBottom:
            yAlignment = max(bottomYs)
            for i, item in enumerate(items):
                item.moveBy(0, yAlignment - bottomYs[i])
        global Dirty
        Dirty = True


    def rotate(self):
        for item in self.scene.selectedItems():
            item.rotate(30)


    def print_(self):
        dialog = QPrintDialog(self.printer)
        if dialog.exec_():
            painter = QPainter(self.printer)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)
            self.scene.clearSelection()
            #self.removeBorders()
            self.scene.render(painter)
            #self.addBorders()


    def open(self):
        self.offerSave()
        path = (QFileInfo(self.filename).path()
                if not self.filename.isEmpty() else ".")
        fname = QFileDialog.getOpenFileName(self,
                "Page Designer - Open", path,
                "Page Designer Files (*.pgd)")
        if fname.isEmpty():
            return
        self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            items = self.scene.items()
            while items:
                item = items.pop()
                self.scene.removeItem(item)
                del item
            self.addBorders()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_4_2)
            magic = stream.readInt32()
            if magic != MagicNumber:
                raise IOError, "not a valid .pgd file"
            fileVersion = stream.readInt16()
            if fileVersion != FileVersion:
                raise IOError, "unrecognised .pgd file version"
            while not fh.atEnd():
                self.readItemFromStream(stream)
        except IOError, e:
            QMessageBox.warning(self, "Page Designer -- Open Error",
                    "Failed to open {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False


    def save(self):
        if self.filename.isEmpty():
            path = "."
            fname = QFileDialog.getSaveFileName(self,
                    "Page Designer - Save As", path,
                    "Page Designer Files (*.pgd)")
            if fname.isEmpty():
                return
            self.filename = fname
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            self.scene.clearSelection()
            stream = QDataStream(fh)
            stream.setVersion(QDataStream.Qt_4_2)
            stream.writeInt32(MagicNumber)
            stream.writeInt16(FileVersion)
            for item in self.scene.items():
                self.writeItemToStream(stream, item)
        except IOError, e:
            QMessageBox.warning(self, "Page Designer -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        global Dirty
        Dirty = False