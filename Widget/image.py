from PyQt4.QtGui import  QColor,QPalette,QLabel,QDialog,QPixmap,QScrollArea,QVBoxLayout

class Image(QDialog):
    def __init__(self,parent,nfile):
        QDialog.__init__(self,parent)
        tab = QLabel()
        pal = QPalette(self.palette())
        bgcolor = QColor("#ffffff")
        pal.setColor(QPalette.Background,bgcolor)
        tab.setPalette(pal)
        if nfile == "":
            return
        pix = QPixmap(nfile)
        tab.setPixmap(pix)
        scrollArea = QScrollArea()
        scrollArea.setWidget(tab)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(scrollArea)
        self.setLayout(mainLayout)
        self.resize(pix.width()+25, pix.height()+25)