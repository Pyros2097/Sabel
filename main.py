#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__copyright__ = 'Copyright (c) 2012, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'
__version__ = "0.57"
#TODO:
#Must learn to destroy editor completely because memory keeps increasing
#when close tab occurs

from PyQt4.QtGui import QApplication,QSplashScreen
from PyQt4.QtCore import Qt
import icons
app = QApplication([])
from globals import splash_pix
from mainwindow import MainWindow

def main():
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    frame.init()
    app.exec_()

if __name__ == "__main__":
    main()