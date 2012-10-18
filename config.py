import yaml
import os
from PyQt4.QtGui import QMessageBox
class Config:
    def __init__(self):     
        self.configfile = 'config.yml'
        self.data = yaml.load(open(self.configfile).read())
        
    def read(self,section):
        return self.data[section]
    
    def readSetting(self,section):
        return self.data["Setting"][section]
    
    def writeSetting(self,section,value):
        self.data["Setting"][section] = value
        self.write()
    
    def workSpace(self):
        return self.readSetting("workspace")
    
    def fontSize(self):
        return int(self.readSetting('fontsize'))
    def setFontSize(self,val):
        self.writeSetting('fontsize',val)
    
    def fontName(self):
        return self.readSetting('fontname')
    def setFontName(self,val):
        self.writeSetting('fontname',val)
        
    def iconSize(self):
        return int(self.readSetting('iconsize'))
    def setIconSize(self,val):
        self.writeSetting('iconsize',val)
        
    def toolLabel(self):
        int(self.readSetting('toollabel'))
    def setToolLabel(self,bool):
        self.writeSetting('toollabel',bool)
    
    def mode(self):
        return int(self.readSetting('mode'))
    def setMode(self,value):
        self.writeSetting("mode",value)
        
    def margin(self):
        return int(self.readSetting('margin'))
    def setMargin(self,value):
        self.writeSetting("margin",value)
        
    def indent(self):
        return int(self.readSetting('indent'))
    def setIndent(self,value):
        self.writeSetting("indent",value)
    
    '''0 is emulator 1 is device'''
    def device(self):
        return int(self.readSetting('device'))
    def setDevice(self,value):
        self.writeSetting("device",value)
        
    def thresh(self):
        return self.readSetting('thresh')
    def setThresh(self,val):
        self.writeSetting('thresh',val)
        
    def tabwidth(self):
        return self.readSetting('tabwidth')
    def setTabWidth(self,val):
        self.writeSetting('tabwidth',val)
    
    def projects(self):
        return self.read('Project')
    def setProject(self,pros):
        self.data['Project'] = pros
        self.write()
    
    def closedProjects(self):
        return self.read('ClosedProject')
    def setClosedProjects(self,val):
        self.data['ClosedProject']= val
        self.write()
    
    def recent(self):
        return self.read('Recent')      
    
    def files(self):
        return self.read('File')
    def setFile(self,files):
        self.data['File'] = files
        self.write()
          
    def adb(self):
        return self.read('ADB')
    def setAdb(self,val):
        self.data['ADB'] = val
        self.write()
        
    def ant(self):
        return self.read('ANT')
    def setAnt(self,val):
        self.data['ANT'] = val
        self.write()
        
    def cmds(self):
        return self.read('CMD')
    
    def setCmd(self,val):
        self.data['CMD'] = val
        self.write()
    
    def params(self):
        return self.read('PARAM')
    
    def setParam(self,val):
        self.data['PARAM'] = val
        self.write()
        
    
    def colorStyle(self):
        return int(self.readSetting('colorstyle'))
    def styleIndex(self):
        return self.readSetting('styleindex')
    def setstyleIndex(self,value):
        self.writeSetting("styleindex",value)
        
    def todo(self):
        return self.read('TODO')
    def setTodo(self,val):
        self.data['TODO'] = val
        self.write()
    
    def write(self):
        try:
            yaml.dump(self.data,open(self.configfile,'w'),default_flow_style=False)
        except:
            QMessageBox.about(self,"Can't Open","cannot open config file\n"+self.configfile) 