# -*- coding: utf-8 -*-
"""
Created on Fri Nov 01 13:45:28 2019

@author: morri
"""
import numpy as np
import operator

def calculatePLSA(a, b, dictionary, queryWords, docWordCount, docLengthIndex, BGs, P_T_d, P_w_T):
    P_q_d = 0
    for word in range(len(queryWords)):
        wordIndex = dictionary.index(queryWords[word])
        docIndex = docLengthIndex['docIndex']
        sigma = docWordCount[wordIndex] / docLengthIndex['docLength']
        a_part = np.log(sigma if sigma > 1e-24 else 1e-24) + np.log(a)
        sigma = np.dot(P_w_T[:,wordIndex],P_T_d[docIndex,:])
        b_part = np.log(sigma if sigma > 1e-24 else 1e-24) + np.log(b)
        c_part = BGs[queryWords[word]] + np.log(1-a-b)

        P_q_d += np.log(np.exp(a_part) + np.exp(b_part) + np.exp(c_part))
    
    return P_q_d

def getSimilarity(a, b, dictionary, querysWords, docCount, docLengthDict, BGs, P_T_d, P_w_T):
    sim={}
    querysSim={} 
    for query in querysWords:
        for doc in docCount:
            sim[doc] = calculatePLSA(a, b, dictionary, querysWords[query], docCount[doc], docLengthDict[doc], BGs, P_T_d, P_w_T)
        querysSim[query] = sorted(sim.items(), key=operator.itemgetter(1),reverse=True)
        print('calculate %s finished'%query)
    return querysSim;