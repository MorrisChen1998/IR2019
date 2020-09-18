# -*- coding: utf-8 -*-
"""
Created on Fri Oct 4 21:45:32 2019

@author: morri
"""
#%% import library
import importData
import makeDictionary
import calculateDocLenNorm
import calculateTF
import calculateIDF
import printOutAnswer

from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import FeatureAgglomeration
import pandas as pd
import numpy as np
import time

#%% load file
start_time = time.time()
print('......loading file......')
#trainQueries,trainQueriesNeg,trainQueriesPos = importData.getTrainQueries()
#trainQueriesNeg.clear()
#trainQueries.clear()
testQueries = importData.getTestQueries()
docs = importData.getDocs()
print(time.time() - start_time)

#%% make dictionary
start_time = time.time()
print('......making the dictionary......')
dictionary = makeDictionary.createDictionary(testQueries,docs)
#docsWords = makeDictionary.getDocsWords()
#querysWords = makeDictionary.getQuerysWords()
print(time.time() - start_time)

#%% calculate document length normalization
start_time = time.time()
print('......calculating document length normalization......')
documentLengthNormalizations = calculateDocLenNorm.getDocumentLengthNormalization(docs)
print(time.time() - start_time)

#%% calculate TF
start_time = time.time()
print('......calculating TF......')
queryTF = calculateTF.getQueryTF(dictionary, testQueries)
#docTF = calculateTF.getDocumentTF(dictionary, docs)
#%%
totalTF = pd.concat([docTF, queryTF], axis=1, sort=False).transpose().values

print(time.time() - start_time)

#%% calculate IDF
start_time = time.time()
print('......calculating TFIDF......')
IDF = calculateIDF.getIDF(queryTF, docTF, dictionary)
#TFIDF = calculateIDF.getTFIDF(queryTF,docTF,IDF)

print(time.time() - start_time)

#%% calculate clustering
start_time = time.time()
print('......calculating clustering......')
group=256
#clustering = KMeans(n_clusters=group, random_state=0).fit(totalTF)
clustering = AgglomerativeClustering(n_clusters=group).fit(totalTF)
label = clustering.labels_.tolist()

print(time.time() - start_time)

#%% initial rocchio
dNumber = len(docTF.transpose().values)
qNumber = len(queryTF.transpose().values)
Rq=[]
for i in tqdm(group):
    Rq.append([j for j in range(dNumber) if(label[j]!=-1 and label[j]==i)]+\
               [q+dNumber for q in range(qNumber) if(label[q]!=-1 and label[q]==i)])

#%% Rocchio Algorithm, tuning the query
start_time = time.time()
print('......calculating Rocchio Algorithm......')
# tuning algorithm parameters
a = 0.5
b = 0.5
#
rocchioP_w_q = totalTF[dNumber:].astype(float)
for q in tqdm(qNumber):
    labelOfQuery = label[dNumber+q]
    RdOfQuery = [totalTF[Rq[labelOfQuery][j],:] for j in range(len(Rq[labelOfQuery]))]
    bpart = np.sum(RdOfQuery,axis=0)/len(Rq[labelOfQuery]) if len(RdOfQuery)>0 else rocchioP_w_q[q,:]
    rocchioP_w_q[q,:] *= a
    rocchioP_w_q[q,:] += (b * bpart)

rocchioQuery = {}
index = 0
for query in tqdm(queryTF):
    rocchioQuery[query]=rocchioP_w_q[index,:]
    index+=1

print(time.time() - start_time)

#%% calculate BM25
import calculateBM25
start_time = time.time()
print('......calculating BM25......')
# tuning model parameters
k1 = 1.5
k3 = 10
beta = 1
delta = 1.2
#
querysSim = calculateBM25.getSimilarity(k1, k3, beta, delta, documentLengthNormalizations,rocchioQuery, docTF, IDF)
print(time.time() - start_time)

#%% print out
start_time = time.time()
print('......print out answer......')
printOutAnswer.printOutAnswer(querysSim)
print(time.time() - start_time)
