# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:45:28 2019

@author: morri
"""
import operator
import numpy as np

def calculateCosineValue(q,dj):
     return np.dot(q, dj) / (np.linalg.norm(q)*np.linalg.norm(dj))

def getSimilarity(P_w_d, docName, queryName):
    sim={}
    querysSim={}
    for q in range(len(queryName)):
        for j in range(len(docName)):
            sim[docName[j]]=calculateCosineValue(P_w_d[len(docName)+q], P_w_d[j])
        querysSim[queryName[q]] = sorted(sim.items(), key=operator.itemgetter(1),reverse=True)[:50]
        print('query %d/800'%q)
    return querysSim;