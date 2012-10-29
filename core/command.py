from PyQt4.QtGui import QWidget,QInputDialog
from PyQt4.QtCore import SIGNAL
from workthread import WorkThread

class Command(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.cmd = ""
        self.running = False
        self.cmdThread = WorkThread()
        self.connect(self.cmdThread, SIGNAL("update"),self.update)
        self.connect(self.cmdThread, SIGNAL("fini"),self.finished)
        
    def setCmd(self):
        text, ok = QInputDialog.getText(self, 'Run Command', 'Command:')
        self.cmd = str(text)
        if ok and self.cmd != "":
            self.parent.textEdit.clear()
            self.run()
            
    def setCmdLine(self):
        com = self.parent.combo.itemText(self.parent.combo.currentIndex())
        self.cmd = str(com+" "+self.parent.combo2.itemText(self.parent.combo2.currentIndex()))
        self.parent.textEdit.clear()
        self.run()
        
    def setCmdText(self,text):
        self.cmd = text
        if self.cmd != "":
            self.parent.textEdit.clear()
            self.run()
        
    def finished(self,no,cmd):
        self.parent.progressStop()
        self.parent.statusWriting()
        if(no == 0):
            self.parent.textEdit.append("Finished: "+cmd)
        else:
            self.parent.textEdit.append("Error: "+cmd)
        
    def update(self,line):
        self.parent.textEdit.append(line)
        self.parent.popOutput()


    def run(self):
        self.cmdThread.setCmd(self.cmd)
        self.parent.progressStart()
        self.parent.statusCommand()
        self.cmdThread.run()
        
    def close(self):
        self.cmdThread.quit()