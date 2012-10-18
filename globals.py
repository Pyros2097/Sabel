import os
from platform import system,python_version
from PyQt4.QtGui import QIcon,QPixmap,QApplication,QSplashScreen
from send2trash import send2trash
from config import Config

__version__ = "0.60"
#Python accesses local variables much more efficiently than global variables. 
oslistdir = os.listdir
ospathisdir = os.path.isdir
ospathsep = os.path.sep
ospathjoin = os.path.join
ospathexists = os.path.exists
ospathbasename = os.path.basename
ospathdirname = os.path.dirname
ospathnormpath = os.path.normpath
oswalk = os.walk
osmkdir = os.mkdir
osremove = os.remove
osrename = os.rename
ossep = os.sep
OS_NAME = system()
eol = 0
if(OS_NAME == 'Windows'):
    eol = 0
elif(OS_NAME == 'Linux'):
    eol = 1
else:
    eol = 2

workDir = os.getcwd()
apiDir = ospathjoin(workDir,"api")
iconDir = ospathjoin("Icons")
binDir = ospathjoin(workDir,"bin")
sqc = ospathjoin(binDir,"sqc.exe")

recycle = send2trash
PY_VERSION = python_version()

#Config data
config = Config()
workSpace = config.workSpace()
fontSize = config.fontSize()
fontName = config.fontName()
iconSize = config.iconSize()

def os_icon(name):
        return QIcon(":/{0}.png".format(ospathjoin(iconDir,name)))
def os_pixmap(name):
        return QPixmap(":/{0}.png".format(ospathjoin(iconDir,name)))

class Icons:
    add = os_icon('auto_add')
    alert_obj = os_icon('alert_obj')
    anchor = os_icon('anchor')
    android = os_icon('android')
    ant_view = os_icon('ant_view')
    capture_screen = os_icon('capture_screen')
    close_view = os_icon('close_view')
    cmpC_pal = os_icon('cmpC_pal')
    color_palette = os_icon('color_palette')
    console_view = os_icon('console_view')
    cprj = os_icon('cprj')
    cut_edit = os_icon('cut_edit')
    debug_exec = os_icon('debug_exec')
    edit = os_icon('edit')
    emblem_system = os_icon('emblem_system')
    error = os_icon('error')
    error_log = os_icon('error_log')
    error_small = os_icon('error_small')
    file_obj = os_icon('file_obj')
    find = os_icon('find')
    foldej = os_icon('foldej')
    font = os_icon('font')
    fullscreen = os_icon('fullscreen')
    go = os_icon('go')
    high = os_icon('high')
    image = os_icon('image')
    lib = os_icon('lib')
    libset = os_icon('libset')
    logoemo = os_icon('logoemo')
    logosabel = os_icon('logosabel')
    logosq = os_icon('logosq')
    music = os_icon('music')
    nattrib = os_icon('nattrib')
    nav_backward = os_icon('nav_backward')
    nav_forward = os_icon('nav_forward')
    nav_home = os_icon('nav_home')
    new_file = os_icon('new_file')
    newfolder = os_icon('newfolder')
    newpack = os_icon('newpack')
    newprj = os_icon('newprj')
    nut = os_icon('nut')
    open = os_icon('open')
    package = os_icon('package')
    paste_edit = os_icon('paste_edit')
    prj = os_icon('prj')
    redo_edit = os_icon('redo_edit')
    refresh_tab = os_icon('refresh_tab')
    run = os_icon('run')
    sabel = os_icon('sabel')
    save = os_icon('save')
    saveall = os_icon('saveall')
    saveas = os_icon('saveas')
    start_ccs_task = os_icon('start_ccs_task')
    stop = os_icon('stop')
    style = os_icon('style')
    system = os_icon('system')
    task_set = os_icon('task_set')
    thread_view = os_icon('thread_view')
    threadgroup_obj = os_icon('threadgroup_obj')
    toc_open = os_icon('toc_open')
    trash = os_icon('trash')
    undo_edit = os_icon('undo_edit')
    warning = os_icon('warning')
    x = os_icon('x')
    zoomminus = os_icon('zoomminus')
    zoomplus = os_icon('zoomplus')
    ios = os_icon('ioss')
    emo = os_icon('emo')
    method = os_icon('auto_jmeth')
    class1 = os_icon('auto_class')
    field = os_icon('auto_field')
    
class Auto:
    auto_activity = os_pixmap('auto_activity')
    auto_add = os_pixmap('auto_add')
    auto_bulb = os_pixmap('auto_bulb')
    auto_class = os_pixmap('auto_class')
    auto_class2 = os_pixmap('auto_class2')
    auto_co = os_pixmap('auto_co')
    auto_doc = os_pixmap('auto_doc')
    auto_enum = os_pixmap('auto_enum')
    auto_envvar = os_pixmap('auto_envvar')
    auto_field = os_pixmap('auto_field')
    auto_jmeth = os_pixmap('auto_jmeth')
    auto_method = os_pixmap('auto_method')
    auto_pub = os_pixmap('auto_pub')
    auto_var = os_pixmap('auto_var')    
    auto_error = os_pixmap('error')
    auto_package = os_pixmap('package')

class Pix:
    logosabel = os_pixmap('logosabel')
    logoemo = os_pixmap('logoemo')
    logosq = os_pixmap('logosq')
    
splash_pix = Pix.logosabel