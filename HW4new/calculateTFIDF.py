# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 00:23:47 2019

@author: morri
"""

def getDocTFIDF(docTF,IDF):
    docTFIDF={}
    for doc in docTF:
        docTFIDF[doc]=docTF[doc]*IDF
    return docTFIDF;

def getQueryTFIDF(queryTF,IDF):
    queryTFIDF={}
    for doc in queryTF:
        queryTFIDF[doc]=queryTF[doc]*IDF
    return queryTFIDF;