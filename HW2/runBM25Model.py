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
import calculateBM25
import printOutAnswer
import time

#%% load file
start_time = time.time()
print('......loading file......')
querys = importData.getQuerys()
docs = importData.getDocs()
print(time.time() - start_time)

#%% make dictionary
start_time = time.time()
print('......making the dictionary......')
dictionary = makeDictionary.createDictionary(querys,docs)
docsWords = makeDictionary.getDocsWords()
querysWords = makeDictionary.getQuerysWords()
print(time.time() - start_time)

#%% calculate document length normalization
start_time = time.time()
print('......calculating document length normalization......')
documentLengthNormalizations = calculateDocLenNorm.getDocumentLengthNormalization(docsWords)
print(time.time() - start_time)

#%% calculate TF
start_time = time.time()
print('......calculating TF......')
queryTF = calculateTF.getQueryTF(dictionary,querysWords)
docTF = calculateTF.getDocumentTF(dictionary,docsWords)
print(time.time() - start_time)

#%% calculate IDF
start_time = time.time()
print('......calculating IDF......')
IDF = calculateIDF.getIDF(queryTF, docTF, dictionary)
print(time.time() - start_time)

#%% tuning model parameters
k1 = 1.5
k3 = 5
b = 1
delta = 0.8

#%% calculate BM25
start_time = time.time()
print('......calculating BM25......')
querysSim = calculateBM25.getSimilarity(k1, k3, b, delta, documentLengthNormalizations,queryTF, docTF, IDF)
print(time.time() - start_time)

#%% print out
start_time = time.time()
print('......print out answer......')
printOutAnswer.printOutAnswer(querysSim)
print(time.time() - start_time)
