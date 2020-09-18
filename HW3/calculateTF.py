# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:37:47 2019

@author: morri
"""
import math
import pandas as pd
import numpy as np

def getQueryTF(dictionary, querysWords):
    queryTF = {}
    for queryWords in querysWords:
        queryTF[queryWords] = []
        for word in dictionary:
            queryTF[queryWords].append(querysWords[queryWords].count(word))
    return pd.DataFrame(data=queryTF)

def getDocumentTF(docCount, docsWords):
    docTF = {}
    for docWords in docsWords:
        docTF[docWords] = np.array(docCount[docWords])/len(docsWords[docWords])
    return pd.DataFrame(data=docTF)

def getDocumentCount(dictionary, docs):
    documentCount = {}
    for doc in docs:
        documentCount[doc] = []
        for word in dictionary:
            documentCount[doc].append(docs[doc].count(word))
    return pd.DataFrame(data=documentCount)

def getCollectionCount(dictionarySize, collection):
    collecitonCount = np.zeros(shape=(len(collection), dictionarySize))
    for doc in range(len(collection)):
        for word in range(len(collection[doc])):
            collecitonCount[doc][int(collection[doc][word])] += 1
        
    return collecitonCount

def getTFIDF(docCount,dictionary):
    IDF = []
    docTFinverse = docCount.transpose()
    for index in range(len(dictionary)):
        N = len(docTFinverse[index])
        ni = np.count_nonzero(docTFinverse[index].values)
        IDF.append(math.log(1+(N-ni+0.5)/(ni+0.5)))
        
    return np.transpose(docCount.values)*np.array(IDF)
