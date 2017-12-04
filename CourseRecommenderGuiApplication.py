# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 11:24:42 2017

@author: Aakash
"""




import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QMessageBox,QPushButton,QLabel
from PyQt5.QtWidgets import QComboBox

class window(QMainWindow):
    
    #Options which are common to the entire application are included inside the init method
    def __init__(self):
        #Setting up the window
        super(window, self).__init__()
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle('DigiPen Course Recommender')
        self.setWindowIcon(QIcon('DigiPenLogo_new.png'))
        
        #Creating Menu
        extractAction = QAction('&Quit Application', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)
        
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)   


        #------------------------Calling-------Home Screen
        self.home()
        
    def home(self):
        
        
        
        self.SelectDepartmentLabel = QLabel('Select Department: ', self)
        self.SelectDepartmentLabel.move(25,25)
        department_List = ['Art','Computer Science','Math','Physics','Social Science','Music']
        department_comboBox = QComboBox(self)
        department_comboBox.addItems(department_List)
        department_comboBox.resize(department_comboBox.sizeHint())
        department_comboBox.move(25, 50)
        
        
        
        self.SelectCourse = QLabel('Select Course : ', self)
        self.SelectCourse.move(25,75)
        courseList = ['cs525','cs529','cs541']
        courses_comboBox = QComboBox(self)
        courses_comboBox.addItems(courseList)
        courses_comboBox.move(25,100)
        courses_comboBox.resize(courses_comboBox.sizeHint())
        
        
        btn = QPushButton('PredictCourses', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())
        btn.move(25, 200)
        
        
        
        self.show()
        
        
        
       
        
        
    
    
    def Predict_CourseContibution():
        print('return a list of relevant courses')
    
        
    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('quit application')
            sys.exit()
        else:
            pass



def main():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()