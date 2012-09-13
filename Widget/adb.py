from globals import config
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString,QTimer
from workthread import WorkThread

class Adb(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.isRunning = False
        self.adb_thread = WorkThread()
        self.timer = QTimer()
        self.device = config.device()
        self.adblist = config.adb()
        #self.adb_thread = AdbThread()
        self.connect(self.adb_thread, SIGNAL("update"),self.update)
        self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        #self.connect(self.timer , SIGNAL('timeout()') , self.onTimeout)
        #self.connect(self.adb_thread , SIGNAL('started()') , self.onThreadStarted)
        #self.connect(self.adb_thread , SIGNAL('finished()'), self.onThreadFinished)
        self.cmd1 = "adb -d push "+self.adblist[0]
        self.cmd2 = "adb -d shell am start -a android.intent.action.MAIN -n "+self.adblist[1]
        self.cmd3 = "adb -d logcat -s "+self.adblist[2]
        self.cmd4 = "adb -d shell pm disable com.emo_framework.examples"
        self.cmd5 = "adb -d shell pm enable com.emo_framework.examples"
        
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
        
    def checkFinished(self,no,cmd):
        if(no == 0):
            self.parent.textEdit.append("Finshed: "+cmd)
        else:
            self.parent.textEdit.append("Error Canceled: "+cmd)
        
    def newstart(self,no,cmd):
        self.checkFinished(no, cmd)
        if(cmd == self.cmd1):
            self.adb_thread.setCmd(self.cmd2)
            self.adb_thread.run()
        elif(cmd == self.cmd2):
            self.adb_thread.setCmd(self.cmd3)
            self.adb_thread.run2()
        elif(cmd == self.cmd3):
            self.adb_thread.setCmd(self.cmd4)
            self.adb_thread.run()
        elif(cmd == self.cmd4):
            self.adb_thread.setCmd(self.cmd5)
            self.adb_thread.run()   
        
    def run(self):
        if self.isRunning == False:
            self.isRunning = True
            self.parent.toolBar.action_Run.setDisabled(True)
            self.parent.toolBar.action_Stop.setEnabled(True)        
            if(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.show()
                self.parent.tabWidget_3.setCurrentIndex(1)
            self.parent.textEdit.clear()
        self.parent.textEdit.append("Pushing main.nut...\n")
        self.adb_thread.setCmd(self.cmd1)
        self.adb_thread.run()
        

    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            self.parent.toolBar.action_Stop.setDisabled(True)
            self.parent.textEdit.append("Stopped.")
            if not(self.parent.tabWidget_3.isHidden()):
                self.parent.tabWidget_3.hide()
            self.parent.toolBar.action_Run.setEnabled(True)
            self.adb_thread.close_process()
            #"adb -d shell ps | grep "+adblist[3]+" | awk '{print $2}' | xargs adbshell kill")
            #adb -d shell ps | grep com.emo_framework.examples | awk '{print $2}' | xargs adb shell kill
            #adb -d shell kill adb shell ps | grep com.emo_framework.examples | awk '{print $2}'

              
    def close(self):
        self.adb_thread.kill_process()
        self.adb_thread.close_process()
        self.adb_thread.quit()