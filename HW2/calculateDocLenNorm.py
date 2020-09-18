# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 23:55:05 2019

@author: morri
"""

def getDocumentLengthNormalization(docsWords):
    average = 0
    documentLengthNormalization = {}
    for doc in docsWords:
        average+=len(docsWords[doc])/len(docsWords)
        documentLengthNormalization[doc] = len(docsWords[doc])
    for doc in docsWords:
        documentLengthNormalization[doc]/=average
    return documentLengthNormalization