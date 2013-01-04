from cx_Freeze import setup, Executable
excludes = ['curses', 'email', 'tcl','tk','Tkinter','Tkconstants','pywin.debugger']
includes = ["urllib2","logging","codecs"]
packages = []
path = []
exe = Executable(
    script="C:\CODE\Sabel\main.py",
    base="Win32GUI",
    targetName = "Sabel.exe",
    initScript = None,
    compress = False,
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = False,
    icon = "C:\CODE\Sabel\Icons\sabel.ico"
    )

setup(
    name = "Sabel",
    version ="0.00",
    description = "Sabel IDE",
    options = {"build_exe": {"includes": includes,
                 "excludes": excludes,
                 #"packages": packages
                 #"path": path
                 }
           },

    executables = [exe]
    )
