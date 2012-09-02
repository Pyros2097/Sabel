from globals import adblist,device
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString,QTimer
from workthread import WorkThread

class Ant(QWidget):
    isRunning = False
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent 
        self.adb_thread = WorkThread()
        self.timer = QTimer()
        self.device = device
        #self.adb_thread = AdbThread()
        self.connect(self.adb_thread, SIGNAL("update"),self.update)
        self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        #self.connect(self.timer , SIGNAL('timeout()') , self.onTimeout)
        #self.connect(self.adb_thread , SIGNAL('started()') , self.onThreadStarted)
        #self.connect(self.adb_thread , SIGNAL('finished()'), self.onThreadFinished) 
        
    def onTimeout(self):
        print "timeout"
        """
        # Update the progress bar
        value = self.pbar.value()
        # Going forward or backwards?
        if self.pbar.invertedAppearance():
            if value-2 < self.pbar.minimum():
                self.pbar.setValue(self.pbar.minimum())
                self.pbar.setInvertedAppearance(False)
            else:
                self.pbar.setValue(value-2)
        else:
            if value+2 > self.pbar.maximum():
                self.pbar.setValue(self.pbar.maximum())
                self.pbar.setInvertedAppearance(True)
            else:
                self.pbar.setValue(value+2)
        """
        
    def onThreadStarted(self):
        print "Thread has been started"
        self.timer.start(10)
        #self.enableButtons(False)
 
    def onThreadFinished(self):
        print "Thread has finished"
        self.timer.stop()
        #self.enableButtons(True)
        #self.pbar.setValue(0)
        
    def update(self,line):
        self.parent.textEdit.append(line)
        
    def newstart(self,no,cmd):
        print "finished"
        
        
    def create(self):
        if self.isRunning == False:
            self.isRunning = True
        self.parent.textEdit.append("Building..")
        self.adb_thread.setCmd("android update project -p "+prj)
        self.adb_thread.run()
        
    def build(self):
        if self.isRunning == False:
            self.isRunning = True
        self.parent.textEdit.append("Building..")
        self.adb_thread.setCmd("ant debug "+prj)
        self.adb_thread.run()
        
    def clean(self):
        if self.isRunning == False:
            self.isRunning = True
        self.parent.textEdit.append("Building..")
        self.adb_thread.setCmd("ant clean "+prj)
        self.adb_thread.run()
        
    def buildRun(self):
        if self.isRunning == False:
            self.isRunning = True
        self.parent.textEdit.append("Building..")
        self.adb_thread.setCmd("ant debug install "+prj)
        self.adb_thread.run()
        
    def close(self):
        self.adb_thread.quit()