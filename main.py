#!/usr/bin/env python
__author__ = "pyros2097"
__license__ = "GPLv3"
__copyright__ = 'Copyright (c) 2013, pyros2097'
__credits__ = ['pyros2097', 'eclipse']
__email__ = 'pyros2097@gmail.com'
"""
WARNING!!WARNING!!
Must not modify the main.py script which is embedded into the exe file 
This is to ensure that updating the software will always work.
Built on :
python 2.7.3
qt 4.8.2
pyqt 4.9.4
cxFreeze 4.3
py2app 0.6.4
sip
qscintilla 
"""

from PyQt4.QtGui import QApplication,QSplashScreen
from PyQt4.QtCore import Qt
import icons
app = QApplication([])
from globals import splash_pix
from mainwindow import MainWindow

'''
#currently 
list = QStyleFactory.keys()
    for i in list:
        print i
        
Windows
WindowsXP
Motif
CDE
Plastique
Cleanlooks
'''
def main():
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    #app.setStyle('Plastique')
    frame = MainWindow()
    frame.showMaximized()
    splash.finish(frame)
    frame.init()
    app.exec_()

if __name__ == "__main__":
    main()
    