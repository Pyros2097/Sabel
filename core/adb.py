from globals import config
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal,SIGNAL,QThread,QProcess,QString,QTimer
from workthread import WorkThread

class Adb(QWidget):
    isRunning = False
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.adb_thread = WorkThread()
        self.adblist = config.adb()
        self.device = ""
        self.setDevice()
        #self.adb_thread = AdbThread()
        self.connect(self.adb_thread, SIGNAL("update"),self.update)
        self.connect(self.adb_thread, SIGNAL("fini"),self.newstart)
        #self.connect(self.timer , SIGNAL('timeout()') , self.onTimeout)
        
    def setDevice(self):
        if(config.device() == 1):
            self.device = " -d "
        else:
            self.device = " -e "
        self.cmd1 = "adb"+self.device+"push "+self.adblist[0]
        self.cmd2 = "adb"+self.device+"shell am start -a android.intent.action.MAIN -n "+self.adblist[1]
        self.cmd3 = "adb"+self.device+"logcat -s "+self.adblist[2]
        self.cmd4 = "adb"+self.device+"shell pm disable com.emo_framework.examples"
        self.cmd5 = "adb"+self.device+"shell pm enable com.emo_framework.examples"
    
    def setAdbList(self):
        self.adblist = config.adb()
        self.cmd1 = "adb"+self.device+"push "+self.adblist[0]
        self.cmd2 = "adb"+self.device+"shell am start -a android.intent.action.MAIN -n "+self.adblist[1]
        self.cmd3 = "adb"+self.device+"logcat -s "+self.adblist[2]
        self.cmd4 = "adb"+self.device+"shell pm disable com.emo_framework.examples"
        self.cmd5 = "adb"+self.device+"shell pm enable com.emo_framework.examples"
        
    def update(self,line):
        self.parent.textEdit.append(line)
        self.parent.popOutput()
        
    def checkFinished(self,no,cmd):
        self.parent.progressStop()
        if(no == 0):
            self.parent.textEdit.append("Finished: "+cmd)
        else:
            self.parent.textEdit.append("Error: "+cmd)
        
    def newstart(self,no,cmd):
        self.checkFinished(no, cmd)
        self.parent.progressStart()
        if(cmd == self.cmd1): 
            self.adb_thread.setCmd(self.cmd2) #start
            self.adb_thread.run()
        elif(cmd == self.cmd2): 
            self.adb_thread.setCmd(self.cmd3) #log
            self.parent.progressStop()
            self.adb_thread.run2()
        elif(cmd == self.cmd3): 
            self.adb_thread.setCmd(self.cmd4) #enable app
            self.adb_thread.run()
        elif(cmd == self.cmd4):  
            self.adb_thread.setCmd(self.cmd5)  #disable app
            self.adb_thread.run()
        elif(cmd == self.cmd5): 
            if not(self.parent.outputTabWidget.isHidden()):
                self.parent.outputTabWidget.hide()
            self.parent.toolBar.action_Run.setEnabled(True)
            self.parent.statusWriting()
            #self.stop()
        
    def run(self):
        if self.isRunning == False:
            self.isRunning = True
            self.parent.toolBar.action_Run.setDisabled(True)
            self.parent.toolBar.action_Stop.setEnabled(True)        
            self.parent.popOutput()
            self.parent.textEdit.clear()
            self.parent.textEdit.append("Pushing main.nut...\n")
            self.adb_thread.setCmd(self.cmd1)
            self.parent.statusRunning()
            self.parent.progressStart()
            self.adb_thread.run()      

    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            self.parent.toolBar.action_Stop.setDisabled(True)
            self.parent.textEdit.append("Stopped.")
            self.parent.statusStopping()
            self.adb_thread.close_process()
            #"adb -d shell ps | grep "+adblist[3]+" | awk '{print $2}' | xargs adbshell kill")
            #adb -d shell ps | grep com.emo_framework.examples | awk '{print $2}' | xargs adb shell kill
            #adb -d shell kill adb shell ps | grep com.emo_framework.examples | awk '{print $2}'

              
    def close(self):
        self.adb_thread.kill_process()
        self.adb_thread.close_process()
        self.adb_thread.quit()