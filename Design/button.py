from PyQt4.QtCore import Qt, SIGNAL,QRectF
from PyQt4.QtGui import (QGraphicsItem, QGraphicsTextItem, QMatrix, QFont, QAction, 
                         QMenu, QPen, QStyle)

PointSize = 10

class BoxItem(QGraphicsItem):
    def __init__(self, position, style=Qt.SolidLine, matrix=QMatrix()):
        QGraphicsItem.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemIsFocusable)
        self.rect = QRectF(-10 * PointSize, -PointSize, 20 * PointSize,2 * PointSize)
        self.style = style
        self.setPos(position)
        self.setMatrix(matrix)
        self.setFocus()


    def parentWidget(self):
        return self.scene().views()[0]


    def boundingRect(self):
        return self.rect.adjusted(-2, -2, 2, 2)


    def paint(self, painter, option, widget):
        pen = QPen(self.style)
        pen.setColor(Qt.black)
        pen.setWidth(1)
        if option.state & QStyle.State_Selected:
            pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawRect(self.rect)


    def itemChange(self, change, variant):
        if change != QGraphicsItem.ItemSelectedChange:
            global Dirty
            Dirty = True
        return QGraphicsItem.itemChange(self, change, variant)

    def contextMenuEvent(self, event):
        menu = QMenu()
        copy = QAction(Icons.file_obj,'Copy',menu)
        cut = QAction(Icons.cut_edit,'Cut',menu)
        paste = QAction(Icons.paste_edit,'Paste',menu)
        delete = QAction(Icons.trash,'Delete',menu)
        menu.addAction(copy)
        menu.addAction(cut)
        menu.addAction(paste)
        menu.addSeparator()
        menu.addAction(delete)
        menu.exec_(event.screenPos())
    '''
    def contextMenuEvent(self, event):
        wrapped = []
        menu = QMenu(self.parentWidget())
        for text, param in (
                ("&Solid", Qt.SolidLine),
                ("&Dashed", Qt.DashLine),
                ("D&otted", Qt.DotLine),
                ("D&ashDotted", Qt.DashDotLine),
                ("DashDo&tDotted", Qt.DashDotDotLine)):
            wrapper = functools.partial(self.setStyle, param)
            wrapped.append(wrapper)
            menu.addAction(text, wrapper)
        menu.exec_(event.screenPos())
    '''

    def setStyle(self, style):
        self.style = style
        self.update()

    def keyPressEvent(self, event):
        factor = PointSize / 4
        changed = False
        if event.modifiers() & Qt.ShiftModifier:
            if event.key() == Qt.Key_Left:
                self.rect.setRight(self.rect.right() - factor)
                changed = True
            elif event.key() == Qt.Key_Right:
                self.rect.setRight(self.rect.right() + factor)
                changed = True
            elif event.key() == Qt.Key_Up:
                self.rect.setBottom(self.rect.bottom() - factor)
                changed = True
            elif event.key() == Qt.Key_Down:
                self.rect.setBottom(self.rect.bottom() + factor)
                changed = True
        if changed:
            self.update()
            global Dirty
            Dirty = True
        else:
            QGraphicsItem.keyPressEvent(self, event)
