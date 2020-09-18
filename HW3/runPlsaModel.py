# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 20:53:33 2019

@author: morri
"""
#%% import library
import importData
import makeDictionary
import calculateTF

import calculatePLSA
import printOutAnswer
import time
import numpy as np

#%%
def printTime(start_time):
    print("cost %.3f seconds"%(time.time() - start_time))
def printStartLine(task):
    print("......%s......"%task)

#%% load file
start_time = time.time()
printStartLine('loading file')
querys = importData.getQuerys()
docs = importData.getDocs()
BGs = importData.getBGs()
printTime(start_time)

#%% make dictionary
start_time = time.time()
printStartLine('making the dictionary')
dictionary = makeDictionary.createDictionary(querys,docs)
docs = makeDictionary.getDocsWords()
querys = makeDictionary.getQuerysWords()

docLengthList,docLengthDict = makeDictionary.getDocLengthList(docs)
printTime(start_time)

#%% calculate TF
start_time = time.time()
printStartLine('calculating TF')
docCount = calculateTF.getDocumentCount(dictionary,docs)
docTFIDF = calculateTF.getTFIDF(docCount,dictionary)
printTime(start_time)

#%% EM model training
start_time = time.time()
printStartLine('training EM model')
wNumber = len(dictionary) #13365
dNumber = len(docs) #2265
topicNum = 12
docTFIDF = docCount.transpose().values
# initialize
P_w_T = np.random.dirichlet(np.ones(wNumber),size= topicNum)
P_T_d = np.random.dirichlet(np.ones(topicNum),size= dNumber)
#P_w_T = np.ones((topicNum, wNumber))/wNumber
#P_T_d = np.ones((dNumber, topicNum))/topicNum


P_T_wd = np.zeros(shape=(topicNum, dNumber, wNumber))

## Estep
#sumP_Tk_wd = np.zeros(shape=(dNumber, wNumber))
#for k in range(topicNum):
#    for j in range(dNumber):
#        P_T_wd[k,j,:] = P_w_T[k,:] * P_T_d[j,k]
#    sumP_Tk_wd += P_T_wd[k,:,:]
#P_T_wd /= np.where(sumP_Tk_wd <= 1e-6, 1e-6, sumP_Tk_wd)
#
## Mstep
#for k in range(topicNum):
#    sumP_w_Tk = 0
#    for i in range(wNumber):
#        P_w_T[k,i] = np.dot(P_T_wd[k,:,i],docTFIDF[:,i])
#        sumP_w_Tk += P_w_T[k,i]
#    P_w_T[k,:] /= sumP_w_Tk if sumP_w_Tk > 1e-6 else 1e-6
#    for j in range(dNumber):
#        P_T_d[j,k] = np.dot(P_T_wd[k,j,:],docTFIDF[j,:]) / docLengthList[j]

def Estep():
    global P_T_wd
    sumP_Tk_wd = np.zeros(shape=(dNumber, wNumber))
    for k in range(topicNum):
        for j in range(dNumber):
            P_T_wd[k,j,:] = P_w_T[k,:] * P_T_d[j,k]
        sumP_Tk_wd += P_T_wd[k,:,:]
    P_T_wd /= np.where(sumP_Tk_wd <= 1e-12, 1e-12, sumP_Tk_wd)
           
def Mstep():
    global P_w_T
    global P_T_d
    for k in range(topicNum):
        sumP_w_Tk = 0
        for i in range(wNumber):
            P_w_T[k,i] = np.dot(P_T_wd[k,:,i],docTFIDF[:,i])
            sumP_w_Tk += P_w_T[k,i]
        P_w_T[k,:] /= sumP_w_Tk if sumP_w_Tk > 1e-12 else 1e-12
        for j in range(dNumber):
            P_T_d[j,k] = np.dot(P_T_wd[k,j,:],docTFIDF[j,:]) / docLengthList[j]

for train in range(5):
    train_time = time.time()
    print('...training %d gen...'%(train+1))
    Estep()
    Mstep()
    printTime(train_time)

printStartLine('training end')
printTime(start_time)

#%% calculate similarity
start_time = time.time()
printStartLine('calculating similarity between queries and documents')
a = 0.12
b = 0.03
querysSim = calculatePLSA.getSimilarity(a, b, dictionary, querys, docCount, docLengthDict, BGs, P_T_d, P_w_T)
printTime(start_time)

#%% print out answer file
start_time = time.time()
printStartLine('print out answer')
printOutAnswer.printOutAnswer(querysSim)
printTime(start_time)
