# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:13:32 2019

@author: morri
"""

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
from sklearn.cluster import KMeans

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
printStartLine('calculating TFIDF')
docCount = calculateTF.getDocumentCount(dictionary,docs)
queryCount = calculateTF.getQueryCount(dictionary, querys)

#IDF = calculateTF.getIDF(queryCount, docCount, dictionary)
#P_w_d = calculateTF.getP_w_d(docCount, IDF)
#P_w_q = calculateTF.getP_w_q(queryCount, IDF)
    
printTime(start_time)

#%% clean memory
docs={}
querys={}
#----I think it's same meaning to center of kmeans----
#Rq=[]
#RqReversed=[]
#for i in range(len(center)):
#    Rq.append([j for j in range(len(P_w_d)) if(label[j]==i)]+[q+len(P_w_q) for q in range(len(P_w_q)) if(label[q]==i)])
#    #RqReversed.append([j for j in range(len(P_w_d)) if(label[j]!=i)]+[q+len(P_w_q) for q in range(len(P_w_q)) if(label[q]!=i)])
#    
##%% Rocchio Algorithm
#start_time = time.time()
#printStartLine('calculating kmeans clustering')
#a = 1
#b = 0.75
##r = 0.15
#rocchioP_w_q = P_w_q
#for q in range(len(P_w_q)):
#    labelOfQuery = label[len(P_w_d)+q]
#    apart = P_w_q[q,:]
#    RdOfQuery = [P_w_d[Rq[labelOfQuery][j],:] for j in range(len(Rq[labelOfQuery]))]
#    bpart = np.sum(RdOfQuery,axis=0)/len(Rq[labelOfQuery])
#    #rpart = P_w_d
#    rocchioP_w_q[q,:] = a * apart + b * bpart# - r * rpart
#printTime(start_time)

#%% calculate kmeans clustering
start_time = time.time()
printStartLine('calculating kmeans clustering')
kmeans = KMeans(n_clusters=36, random_state=0).fit(np.concatenate((docCount.transpose().values, queryCount.transpose().values)))

center = kmeans.cluster_centers_
label = kmeans.labels_.tolist()

printTime(start_time)

#%% EM model training
start_time = time.time()
printStartLine('training EM model')
wordCount = np.concatenate((docCount.transpose().values, queryCount.transpose().values))
dictionaryBG = np.array([np.exp(BGs[dictionary[i]]) for i in range(len(dictionary))])
wNumber = len(dictionary)
dNumber = len(wordCount)

a = 0.3
b = 0.3
# initialize
C_w_d,P_w_d = calculateTF.getC_w_dAndP_w_d(docCount,queryCount,docLengthList,queryLengthList)
P_Ttmm_w = center

P_Ttmm_wd = np.zeros(shape=(dNumber, wNumber))
P_T_wd = np.zeros(shape=(dNumber, wNumber))

#%% EM
def Estep():
    global P_Ttmm_wd
    global P_T_wd
    for j in range(dNumber):
        S = label[j]
        P_Ttmm_wd[j,:] = C_w_d[j,:]*P_Ttmm_w[S,:]*(1-a-b)/(P_Ttmm_w[S,:]*(1-a-b) + P_w_d[j,:]*a + dictionaryBG*b)
        P_T_wd[j,:] = C_w_d[j,:]*P_w_d[j,:]*a/(P_Ttmm_w[S,:]*(1-a-b) + P_w_d[j,:]*a + dictionaryBG*b)
def Mstep():
    global P_Ttmm_w
    global P_w_d
    sumP_Ttmm_w = 0
    sumP_w_d = np.zeros(shape=(dNumber))
    for k in range(len(P_Ttmm_w)):
        for i in range(wNumber):
            P_Ttmm_w[k,i] = np.sum(P_Ttmm_wd[:,i])
            sumP_Ttmm_w += P_Ttmm_w[k,i]
        P_Ttmm_w[k,:] /= sumP_Ttmm_w# if sumP_Ttmm_w > 1e-12 else 1e-12
        
    for i in range(wNumber):
        P_w_d[:,i] = P_T_wd[:,i]
        sumP_w_d += P_w_d[:,i]
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
