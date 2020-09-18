# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 21:42:43 2019

@author: morri
"""

import operator
'''
k1, k3, b, delta, DLN = constant
DLN = document length normalization
'''
import numpy as np

def calculateBM25(k1, k3, b, delta, DLN, TFq, TFj, IDF):
    TFpron = np.array(TFj)/(1-b+b*DLN)+delta
    F = (k1+1)*TFpron/(k1+TFpron)
    TF = (k3+1)*TFq/(k3+TFq)
    SIMbm25 = np.sum(F*TF*np.array(IDF))
    return SIMbm25
  

def getSimilarity(k1, k3, b, delta, DLNs, queryTF, docTF, IDF):
    sim={}
    querysSim={}
    index = 0
    for query in queryTF:
        for doc in docTF:
            sim[doc]=calculateBM25(k1, k3, b, delta, DLNs[doc], queryTF[query], docTF[doc].values, IDF)
        querysSim[query] = sorted(sim.items(), key=operator.itemgetter(1),reverse=True)[:50]
        index+=1
        print('query %d/800'%index)
    return querysSim
