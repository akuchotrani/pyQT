# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 11:24:42 2017

@author: Aakash
"""




import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QMessageBox,QPushButton,QLabel
from PyQt5.QtWidgets import QComboBox,QFileDialog,QListWidget,QListWidgetItem
import numpy as np
import ExtractingStudents
import GradientDescentGradePrediction

xPosition = 25
yPosition = 25


class window(QMainWindow):
    
    csvFileName = ''
    courseList = []
    csvTrainingData = 'TrainingData.csv'
    predictedCourses = []
    predictedCoursesWeights = []
    
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
        
        chooseDataFilebtn = QPushButton('Choose File', self)
        chooseDataFilebtn.clicked.connect(self.file_open)
        chooseDataFilebtn.resize(chooseDataFilebtn.sizeHint())
        chooseDataFilebtn.move(xPosition, yPosition)
        
        self.SelectDepartmentLabel = QLabel('Select Department: ', self)
        self.SelectDepartmentLabel.move(xPosition,yPosition+30)
        department_List = ['ALL','Art','Computer Science','Math','Physics','Social Science','Music']
        department_comboBox = QComboBox(self)
        department_comboBox.addItems(department_List)
        department_comboBox.resize(department_comboBox.sizeHint())
        department_comboBox.move(xPosition, yPosition+60)
        print(department_comboBox.currentIndex())
        
        
        
        self.SelectCourse = QLabel('Select Course : ', self)
        self.SelectCourse.move(xPosition,yPosition+90)
        self.courses_comboBox = QComboBox(self)
        self.courses_comboBox.addItems(self.courseList)
        self.courses_comboBox.move(xPosition,yPosition+120)
        self.courses_comboBox.resize(self.courses_comboBox.sizeHint())
        
        self.predictedCoursesWeightWidget = QListWidget(self)
        self.predictedCoursesWeightWidget.move(xPosition+500,yPosition)
        self.predictedCoursesWeightWidget.resize(300,400)
        self.predictedCoursesWeightWidget.addItems(self.predictedCoursesWeights)
        
        self.predictedCoursesListWidget = QListWidget(self)
        self.predictedCoursesListWidget.move(xPosition+200,yPosition)
        self.predictedCoursesListWidget.resize(300,400)
        self.predictedCoursesListWidget.addItems(self.predictedCoursesWeights)
        
        PredictBtn = QPushButton('Predict Courses', self)
        PredictBtn.clicked.connect(self.Predict_Results)
        PredictBtn.clicked.connect(self.update_available_courses)
        PredictBtn.resize(PredictBtn.sizeHint())
        PredictBtn.move(xPosition, yPosition+150)
        
        
        
        self.show()
        
    def Predict_Results(self):
        
        targetCourse = str(self.courses_comboBox.currentText())
        print("Target Course Selected: ",targetCourse)
        
        ID_Prev_Students = ExtractingStudents.Check_Target_Course(targetCourse)
        print("Num of Students Who Previously Took The Target Course: ", len(ID_Prev_Students))
        
        
        
        target_course_recorded_grades = ExtractingStudents.Record_Target_Course_Values(ID_Prev_Students,targetCourse)
        
        
        self.Target_Student_Prev_Courses = ['MAT140','CS100','CS120','ENG110','COL101','GAM100',
                                   'MAT150','CS170','CS230','COM150','GAM150',
                                   'MAT200','CS180','CS200','CS225','GAM200',
                                   'MAT250','PHY200','CS250','CS280','GAM250']
        
        recordedCourseData = ExtractingStudents.Create_Data_To_Train(self.Target_Student_Prev_Courses, ID_Prev_Students)
        cleanedRecordedData = ExtractingStudents.Clean_Data_To_Train(recordedCourseData)
        
        ExtractingStudents.Merge_Target_Course_Grade_To_Cleaned_Data(cleanedRecordedData,target_course_recorded_grades)
    
        gradeTable = ExtractingStudents.Create_Grade_Table(cleanedRecordedData)
        ExtractingStudents.Array2D_to_CSV("TrainingData.csv",gradeTable)
        
        Model = GradientDescentGradePrediction.Perform_All_Data_Steps(self.csvTrainingData)
        
        self.Display_Predicted_Courses(Model)
    
    
    def Display_Predicted_Courses(self,Model):
        #print("Model Weights: ",Model.coef_)
        
        courseCounter = 0
        for weight in Model.coef_[0]:
            self.predictedCoursesWeights.append(str(weight))
            courseCounter = courseCounter + 1
            
        #print(self.predictedCoursesWeights)
        #self.predictedCoursesWeights = np.array_str(Model.coef_) 
        Output_Weights = []
        Output_Subjects = []
        Output_Subjects.clear()
        Output_Weights.clear()
        zipped = sorted(zip(self.Target_Student_Prev_Courses,self.predictedCoursesWeights),key = lambda x:x[1], reverse = True)
        for item in zipped:
            print("Subject:",item[0]," Weight:",item[1])
            Output_Subjects.append(item[0])
            Output_Weights.append(item[1])
            
            
        self.predictedCoursesListWidget.clear()
        self.predictedCoursesWeightWidget.clear()

        self.predictedCoursesWeightWidget.addItems(Output_Weights)
        self.predictedCoursesListWidget.addItems(Output_Subjects)
       
        
    def file_open(self):
        self.csvFileName, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        print("Opening Csv File: ",self.csvFileName)
        ExtractingStudents.Create_Dictionary_of_Dictionary(self.csvFileName)
        print("Creating Dictionary of Dictionary")
        self.update_available_courses()
        
    
    def update_available_courses(self):
        self.courseList = ExtractingStudents.AvailableCourses
        self.courseList.sort()
        self.courses_comboBox.addItems(self.courseList)
        
    
        
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