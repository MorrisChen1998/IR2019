# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:37:47 2019

@author: morri
"""

import pandas as pd
import math

def logNormalization(tf):
    return math.log(tf+1,2)

def getQueryTF(dictionary, querysWords):
    queryTF = {}
    for queryWords in querysWords:
        queryTF[queryWords] = []
        for word in dictionary:
            queryTF[queryWords].append(logNormalization(querysWords[queryWords].count(word)))
        
    return pd.DataFrame(data=queryTF)

def getDocumentTF(dictionary, docsWords):
    docTF = {}
    for docWords in docsWords:
        docTF[docWords] = []
        for word in dictionary:
            docTF[docWords].append(logNormalization(docsWords[docWords].count(word)))
        
    return pd.DataFrame(data=docTF)
