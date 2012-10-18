from PyQt4.QtGui import QWidget, QGridLayout, QPushButton, QLabel, QTabWidget, QPixmap
from PyQt4.QtGui import QScrollArea


class TileMapGrid(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.layout = QGridLayout(self)
        self.buttons = {}
        for i in range(10):
            for j in range(10):
                # keep a reference to the buttons
                self.buttons[(i, j)] = QPushButton('row %d, col %d' % (i, j))
                # add to the layout
                self.layout.addWidget(self.buttons[(i, j)], i, j)

        self.setLayout(self.layout)
        
class Tiler(QTabWidget):
    Count = 0
    def __init__(self,parent):
        QTabWidget.__init__(self,parent)
        self.tabCloseRequested.connect(self.closeTab)
        self.setAcceptDrops(True)
        #self.connect(self.tabBar(), SIGNAL("dropped"), self.addItem)
        
        
    def addImage(self,nfile):
        #widgetLayout = QHBoxLayout()
        tab = QLabel()
        pal = QPalette(self.palette())
        pal.setColor(QPalette.Background,QColor("#ffffff"))
        tab.setPalette(pal)
        tab.setPixmap(QPixmap(nfile))
        #widgetLayout.addWidget(tab)           
        #widget.setLayout(widgetLayout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(tab)
        #dialogLayout = QVBoxLayout()
        #dialogLayout.addWidget(scrollArea)    
        #self.setLayout(dialogLayout)
        self.addTab(scrollArea, ospathbasename(nfile))
        self.setCurrentIndex(self.Count)
        self.Count+=1
        
    def closeTab(self,index):
        self.removeTab(index)
        self.Count-=1
    
    def hideTiler(self):
        self.tiler.setCurrentIndex(0)
        self.tiler.hide()
        #if(self.currentIndex() == self.indexOf(self.cornerWidget())):
        #    return True  