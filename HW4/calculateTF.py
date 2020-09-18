# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:37:47 2019

@author: morri
"""
import pandas as pd
import numpy as np
import math

def getQueryCount(dictionary, querysWords):
    queryTF = {}
    for queryWords in querysWords:
        queryTF[queryWords] = []
        for word in dictionary:
            queryTF[queryWords].append(querysWords[queryWords].count(word))
    return pd.DataFrame(data=queryTF)

def getDocumentCount(dictionary, docs):
    documentCount = {}
    for doc in docs:
        documentCount[doc] = []
        for word in dictionary:
            documentCount[doc].append(docs[doc].count(word))
    return pd.DataFrame(data=documentCount)

def getC_w_dAndP_w_d(docCount,queryCount,docLengthList,queryLengthList):
    P_w_d = np.zeros(shape=(len(docLengthList)+len(queryLengthList), docCount.shape[0]))
    C_w_d = np.concatenate((docCount.transpose().values, queryCount.transpose().values))
    
    for j in range(len(docLengthList)):
        P_w_d[j,:] = C_w_d[j,:]/docLengthList[j]
    for j in range(len(queryLengthList)):
        P_w_d[len(docLengthList)+j,:] = C_w_d[len(docLengthList)+j,:]/queryLengthList[j]

    return C_w_d, P_w_d

def getIDF(queryTF, docTF, dictionary):
    docTFinverse=docTF.transpose()
    IDF = []
    for index in range(len(dictionary)):
        N = len(docTFinverse[index])
        ni = np.count_nonzero(docTFinverse[index].values)
        IDF.append(math.log(1+(N-ni+0.5)/(ni+0.5)))
    return IDF

def getP_w_q(queryCount,IDF):
    queryTFIDF={}
    for doc in queryCount:
        queryTFIDF[doc]=queryCount[doc]*IDF
    return pd.DataFrame(data=queryTFIDF).transpose().values

def getP_w_d(docCount,IDF):
    docTFIDF={}
    for doc in docCount:
        docTFIDF[doc]=docCount[doc]*IDF
    return pd.DataFrame(data=docTFIDF).transpose().values
