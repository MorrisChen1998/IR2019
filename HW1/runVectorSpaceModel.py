# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:16:46 2019

@author: morri
"""
#%% import library
import importData
import makeDictionary
import calculateTF
import calculateIDF
import calculateTFIDF
import calculateCos
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

#%% calculate TF-IDF
start_time = time.time()
print('......calculating TF-IDF......')
queryTFIDF = calculateTFIDF.getQueryTFIDF(queryTF,IDF)
docTFIDF = calculateTFIDF.getDocTFIDF(docTF,IDF)
print(time.time() - start_time)

#%% calculate similarity
start_time = time.time()
print('......calculating similarity between queries and documents......')
querysSim = calculateCos.getSimilarity(docTFIDF, queryTFIDF)
print(time.time() - start_time)

#%% print out
start_time = time.time()
print('......print out answer......')
printOutAnswer.printOutAnswer(querysSim)
print(time.time() - start_time)
