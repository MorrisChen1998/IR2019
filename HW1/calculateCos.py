# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:45:28 2019

@author: morri
"""
import operator
#from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#teacher said we can not use the "工具包", so...
def calculateCosineValue(q,dj):#parameters are vectors which present query's and doc's TFIDF
     return np.dot(q, dj) / (np.linalg.norm(q)*np.linalg.norm(dj))
        

def getSimilarity(docTFIDF, queryTFIDF):
    sim={}
    querysSim={}
    for query in queryTFIDF:
        for doc in docTFIDF:
#            sim[doc]=cosine_similarity(queryTFIDF[query].values.reshape(1,13353), docTFIDF[doc].values.reshape(1,13353))[0][0]
            sim[doc]=calculateCosineValue(queryTFIDF[query].values, docTFIDF[doc].values)
        querysSim[query] = sorted(sim.items(), key=operator.itemgetter(1),reverse=True)

    return querysSim;