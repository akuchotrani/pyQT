# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 11:24:42 2017

@author: Aakash
"""




import sys
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QMessageBox,QPushButton,QLabel
from PyQt5.QtWidgets import QComboBox,QFileDialog,QListWidget,QLineEdit,QHBoxLayout
import ExtractingStudents
import GradientDescentGradePrediction

xPosition = 40
yPosition = 40


class QCustomQWidget(QMainWindow):
    def __init__(self,parent = None):
        super(QMainWindow, self).__init__(parent)
        self.myTestBtn = QPushButton("helloBtn")
        
        self.CourseNameLabel = QLabel()
        self.GradeTextBox = QLineEdit()
        self.allQHBoxLayout = QHBoxLayout()
        #self.allQHBoxLayout.addLayout(self.CourseNameLabel,0)
        #self.allQHBoxLayout.addLayout(self.GradeTextBox,1)
        #self.allQHBoxLayout.addWidget(self.myTestBtn,0)
        self.allQHBoxLayout.addWidget(self.GradeTextBox,0)
        self.setLayout(self.allQHBoxLayout)
    
    def setCourseName(self,courseName):
        self.CourseNameLabel.setText(courseName)


class window(QMainWindow):
    
    csvFileName = ''
    courseList = []
    csvTrainingData = 'TrainingData.csv'
    predictedCourses = []
    predictedCoursesWeights = []
    Target_Student_Prev_Courses = []
    
    #Options which are common to the entire application are included inside the init method
    def __init__(self):
        #Setting up the window
        super(window, self).__init__()
        self.setGeometry(50, 50, 2000, 1000)
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

        
        SelectDataFileLabel = QLabel('Select Data File: ', self)
        SelectDataFileLabel.move(xPosition,yPosition)
        SelectDataFileLabel.setStyleSheet("Qlabel{font:30pt Comic Sans MS}")
        SelectDataFileLabel.setFont(QFont('Arial', 12))
        SelectDataFileLabel.resize(SelectDataFileLabel.sizeHint())
        
        chooseDataFilebtn = QPushButton(' Choose File ', self)
        chooseDataFilebtn.clicked.connect(self.file_open)
        chooseDataFilebtn.setFont(QFont('Arial', 12))
        chooseDataFilebtn.resize(chooseDataFilebtn.sizeHint())
        chooseDataFilebtn.move(xPosition+120, yPosition)
        
        
        SelectDepartmentLabel = QLabel('Select Department: ', self)
        SelectDepartmentLabel.setFont(QFont('Arial', 12))
        SelectDepartmentLabel.move(xPosition,yPosition+40)
        SelectDepartmentLabel.resize(SelectDepartmentLabel.sizeHint())
        
        department_List = ['ALL','Art','Computer Science','Math','Physics','Social Science','Music']
        department_comboBox = QComboBox(self)
        department_comboBox.setFont(QFont('Arial', 12))
        department_comboBox.addItems(department_List)
        department_comboBox.resize(department_comboBox.sizeHint())
        department_comboBox.move(xPosition+150, yPosition+40)
        print(department_comboBox.currentIndex())
        
        
        
        SelectTargetCourse = QLabel('Select Target Course : ', self)
        SelectTargetCourse.move(xPosition+500,yPosition+40)
        SelectTargetCourse.setFont(QFont('Arial', 12))
        SelectTargetCourse.resize(SelectTargetCourse.sizeHint())
        

        self.target_courses_comboBox = QComboBox(self)
        self.target_courses_comboBox.addItems(self.courseList)
        self.target_courses_comboBox.setFont(QFont('Arial', 12))
        self.target_courses_comboBox.move(xPosition+650,yPosition+40)
        self.target_courses_comboBox.resize(200,25)
        
        self.SelectTrainingCourses = QLabel('Select Training Courses : ', self)
        self.SelectTrainingCourses.move(xPosition,yPosition+200)
        self.SelectTrainingCourses.setFont(QFont('Arial', 12))
        self.SelectTrainingCourses.resize(self.SelectTrainingCourses.sizeHint())
        
        self.Training_Courses_ComboBox = QComboBox(self)
        self.Training_Courses_ComboBox.move(xPosition,yPosition+220)
        self.Training_Courses_ComboBox.setFont(QFont('Arial', 12))
        self.Training_Courses_ComboBox.resize(self.target_courses_comboBox.sizeHint())
        self.Training_Courses_ComboBox.resize(200,25)
        
        AddTrainingCourseBtn = QPushButton('Add Training Course >>> ', self)
        AddTrainingCourseBtn.clicked.connect(self.Add_Training_Courses)
        AddTrainingCourseBtn.setFont(QFont('Arial', 12))
        AddTrainingCourseBtn.resize(AddTrainingCourseBtn.sizeHint())
        AddTrainingCourseBtn.move(xPosition, yPosition+270)
        

        TrainingCoursesLabel = QLabel('Training Courses:', self)
        TrainingCoursesLabel.move(xPosition+300,yPosition+175)
        TrainingCoursesLabel.setFont(QFont('Arial', 12))
        TrainingCoursesLabel.resize(TrainingCoursesLabel.sizeHint())
        #self.cutomItem = QListWidgetItem('this is custom text')
        self.TrainingCourses = QListWidget(self)
        self.TrainingCourses.move(xPosition+300,yPosition+200)
        self.TrainingCourses.resize(300,400)
        self.TrainingCourses.setFont(QFont('Arial', 12))


        PredictedCoursesLabel = QLabel('Predicted Courses Effect:', self)
        PredictedCoursesLabel.move(xPosition+700,yPosition+175)
        PredictedCoursesLabel.setFont(QFont('Arial', 12))
        PredictedCoursesLabel.resize(PredictedCoursesLabel.sizeHint())
        
        self.predictedCoursesListWidget = QListWidget(self)
        self.predictedCoursesListWidget.move(xPosition+700,yPosition+200)
        self.predictedCoursesListWidget.resize(300,400)
        self.predictedCoursesListWidget.addItems(self.predictedCoursesWeights)
        self.predictedCoursesListWidget.setFont(QFont('Arial', 12))
        
        PredictedWeightsLabel = QLabel('Predicted Weights:', self)
        PredictedWeightsLabel.move(xPosition+1000,yPosition+175)
        PredictedWeightsLabel.setFont(QFont('Arial', 12))
        PredictedWeightsLabel.resize(PredictedWeightsLabel.sizeHint())
        self.predictedCoursesWeightWidget = QListWidget(self)
        self.predictedCoursesWeightWidget.move(xPosition+1000,yPosition+200)
        self.predictedCoursesWeightWidget.resize(300,400)
        self.predictedCoursesWeightWidget.setFont(QFont('Arial', 12))
        self.predictedCoursesWeightWidget.addItems(self.predictedCoursesWeights)
        

        
        PredictBtn = QPushButton(' Build Weights ', self)
        PredictBtn.clicked.connect(self.Predict_Results)
        PredictBtn.clicked.connect(self.update_available_courses)
        PredictBtn.setFont(QFont('Arial', 12))
        PredictBtn.resize(PredictBtn.sizeHint())
        PredictBtn.move(xPosition+375,yPosition+625)
        
        
        
        SelectDataFileLabel = QLabel('Enter Grades Of Training Courses: ', self)
        SelectDataFileLabel.move(xPosition+50,yPosition+710)
        SelectDataFileLabel.setStyleSheet("Qlabel{font:30pt Comic Sans MS}")
        SelectDataFileLabel.setFont(QFont('Arial', 12))
        SelectDataFileLabel.resize(SelectDataFileLabel.sizeHint())
        # Create textbox
        self.GradeTextBox = QLineEdit(self)
        self.GradeTextBox.move(xPosition+300,yPosition+700)
        self.GradeTextBox.setFont(QFont('Arial', 12))
        self.GradeTextBox.resize(280,40)
        
        PredictGradeBtn = QPushButton('Predict Grade', self)
        PredictGradeBtn.clicked.connect(self.Predict_Grade)
        PredictGradeBtn.move(xPosition+375,yPosition+750)
        PredictGradeBtn.setFont(QFont('Arial', 12))
        PredictGradeBtn.resize(PredictGradeBtn.sizeHint())
        
        PredictGradeHintLabel = QLabel('Predicted Grade: ', self)
        PredictGradeHintLabel.move(xPosition+800,yPosition+750)
        PredictGradeHintLabel.setStyleSheet("color: rgb(0,0,250);")
        PredictGradeHintLabel.setFont(QFont('Arial', 12))
        PredictGradeHintLabel.resize(PredictGradeHintLabel.sizeHint())
        
        self.PredictedGradeNumberLabel = QLabel('0', self)
        self.PredictedGradeNumberLabel.move(xPosition+1000,yPosition+750)
        self.PredictedGradeNumberLabel.setStyleSheet("color: rgb(0,0,250);")
        self.PredictedGradeNumberLabel.setFont(QFont('Arial', 12))
        self.PredictedGradeNumberLabel.resize(100,20)
        
        RestartBtn = QPushButton('Reset', self)
        RestartBtn.clicked.connect(self.Restart_Prediction)
        RestartBtn.setFont(QFont('Arial', 12))
        RestartBtn.resize(RestartBtn.sizeHint())
        RestartBtn.move(xPosition+700,yPosition+850)
        
        self.show()
        
    
    def Predict_Grade(self):
        enteredGrades = self.GradeTextBox.text()
        floatGrades = []
        for grade in enteredGrades.split(','):
            floatGrades.append(float(grade))
            
        print("Entered Grades:",enteredGrades)
        print("Float Grades:",floatGrades)
        
        finalPredictedGrade = 0
        courseCounter = 0
        for grade in floatGrades:
            print("Multiplying Weight:",self.predictedCoursesWeights[courseCounter]," and Grade:",grade)
            finalPredictedGrade = finalPredictedGrade + grade*float(self.predictedCoursesWeights[courseCounter])
            courseCounter = courseCounter + 1
        
        print("Final Grade: ",finalPredictedGrade)
        finalPredictedGrade = format(finalPredictedGrade,'.2f')
        self.PredictedGradeNumberLabel.setText(str(finalPredictedGrade))
        
        #clearing the enteredGrades when prediction is done
        floatGrades.clear()
        
        
    def Restart_Prediction(self):
        print("Restarting Prediction")
        self.TrainingCourses.clear()
        self.predictedCoursesListWidget.clear()
        self.predictedCoursesWeightWidget.clear()
        self.Target_Student_Prev_Courses.clear()
        self.predictedCoursesWeights.clear()
        
        self.GradeTextBox.clear()
        self.PredictedGradeNumberLabel.setText("0")
    
    
    
    def Add_Training_Courses(self):
        training_Course = str(self.Training_Courses_ComboBox.currentText())
        print("Adding training course: ",training_Course)
        self.Target_Student_Prev_Courses.append(training_Course)
        self.TrainingCourses.addItem(training_Course)
        self.TrainingCourses.update()
        
    
    
        
    def Predict_Results(self):
        
        targetCourse = str(self.target_courses_comboBox.currentText())
        print("Target Course Selected: ",targetCourse)
        
        ID_Prev_Students = ExtractingStudents.Check_Target_Course(targetCourse)
        print("Num of Students Who Previously Took The Target Course: ", len(ID_Prev_Students))
        
        
        
        target_course_recorded_grades = ExtractingStudents.Record_Target_Course_Values(ID_Prev_Students,targetCourse)
        
        
        recordedCourseData = ExtractingStudents.Create_Data_To_Train(self.Target_Student_Prev_Courses, ID_Prev_Students)
        cleanedRecordedData = ExtractingStudents.Clean_Data_To_Train(recordedCourseData)
        
        ExtractingStudents.Merge_Target_Course_Grade_To_Cleaned_Data(cleanedRecordedData,target_course_recorded_grades)
    
        gradeTable = ExtractingStudents.Create_Grade_Table(cleanedRecordedData)
        ExtractingStudents.Array2D_to_CSV("TrainingData.csv",gradeTable)
        
        Model = GradientDescentGradePrediction.Perform_All_Data_Steps(self.csvTrainingData)
        
        self.Display_Predicted_Courses(Model)
    
    
        
    def Display_Predicted_Courses(self,Model):
        
        unScaledPredictedWeights = []
        SumOfPredictedWeights = 0
        for weight in Model.coef_[0]:
            #Ignoring the negative weights
            if weight > 0:
                SumOfPredictedWeights = SumOfPredictedWeights + weight
                unScaledPredictedWeights.append(weight)
            else:
                unScaledPredictedWeights.append(0)
        
        ScaledPredictedWeights = []
        for item in unScaledPredictedWeights:
            scaledItem = item/SumOfPredictedWeights
            scaledItem = format(scaledItem,'.4f')
            ScaledPredictedWeights.append(scaledItem)
            
        print("UnScaledPredicted Weights:",unScaledPredictedWeights)
        print("SumOfPredictedPositiveWeights:",SumOfPredictedWeights)
        print("ScaledPredictedWeight:",ScaledPredictedWeights)
        for weight in ScaledPredictedWeights:
            self.predictedCoursesWeights.append(str(weight))
            
        #print(self.predictedCoursesWeights)
        #self.predictedCoursesWeights = np.array_str(Model.coef_) 
        Output_Weights = []
        Output_Subjects = []

        zipped = sorted(zip(self.Target_Student_Prev_Courses,self.predictedCoursesWeights),key = lambda x:x[1], reverse = True)
        print("Zipped:",zipped)
        for item in zipped:
            print("Subject:",item[0]," Weight:",item[1])
            Output_Subjects.append(item[0])
            Output_Weights.append(item[1])
            

        self.predictedCoursesWeightWidget.addItems(Output_Weights)
        self.predictedCoursesListWidget.addItems(Output_Subjects)
        
        #clearing All data before next prediction
        zipped.clear()
        print("Zipped Clear: ",zipped)
        Output_Subjects.clear()
        Output_Weights.clear()
        unScaledPredictedWeights.clear()
        ScaledPredictedWeights.clear()
        SumOfPredictedWeights = 0
       
        
    def file_open(self):
        self.csvFileName, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        print("Opening Csv File: ",self.csvFileName)
        ExtractingStudents.Create_Dictionary_of_Dictionary(self.csvFileName)
        print("Creating Dictionary of Dictionary")
        self.update_available_courses()
        
    
    def update_available_courses(self):
        self.courseList = ExtractingStudents.AvailableCourses
        self.courseList.sort()
        self.target_courses_comboBox.addItems(self.courseList)
        self.Training_Courses_ComboBox.addItems(self.courseList)
        
    
        
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