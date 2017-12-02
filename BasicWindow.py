# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:23:07 2017

@author: aakash.chotrani
"""

import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget, QMainWindow, QPushButton, QAction



class window(QMainWindow):
    
    def __init__(self):
        super(window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle('DigiPen Course Recommender')
        self.setWindowIcon(QIcon(r'C:\Users\aakash.chotrani\Desktop\pyQT\DigiPenLogo_new.png'))
        
        
        extractAction = QAction('&Quit Application',self)
        extractAction.setShortcut('ctrl+s')
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        
        
        
        
        
        
        self.home()
        
        
        
        

    def home(self):
        btn = QPushButton('quit', self)
        btn.resize(100, 100)
        btn.move(100, 100)
        #btn.clicked.connect(QCoreApplication.instance().quit)
        btn.clicked.connect(self.close_application)
        self.show()
        
    def close_application(self):
        print("Hello the application is closed")
        sys.exit()
        
def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())


run()    
        


