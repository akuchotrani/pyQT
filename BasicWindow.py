# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:23:07 2017

@author: aakash.chotrani
"""

import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget, QMainWindow, QPushButton, QAction,QMessageBox
from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QCheckBox



class window(QMainWindow):
    
    def __init__(self):
        super(window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle('DigiPen Course Recommender')
        #self.setWindowIcon(QIcon(r'C:\Users\aakash.chotrani\Desktop\pyQT\DigiPenLogo_new.png'))
        self.setWindowIcon(QIcon(r'DigiPenLogo_new.png'))
        
        extractAction = QAction('&Quit Application',self)
        extractAction.setShortcut('ctrl+Q')
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        
        extractAction = QAction(QIcon('CsvToolPic.png'),'flee the scene',self)
        extractAction.triggered.connect(self.close_application)
        
        self.toolBar = self.addToolBar('Extraction')
        self.toolBar.addAction(extractAction)
        
 
        
        
        
        self.home()
        
        
        
        

    def home(self):
        btn = QPushButton('quit', self)
        btn.resize(100, 100)
        btn.move(100, 100)
        #btn.clicked.connect(QCoreApplication.instance().quit)
        btn.clicked.connect(self.close_application)
        
        checkBox = QCheckBox('Enlarge Window',self)
        checkBox.move(0,50)
        checkBox.stateChanged.connect(self.enlarge_window)
        
        
        
        
        self.show()
    
    def enlarge_window(self,state):
        if state == Qt.Checked:
            self.setGeometry(50,50,1000,600)
        else:
            self.setGeometry(50,50,500,300)
        
    def close_application(self):
        choice = QMessageBox.question(self,'Quit',"Are you sure you want to Quit?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if choice == QMessageBox.Yes:
            print('Quit Application')
            sys.exit()
        else:
            pass
        
def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())


run()    
        


