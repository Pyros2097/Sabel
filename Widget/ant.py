from globals import ospathjoin,config
from PyQt4.QtGui import QWidget,QMessageBox
from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString,QTimer
from workthread import WorkThread

class Ant(QWidget):
    isRunning = False
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent 
        self.setAntList()
        self.ant_thread = WorkThread()
        self.timer = QTimer()
        #self.ant_thread = antThread()
        self.connect(self.ant_thread, SIGNAL("update"),self.update)
        self.connect(self.ant_thread, SIGNAL("fini"),self.newstart)
        self.connect(self.timer , SIGNAL('timeout()') , self.onTimeout)
        #self.connect(self.ant_thread , SIGNAL('started()') , self.onThreadStarted)
        #self.connect(self.ant_thread , SIGNAL('finished()'), self.onThreadFinished) 
        
    def onTimeout(self):
        print "timeout"
        
    def update(self,line):
        self.parent.textEdit.append(line)
        
    def setAntList(self):
        self.antlist = config.ant()
        self.cmd1 = self.antlist[0]
        self.cmd2 = self.antlist[1]
        self.cmd3 = self.antlist[2]
        self.cmd4 = self.antlist[3]
        self.cmd5 = self.antlist[4]
        
    def checkFinished(self,no,cmd):
        if(no == 0):
            #QMessageBox.about(self,"Error","Finished: "+cmd)
            self.parent.textEdit.append("Finished: "+cmd)
        else:
            self.parent.textEdit.append("Error: "+cmd)
        
    def newstart(self,no,cmd):
        self.checkFinished(no, cmd)
        self.parent.progressStop()
        self.parent.statusWriting()
           
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
        self.ant_thread.setCmd(self.cmd1+" "+prj.getPath())
        self.parent.progressStart()
        self.parent.statusCreating()
        self.ant_thread.run()
        
    def build(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Building Debug... "+ospathjoin(prj.getPath(),"build.xml"))
        self.ant_thread.setCmd(self.cmd2+" "+ospathjoin(prj.getPath(),"build.xml"))
        self.parent.progressStart()
        self.parent.statusBuilding()
        self.ant_thread.run()
        
    def clean(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Cleaning... "+prj.getPath())
        self.ant_thread.setCmd(self.cmd5+" "+ospathjoin(prj.getPath(),"build.xml"))
        self.parent.progressStart()
        self.parent.statusCleaning()
        self.ant_thread.run()
        
    def buildRun(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Ant Building and Installing... "+ospathjoin(prj.getPath(),"build.xml"))
        self.ant_thread.setCmd(self.cmd4+" "+ospathjoin(prj.getPath(),"build.xml"))
        self.parent.progressStart()
        self.ant_thread.run()
        
    def run(self,prj):
        if self.isRunning == False:
            self.isRunning = True
        self.showOutput()
        self.parent.textEdit.clear()
        self.parent.textEdit.append("Installing... "+prj.getPath())
        self.ant_thread.setCmd(self.cmd3+" "+ospathjoin(prj.getPath(),"build.xml"))
        self.parent.progressStart()
        self.parent.statusInstalling()
        self.ant_thread.run()
        
    def kill(self):
        self.ant_thread.kill_process()
        self.ant_thread.close_process()
        
    def close(self):
        self.ant_thread.kill_process()
        self.ant_thread.close_process()
        self.ant_thread.quit()