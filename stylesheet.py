slisty = """
         QSlider::groove:horizontal {
     border: 1px solid #999999;
     height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
     margin: 2px 0;
 }

 QSlider::handle:horizontal {
     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
     border: 1px solid #5c5c5c;
     width: 18px;
     margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
     border-radius: 3px;
 }
 /*
 QSlider::add-page:horizontal {
     background: white;
 }

 QSlider::sub-page:horizontal {
     background: pink;
 }
 */
"""

stletabb = """
        /* Style the tab using the tab sub-control. Note that
     it reads QTabBar _not_ QTabWidget */
 QTabBar::tab {
    /*background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);*/
     border: 1px solid #C2C7CB;
     border-bottom-color: #C2C7CB; /* same as the pane color */
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
     border-color: #9B9B9B;
     border-bottom-color: #C2C7CB; /* same as pane color */
 }

 QTabBar::tab:!selected {
     margin-top: 0px; /* make non-selected tabs look smaller */
      margin-left: 0px;
      margin-right: 0px;
 }

 /* make use of negative margins for overlapping tabs */
 QTabBar::tab:selected {
     /* expand/overlap to the left and right by 4px */
     margin-left: 0px;
     margin-right: 0px;
 }
 
  QTabBar::close-button {
     /*image: url(:/Icons/x.png) 5;*/
 }
 QTabBar::close-button:hover {
      /*image: url(:/Icons/x.png);*/
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

 QMainWindow::separator:hover {
     background: red;
 }
"""
