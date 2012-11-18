import urllib2
from PyQt4.QtGui import QLabel, QMessageBox, QWidget, QDialog, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt4.QtCore import SIGNAL, QThread, QString, QTimer
from globals import error, Icons, __version__, osrename, ospathdirname ,ospathjoin, ospathexists, recycle
from subprocess import Popen, STARTUPINFO, SW_HIDE

"""
We Can update the software by following these steps:
1.Check if net connecetion is there
2.Download the update.txt text which contains any version changes
3.If a new version is there it will ask to download and then starts downloading
  library.zip as library.zip_2097 after it completes it renames this file
4.If no version changes is there then it will just show no updates
5.If download is incomplete or terminated nothing happens since original file is intact
"""
class Updater(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent = parent
        self.downThread = DownThread()
        self.prog = ProgressDialog(self)
        self.firstStartUp = 0
        self.connect(self.downThread, SIGNAL("net"),self.net)
        self.connect(self.downThread, SIGNAL("timed"),self.timed)
        self.connect(self.downThread, SIGNAL("cant"),self.cant)
        self.connect(self.downThread, SIGNAL("stop"),self.stop)
        self.connect(self.downThread, SIGNAL("progress"),self.show_prog)
        self.connect(self.downThread, SIGNAL("status"),self.status)
        self.connect(self.downThread, SIGNAL("text"),self.showPop)
        self.connect(self.downThread, SIGNAL("updated"),self.updated)
        self.connect(self.prog, SIGNAL("forceStop"),self.forceStop)
        self.connect(self.parent.popWidget,SIGNAL("download"),self.OK)
        self.connect(self.parent.popWidget,SIGNAL("cancel"),self.NotOK)
        
    def updated(self):
        done = False
        self.prog.accept()
        info = STARTUPINFO()
        info.dwFlags |= SW_HIDE
        reply = QMessageBox.question(self,
                    "Sabel IDE",
                    "You have to restart for changes to take place.\nRestart Now?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.No:
            done = False
        elif reply == QMessageBox.Yes:
            done = True
            self.parent.fileSaveAll()
        if(done):
            proc = Popen("Sabel.exe",startupinfo = info)
            self.parent.kill()
        
        
    def start(self):
        print "starting updater"
        self.downThread.setOK(0) #everytime we check for update the while should wait otherwise thread exits default
        self.downThread.start()
        
    def OK(self):
        self.downThread.setOK(1)
        
    def NotOK(self):
        self.downThread.setOK(2)
        
    def showPop(self,text):
        if(text == []):
            self.retry()
            return
        if(text[0] > __version__): #If the update version is greater than current
            self.parent.popWidget.setInfo(text)
            self.parent.popWidget.showPopup()
            self.parent.popWidget.showBtn()
        else:
            ''' This is to trigger checking on startup if no update dont show 
                otherwise can be nagging on every startup '''
            if(self.firstStartUp != 0):
                self.parent.popWidget.setInfo([__version__,"<br> Currently No Update "])
                self.parent.popWidget.hideBtn()
                self.parent.popWidget.showPopup()
            else:
                self.firstStartUp = 1
                self.NotOK() #thread should exit if no update is present
            
        
    def retry(self):
        QMessageBox.about(self,"Error",'Cant Read repository Retry')
        error('Update: Cant Read repository Retry')
    def net(self):
        QMessageBox.about(self,"Error",'Net Connection Not Found')
        error('Update: Net Connection Not Found')
    def timed(self):
        QMessageBox.about(self,"Error",'Connection Timed Out')
        error('Update: Timed out')
    def cant(self):
        QMessageBox.about(self,"Error",'File Cant be downloaded')
        error('Update: File Cant be downloaded')
    def stop(self):
        QMessageBox.about(self,"Error",'Stopped / Net Connection Lost')
        error('Update: Stopped / Net Connection Lost')
        
    def show_prog(self):
        self.prog.exec_()
        
    def status(self,val):
        self.prog.setValue(int(val))
        
    def forceStop(self):
        print "Thread ForceStopping"
        self.prog.accept()
        self.downThread.forceStop()
        
class ProgressDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.resize(300, 75)
        self.setWindowTitle("Updating")
        self.vw = QWidget(self)
        self.vl = QVBoxLayout(self.vw)
        self.vl.setMargin(10)
        self.label = QLabel(self.vw)
        self.label.setText("<b>Downloading:</b> library.zip")
        self.vl.addWidget(self.label)
        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.progressbar = QProgressBar(self.horizontalLayoutWidget)
        self.progressbar.setFixedWidth(260)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.stopButton = QPushButton(self.horizontalLayoutWidget)
        self.stopButton.setFlat(True)
        self.stopButton.setIcon(Icons.stop)
        self.stopButton.setFixedSize(16,16)
        self.horizontalLayout.addWidget(self.progressbar)
        self.horizontalLayout.addWidget(self.stopButton)
        self.vl.addWidget(self.horizontalLayoutWidget)
        self.stopButton.clicked.connect(self.forceStop)
        
    def setValue(self,val):
        self.progressbar.setValue(val)
    def forceStop(self):
        self.emit(SIGNAL("forceStop"))
        
class DownThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.ok = 0
        self.running = True
        
    def start(self):
        QThread.start(self)
        self.running = True
        
    def forceStop(self):
        self.running = False
        
    def setOK(self, val):
        self.ok = val
        
    def run(self):
        print "Checking Net"
        if(self.internet_on()):
            print "Checking version"
            text = self.check()
            self.emit(SIGNAL("text"),text)
            while self.ok == 0:
                pass
            if(self.ok ==1):
                print "Thread Downloading"
                self.download() #pushbutton accepted
            else:
                self.forceStop() #canceled
                print "Thread Exiting"
        #self.exec_()
        
    def internet_on(self):
        try:
            response = urllib2.urlopen('http://74.125.113.99', timeout=2)
            return True
        except urllib2.URLError as err:
            self.emit(SIGNAL("net"))    
        except:
            self.emit(SIGNAL("timed"))    
        return False 
    
    def check(self):
        url = 'https://raw.github.com/Pyros2097/Sabel/master/update.txt'
        try:
            u = urllib2.urlopen(url)
            lines = u.read()
            lines = lines.splitlines()
            #print lines
            return lines
        except:
            return []
        
    ''' maybe be put this into an entire while self.running loop to allow updates after forceStop'''
    def download(self):
        self.emit(SIGNAL("progress"))
        url = 'https://raw.github.com/Pyros2097/Sabel/master/build/exe.win32-2.7/library.zip'
        file_name = url.split('/')[-1]
        try:
            u = urllib2.urlopen(url)
            f = open(file_name+"_2097", 'wb')
            meta = u.info()
            file_size = int(meta.getheaders('Content-Length')[0])
            #print 'Downloading: %s Bytes: %s' % (file_name, file_size)
            file_size_dl = 0
            block_sz = 8192
            while self.running:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                status = file_size_dl * 100.0 / file_size
                self.emit(SIGNAL("status"),status)
            ''' The file library.zip is never used the library 
                is once loaded into the vm so no need to delete it '''
            f.close()
            if(self.running): #to prevent it from executing this code if terminated
                if(ospathexists(file_name)):
                    recycle(file_name) # deletes library.zip
                osrename(file_name+"_2097",ospathjoin(ospathdirname(file_name+"_2097"),"library.zip"))
                self.emit(SIGNAL("updated"))
                
        except urllib2.URLError as err:
            self.emit(SIGNAL("cant"))
        except:
            self.emit(SIGNAL("stop"))
        self.quit()

    def __del__(self):
        self.wait()