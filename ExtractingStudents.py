# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:13:11 2017

@author: aakash.chotrani
"""

import numpy as np
import pandas as pd


#DataCsv = pd.read_csv("StudGradesInfo.csv")



def CSV_to_Array2D(filename):
  import csv
  csvfile = open(filename, 'r')
  reader = csv.reader(csvfile)
  result = []
  for row in reader:
    result.append(row)
  return result

def Array2D_to_CSV(filename, table):
  csvfile = open(filename, 'w')
  for row in table:
    counter = 1
    for cell in row:
      csvfile.write(str(cell))
      if(counter < len(row)):
          csvfile.write(',')
          counter = counter + 1
    csvfile.write('\n')
  csvfile.close()



#Return an object by parsing the course string and seperating it with keys: code , season, year
#Example:-
#course string = CS230S17-B
#code: CS230
#season: S
#year: 17
def courseString_to_Object(course):
  import re
  expression = r'(([A-Z]+)([0-9]+))([A-Z]+)([0-9]+)'
  match = re.match(expression, course)
  return { 'code': match.group(1), 'season': match.group(4), 'year': match.group(5) }



students = {}
AvailableCourses = []
def Create_Dictionary_of_Dictionary(fileName):
    #creating a dictionary of dictionary of all the 4102 students mapped by ID 
    StudGradesInfo = CSV_to_Array2D(fileName)
    DataCsv = pd.read_csv(fileName)
    print("Total Data Records Parsed: ",len(DataCsv))
    #creating a dictionary for 4102 students
    for i in range(1,len(DataCsv)):
        row = StudGradesInfo[i]
        ID = row[0]    
        students[ID] = {}
        
        SectionCode = courseString_to_Object(row[3])
        SubjectString = SectionCode['code']
        if SubjectString not in AvailableCourses:
            AvailableCourses.append(SubjectString)
    print('Total available courses: ',len(AvailableCourses))
    
    #For each student mapping their ID to the course that they took.
    for i in range(1,len(DataCsv)):
        row = StudGradesInfo[i]
        ID = row[0]
        #Considering only the student who enrolled into the class. 
        #If status row[5] is 2 the student took it and did not drop the class
        #If Grade row[6] is zero. It indicates that student is enrolled and currently taking the class. The data is not avaialble. Hence we will skip it.
        if row[5] == '2' and row[6] != '0':
            SectionCode = courseString_to_Object(row[3])
            students[ID][SectionCode['code']] = row[7]
        

#Go through the whole students dictionary and check if the student has taken the target course
# If yes then record the grade and record the keys
def Check_Target_Course(target_course):

    ID_Prev_Students = []
    for keys in students:
        if target_course in students[keys]:
            ID_Prev_Students.append(keys)

    return ID_Prev_Students


def Record_Target_Course_Values(student_IDs,target_course):
    print("Recording target course values.....")
    grades_Target_Course = []
    for ID in student_IDs:
        grade = students[ID][target_course]
        grades_Target_Course.append(grade)
        #print(grade)
    return grades_Target_Course
        
    

#recoding the grade of all the students for all the courses target student took previously.
def Create_Data_To_Train(Courses,StudentIDs):
    print("Creating Training Data....")
    
    #Creating lists of list of all the courses for recording the grade
    courseLists = [[] for i in Courses]
    #print("Course List: ",courseLists)
    
    #looping through all the students who previously took the course
    for ID in StudentIDs:
        if ID in students:
            #looping through and checking if the previous student also took similar courses as traget course.
            
            for index,course in enumerate(Courses):
                #if student also took the same course just record his grade for training
                if course in students[ID]:
                    courseLists[index].append(students[ID][course])
                #Student did not take this course then append -1
                else:
                    courseLists[index].append(-1)
    return courseLists

def Clean_Data_To_Train(recordedCourseData):
    print("Clean data for total courses: ",len(recordedCourseData))
 
    
    #cleaning all the courses grade list
    for indexList in range(0,len(recordedCourseData)):
        #converting all the grade values from string to float
        recordedCourseData[indexList] = [float(i) for i in recordedCourseData[indexList]]
        #calculating the mean of the course and rounding it to 2 decimal places
        mean_course = sum(recordedCourseData[indexList])/len(recordedCourseData[indexList])
        mean_course = round(mean_course,2)
        #print("Mean: ",mean_course)
        
        #for all the courses if the data is not available == -1 we will fill in the missing values with mean
        for indexGrade,grade in enumerate(recordedCourseData[indexList]):
            if grade == -1:
                recordedCourseData[indexList][indexGrade] = mean_course
    return recordedCourseData


def Merge_Target_Course_Grade_To_Cleaned_Data(cleanedRecordedData, grades_Target_Course):
    cleanedRecordedData.append(grades_Target_Course)
    
    


def Create_Grade_Table(cleanedRecordedData):
    
    print("Creating Grade Table")
    # make a grade table for students(columns) and courses(rows)
    gradeTable = []
    
    #go through all the student records
    for index in range(0,len(cleanedRecordedData[0])):
        #create a row for each student
        gradeTableRow = []
        #go through all the courses per student
        for courseIndex in range(0,len(cleanedRecordedData)):
            gradeTableRow.append(cleanedRecordedData[courseIndex][index])
        gradeTable.append(gradeTableRow)        
        
    return gradeTable



def main():
    print("Exectuing the code")
    fileName = 'StudGradesInfo.csv'
    Create_Dictionary_of_Dictionary(fileName)
    
    print('Total available courses: ',len(AvailableCourses))
    
    Target_Course = "CS300"
    Target_Student_Prev_Courses = ['MAT140','CS100','CS120','ENG110','COL101','GAM100',
                                   'MAT150','CS170','CS230','COM150','GAM150',
                                   'MAT200','CS180','CS200','CS225','GAM200',
                                   'MAT250','PHY200','CS250','CS280','GAM250']
    
    ID_Prev_Students = Check_Target_Course(Target_Course)
    print("Num of Students Who Previously Took The Target Course: ", len(ID_Prev_Students))
    
    target_course_recorded_grades = Record_Target_Course_Values(ID_Prev_Students,Target_Course)
    
    recordedCourseData = Create_Data_To_Train(Target_Student_Prev_Courses, ID_Prev_Students)
    cleanedRecordedData = Clean_Data_To_Train(recordedCourseData)
    
    Merge_Target_Course_Grade_To_Cleaned_Data(cleanedRecordedData,target_course_recorded_grades)
    
    gradeTable = Create_Grade_Table(cleanedRecordedData)
    Array2D_to_CSV("TrainingData.csv",gradeTable)
    
    
if __name__ == "__main__":
    main()



