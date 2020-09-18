# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:30:17 2019

@author: morri
"""

querysWords={}
docsWords={}
dictionary=[]

def createDictionary(querys,docs):
    for query in querys:
        words=querys[query].replace('-1\n', '').split(' ')
        querysWords[query]=words
        for word in words:
            if word not in dictionary and word is not '':
                dictionary.append(word)

    for doc in docs:
        words=docs[doc].split('\n',3)[3].replace('-1\n', '').split(' ')
        docsWords[doc]=words
        for word in words:
            if word not in dictionary and word is not '':
                dictionary.append(word)
                
    return dictionary;

def getQuerysWords():
    return querysWords;
def getDocsWords():
    return docsWords;
