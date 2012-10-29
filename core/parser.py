from globals import sqc
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import SIGNAL
from workthread import WorkThread


class Parser(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.par_thread = WorkThread()
        self.connect(self.par_thread, SIGNAL("update"),self.error)
        self.connect(self.par_thread, SIGNAL("fini"),self.stop)
        
    def error(self,text):
        '''Solved problem by adding Success to sqc file'''
        self.parent.errorTree.reset() 
        if(text != "" and text != "Success"):
            self.parent.popError()
            errorlist = text.split(',')
            fileName = self.parent.files[self.parent.tabWidget.currentIndex()]
            self.parent.errorTree.addError(fileName,errorlist)
            self.parent.tabWidget.currentWidget().reset()
            self.parent.tabWidget.currentWidget().addError(int(errorlist[0]))
        else:
            self.parent.tabWidget.currentWidget().reset()
            self.parent.errorTree.reset()
                
                
    def run(self,nfile):
        if(nfile.endswith(".nut")):
            self.par_thread.setCmd(sqc+" "+nfile)
            self.parent.statusParsing()
            self.parent.progressStart()
            self.par_thread.run()
            
    def stop(self):
        self.par_thread.close_process()
        self.parent.statusWriting()
        self.parent.progressStop()
        
    def close(self):
        self.par_thread.kill_process()
        self.par_thread.close_process()
        self.par_thread.quit()