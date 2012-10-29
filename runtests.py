import os
def main(func):
    cmd = "nosetests C:/CODE/Sabel/Test/testMain.py:TestMainWindow"#+".test_file
    try:
        os.system(cmd)
    except OSError, e:
        raise Exception, "Error: ", e

if __name__ == "__main__":
    #import uncompyle2
    #import sys
    #file = open("C:/gg.txt")
    #uncompyle2.uncompyle_file("C:/update.pyc",sys.stdout)#,file)
    main("")