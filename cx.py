from cx_Freeze import setup, Executable
#excludes = ['curses', 'email', 'tcl','tk','Tkinter','Tkconstants','pywin.debugger']
"""
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
               'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
               'Tkconstants', 'Tkinter']
"""
packages = []
path = []
exe = Executable(
    script="C:\CODE\Sabel\main.py",
    base="Win32GUI",
    targetName = "Sabel.exe",
    initScript = None,
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "C:\CODE\Sabel\Icons\sabel.ico"
    )

setup(
    name = "Sabel",
    version ="0.60",
    description = "Sabel IDE",
    executables = [exe]
    )
