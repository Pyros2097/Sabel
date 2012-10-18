from PyQt4.QtCore import (QByteArray, QDataStream, QFile, QFileInfo,
        QIODevice, QPoint, QPointF, QRectF, QString, Qt, SIGNAL, QEvent)

from PyQt4.QtGui import (QCursor, QFileDialog, QFont,QGraphicsPixmapItem, 
        QGraphicsScene, QGraphicsView, QGridLayout,QHBoxLayout, 
        QLabel, QMatrix, QMessageBox, QPainter,
        QPen, QPixmap, QPrintDialog, QPrinter, QVBoxLayout, QFrame, 
        QBrush, QColor, QColorDialog, QGraphicsTextItem, QGraphicsPixmapItem)

import random
from bar import LevelBar
from grid import TileMapGrid
from globals import eol,Icons

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

Magicnumber = 0x2097
FileVersion = 1
Dirty = False

class LevelView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self,parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        #self.scale(0.99,0.99)


    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)
        self.scale(factor, factor)


class Level(QFrame):
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


        '''1.Header'''
        self.levelBar = LevelBar(self)
        
        '''3.Tiler'''
        self.tiler = TileMapGrid(self)#Tiler(self)
        self.tiler.setMinimumHeight(100)
        #self.tiler.currentChanged.connect(self.closeDesigner)
        #self.tiler.setTabsClosable(True)
        #self.tiler.setTabShape(0)
        #self.tiler.hide()
        #self.levelLayout.addWidget(self.levelBar) 
        
        '''2.view'''
        viewLayoutWidget = QFrame()
        viewLayoutWidget.setFrameShape(QFrame.StyledPanel)
        viewLayout = QHBoxLayout(viewLayoutWidget)
        #viewLayout.setMargin(10)
        self.view = LevelView(viewLayoutWidget)
        '''scene'''
        self.scene = QGraphicsScene(self)
        #self.scene.selectionChanged.connect(self.setConnect)
        #self.view.setStyleSheet("border: 1px solid red;")
        
        self.setBackgroundColor(self.bgColor)
        self.setScreenSize(self.screenSize)
        
        self.view.setScene(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        self.scroll_off = 1
        self.setScrollBar()
        
        viewLayout.setMargin(0)
        viewLayout.addWidget(self.view)

        self.wrapped = [] # Needed to keep wrappers alive
        layout = QVBoxLayout(self)
        layout.addWidget(self.levelBar)
        layout.addWidget(viewLayoutWidget)
        layout.addWidget(self.tiler)
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