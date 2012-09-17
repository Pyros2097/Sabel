from nose.tools import eq_, ok_
from PyQt4.QtGui import QApplication,QSplashScreen
from PyQt4.QtCore import Qt
app = QApplication([])
import mainwindow
import icons
import sys
import os
from globals import config

path = os.getcwd()

class TestMainWindow:
    def __init__(self):
        self.frame = mainwindow.MainWindow()
        self.frame.showMaximized()
        self.frame.init()
        self.test_project()
        #self.test_file()
        #self.test_syntax()
        #self.test_openImage()
        #self.test_openAudio()
        #self.test_openEditor()
        sys.exit(app.exec_())
        
    def test_project(self):
        eq_(False,self.frame.treeWidget.createProject("C:/gg/gg/"))
        if not(self.frame.treeWidget.contains("C:/port/")):
            eq_(True,self.frame.treeWidget.createProject("C:/port/"))
        else:
            eq_(False,self.frame.treeWidget.createProject("C:/port/"))
         
    def test_file(self):
        eq_(False,self.frame.createTab("somefile.c"))
        eq_(False,self.frame.createTab(os.path.join(os.getcwd(),"cx.py")))
        
    def test_syntax(self):
        eq_(0,self.frame.syntax("somefile.py"))
        eq_(1,self.frame.syntax("somefile.c"))
        eq_(1,self.frame.syntax("somefile.cpp"))
        eq_(1,self.frame.syntax("somefile.h"))
        eq_(1,self.frame.syntax("somefile.hpp"))
        eq_(2,self.frame.syntax("somefile.nut"))
        eq_(2,self.frame.syntax("somefile.neko"))
        eq_(2,self.frame.syntax("somefile.lua"))
        
    def test_openImage(self):
        eq_(False,self.frame.openImage("somefile.png"))
        eq_(True,self.frame.openImage("C:/CODE/Sabel/Icons/sabel.png"))
        
    def test_openAudio(self):
        eq_(False,self.frame.openAudio("somefile.wav"))
        eq_(True,self.frame.openAudio("C:/CODE/Sabel/Test/title.wav"))
        
    def test_openEditor(self):
        eq_(False,self.frame.openEditor("somefile.nut"))
        eq_(True,self.frame.openEditor("C:/CODE/Sabel/Test/testMain.py"))
        