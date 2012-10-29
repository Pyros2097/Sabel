popbg = """
        QWidget { 
        background: QLinearGradient(x1: 1, y1: 0, x2: 0, y2: 1, stop: 0.4 #eef, stop: 0.9 #ccf);
        border: 1px solid gray;
        border-radius: 40px;
        }
        QLabel{
		    /*background: qlineargradient(x1: 0, y1: 1, x2: 0.08, y2: 0.05,stop: 0.2 #e8f2fe, stop: 0.9 #d8f2dd);*/
		    border: 1px solid gray;
            font-size: 12px;
			padding-left: 15px;
			padding-top: 5px;
			border-radius: 30px;
        }
        QLineEdit {
            padding: 1px;
            border-style: solid;
            border: 2px solid gray;
            border-radius: 8px;
        }
        QPushButton {
            color: white;
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c);
            border-width: 1px;
            border-color: #339;
            border-style: solid;
            border-radius: 7;
            padding: 3px;
            font-size: 10px;
            padding-left: 5px;
            padding-right: 5px;
            min-width: 50px;
            max-width: 50px;
            min-height: 13px;
            max-height: 13px;
        }  
        """
stletabb = """
        /* Style the tab using the tab sub-control. Note that
     it reads QTabBar _not_ QTabWidget */
 QTabBar::tab {
    /*background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);*/
     border: 1px solid #C2C7CB;
     border-top-color: #e8f2fe;
     border-bottom-color: #e8f2fe; /* same as the pane color */
     border-top-left-radius: 1px;
     border-top-right-radius: 1px;
     min-width: 10ex;
     padding: 4px;
 }

 QTabBar::tab:selected, QTabBar::tab:hover {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                 stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
 }

 QTabBar::tab:selected {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    /* border-color: #9B9B9B; */
     border: 0px solid #C2C7CB;
     border-bottom-color: #C2C7CB;
     border-top-left-radius: 1px;
     border-top-right-radius: 1px;
     margin-left: 1px;
     margin-right: 1px;
 }

 QTabBar::tab:!selected {
     margin-top: 0px; /* make non-selected tabs look smaller */
      margin-left: 0px;
      margin-right: 0px;
 }
 
  QTabBar::close-button {
     /*image: url(:/Icons/x.png) 5;*/
 }
 QTabBar::close-button:hover {
      /*image: url(:/Icons/x.png);*/
 }
 QTabBar:hover
    {
        /*background-color: rgb(175,175,175);*/
    }
  
"""

progstyl = """
 QProgressBar {
     border: 2px solid grey;
     border-radius: 5px;
     text-align: center;
 }

 QProgressBar::chunk {
     background-color: #05B8CC;
     width: 20px;
     margin: 0.5px;
 }
"""
mainstyl = """
QMainWindow::separator {
     background: yellow;
     width: 10px; /* when vertical */
     height: 10px; /* when horizontal */
 }

 QMainWindow::separator:hov
"""