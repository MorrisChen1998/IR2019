# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 23:40:53 2019

@author: morri
"""
#%% import library
import importData
import makeDictionary
import calculateTF
import calculateCos
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

docLengthList = makeDictionary.getDocLengthList(docs)
queryLengthList = makeDictionary.getQueryLengthList(querys)
printTime(start_time)

#%% calculate TF
start_time = time.time()
printStartLine('calculating TF')
docCount = calculateTF.getDocumentCount(dictionary,docs)
queryCount = calculateTF.getQueryCount(dictionary, querys)

printTime(start_time)

#%% clean memory
docs={}
querys={}

#%% EM model training
start_time = time.time()
printStartLine('training EM model')
wordCount = np.concatenate((docCount.transpose().values, queryCount.transpose().values))
dictionaryBG = np.array([np.exp(BGs[dictionary[i]]) for i in range(len(dictionary))])
wNumber = len(dictionary)
dNumber = len(wordCount)

a = 0.4
b = 0.5
# initialize
C_w_d,P_w_d = calculateTF.getC_w_dAndP_w_d(docCount,queryCount,docLengthList,queryLengthList)

P_Ttmm_w = np.random.dirichlet(np.ones(wNumber),size= 1)
P_Ttmm_wd = np.zeros(shape=(dNumber, wNumber))
P_T_wd = np.zeros(shape=(dNumber, wNumber))

#%%
def Estep():
    global P_Ttmm_wd
    global P_T_wd
    for j in range(dNumber):
        P_Ttmm_wd[j,:] = C_w_d[j,:]*P_Ttmm_w[0,:]*(1-a-b)/(P_Ttmm_w[0,:]*(1-a-b) + P_w_d[j,:]*a + dictionaryBG*b)
        P_T_wd[j,:] = C_w_d[j,:]*P_w_d[j,:]*a/(P_Ttmm_w[0,:]*(1-a-b) + P_w_d[j,:]*a + dictionaryBG*b)
def Mstep():
    global P_Ttmm_w
    global P_w_d
    sumP_Ttmm_w = 0
    sumP_w_d = np.zeros(shape=(dNumber))
    
    for i in range(wNumber):
        P_Ttmm_w[0,i] = np.sum(P_Ttmm_wd[:,i])
        sumP_Ttmm_w += P_Ttmm_w[0,i]
        
        P_w_d[:,i] = P_T_wd[:,i]
        sumP_w_d += P_w_d[:,i]
        
    P_Ttmm_w[0,:] /= sumP_Ttmm_w# if sumP_Ttmm_w > 1e-12 else 1e-12
    for i in range(wNumber):
       P_w_d[:,i] /= sumP_w_d# if sumP_w_d > 1e-12 else 1e-12
        
for train in range(10):
    train_time = time.time()
    print('...training %d gen...'%(train+1))
    Estep()
    Mstep()
    printTime(train_time)

printStartLine('training end')
printTime(start_time)

#%% calculate similarity

start_time = time.time()
print('......calculating similarity between queries and documents......')
querysSim = calculateCos.getSimilarity(P_w_d, list(docCount.columns.values), list(queryCount.columns.values))
print(time.time() - start_time)

#%% print out answer file
start_time = time.time()
printStartLine('print out answer')
printOutAnswer.printOutAnswer(querysSim)
printTime(start_time)
