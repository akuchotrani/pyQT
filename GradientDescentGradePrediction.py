# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:44:44 2017

@author: aakash.chotrani
"""
import numpy as np
import pandas as pd


'''
def GradentDescent(X,y,Theta,alpha,m,numIterations):
    X_trans = X.transpose()
    #print("X_transpose: ",X_trans)
    for i in range(1,numIterations):
        hypothesis = np.dot(X,Theta)
        loss = hypothesis - y
        cost = np.sum(loss ** 2)/(2*m)
        print("Iteration: ",i," | Cost: ", cost)
        print("Weights: ",Theta)
        print("")
        gradient = np.dot(X_trans,loss)
        print("Gradient: ",gradient)
        #Theta = Theta - alpha*gradient
        Theta = Theta - gradient.dot(alpha)
    return Theta


'''


def Read_Dataset(filename):
    DataCsv = pd.read_csv(filename)
    X =DataCsv.iloc[:,:-1].values
    y = DataCsv.iloc[:,-1].values
    return X,y


def Perform_Feature_Scaling(X,y):
    #Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X)
    sc_y = StandardScaler()
    y = np.array(y).reshape(-1,1)
    y_train = sc_y.fit_transform(y)
    
    return X_train, y_train


def Train_Model_Library_Method(X_train, y_train):
    from sklearn.linear_model import LinearRegression
    ols = LinearRegression()
    regressor = ols.fit(X_train,y_train)
    return regressor
    



def Predict_Grade(weights,target_Student_Grades):
    predictedGrade = np.dot(weights,target_Student_Grades)
    return predictedGrade


def Train_Model_Custom_Method():
    weights = []
    return weights


def Perform_All_Data_Steps(fileName):
    #filename = "C:\\Users\\aakash.chotrani\\Desktop\\GradientDescentGradePrediction\\DataExtraction\\TrainingData.csv"
    #numIterations = 5
    #alpha = 0.001
    X,y = Read_Dataset(fileName)
    X_train, y_train = Perform_Feature_Scaling(X,y)
    Model = Train_Model_Library_Method(X_train, y_train)
    return Model



def main():
    
    
    print("Gradient Descent File Main Message")
    
    
    
#    #Model = Train_Model_Library_Method(X, y)
#    
#    weights = np.array(Model.coef_)
#    print("Weights: ",weights)
#    normWeights = [float(i)/sum(weights) for i in weights]
#    print(normWeights)
#    normWeights =  np.sort(normWeights)
#    print('Sorted norm:',normWeights)
#    
#    target_Student_Grades = [88,88,82,87,85,0,84,85,85,75,94]
#    
#    predictedGrade = Predict_Grade(normWeights,target_Student_Grades)
#    
#    print("PredictedGrade: ",predictedGrade)


if __name__ == "__main__":
    main()



'''

def GradentDescent(X,y,Theta,alpha,m,numIterations):
    X_trans = X.transpose()
    print("X_transpose: ",X_trans)
    for i in range(0,numIterations):
        hypothesis = np.dot(X,Theta)
        loss = hypothesis - y
        cost = np.sum(loss ** 2)/(2*m)
        print("Iteration: ",i," | Cost: ", cost)
        print("Weights: ",Theta)
        gradient = np.dot(X_trans,loss)
        Theta = Theta - alpha*gradient
    return Theta
    


numIterations = 1000
alpha = 0.008
DataCsv = pd.read_csv("StudentData.csv")
X =DataCsv.iloc[:,:-1].values
y = DataCsv.iloc[:,3].values
Theta = np.array([0.1,0.5,0.8])
m = np.shape(X)
Theta = GradentDescent(X,y,Theta,alpha,m,numIterations)

student5 = [0.2,0.9,0.1]
predictedGrade = np.dot(Theta,student5)

print("PredictedGrade: ",predictedGrade)
'''