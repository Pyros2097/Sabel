from globals import adblist,device,ospathjoin
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
        self.parent.textEdit.append("Finished")
        self.parent.textEdit.append(cmd)
        
    def showOutput(self):
        if(self.parent.tabWidget_3.isHidden()):
            self.parent.tabWidget_3.show()
            self.parent.tabWidget_3.setCurrentIndex(1)
        
    def create(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Creating... "+prj.getPath())
        self.adb_thread.setCmd("android.bat update project -p "+prj.getPath())
        self.adb_thread.run()
        
    def build(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Building Debug... "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.setCmd("ant.bat debug -buildfile "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.run()
        
    def clean(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Cleaning... "+prj.getPath())
        self.adb_thread.setCmd("ant.bat clean -buildfile "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.run()
        
    def buildRun(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Building and Installing... "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.setCmd("ant.bat debug install -buildfile "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.run()
        
    def run(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Installing... "+prj.getPath())
        self.adb_thread.setCmd("ant.bat install -buildfile "+ospathjoin(prj.getPath(),"build.xml"))
        self.adb_thread.run()
        
    def close(self):
        self.adb_thread.quit()