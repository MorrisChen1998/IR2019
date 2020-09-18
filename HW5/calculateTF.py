# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 19:37:47 2019

@author: morri
"""
from tqdm import tqdm

import pandas as pd

def getQueryTF(dictionary, querysWords):
    queryTF = {}
    for queryWords in tqdm(querysWords):
        queryTF[queryWords] = []
        for word in range(len(dictionary)):
            queryTF[queryWords].append(querysWords[queryWords].count(dictionary[word]))
    return pd.DataFrame(data=queryTF)

def getDocumentTF(dictionary, docsWords):
    docTF = {}
    for docWords in tqdm(docsWords):
        docTF[docWords] = []
        for word in range(len(dictionary)):
            docTF[docWords].append(docsWords[docWords].count(dictionary[word]))
    return pd.DataFrame(data=docTF)
