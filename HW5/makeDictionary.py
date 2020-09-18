# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:30:17 2019

@author: morri
"""
from tqdm import tqdm
querysWords={}
docsWords={}
dictionary=[]

def createDictionary(querys,docs):
    for query in tqdm(querys):
        for word in querys[query]:
            if word not in dictionary and word is not '':
                dictionary.append(word)

    for doc in tqdm(docs):
        for word in docs[doc]:
            if word not in dictionary and word is not '':
                dictionary.append(word)
                
    return dictionary;

def getQuerysWords():
    return querysWords;
def getDocsWords():
    return docsWords;
