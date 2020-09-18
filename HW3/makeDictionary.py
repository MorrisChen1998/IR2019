# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:30:17 2019

@author: morri
"""
querysWords={}
docsWords={}
dictionary=[]
collectionList=[]

def createDictionary(querys,docs):#, collection):
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

#    for doc in range(len(collection)):
#        collectionList.append(collection[doc].split(' '))
#        collectionList[doc] = [i for i in collectionList[doc] if i]
#        for word in collectionList[doc]:
#            if word not in dictionary and word is not '':
#                dictionary.append(word)
    return dictionary;

def getQuerysWords():
    for query in querysWords:
        while(querysWords[query][len(querysWords[query])-1] == '' or \
              querysWords[query][len(querysWords[query])-1] == '-1' or \
              querysWords[query][len(querysWords[query])-1] == '\n'):
            querysWords[query].pop()
    return querysWords

def getDocsWords():
   for doc in docsWords:
       while(docsWords[doc][len(docsWords[doc])-1] == '' or \
             docsWords[doc][len(docsWords[doc])-1] == '-1' or \
             docsWords[doc][len(docsWords[doc])-1] == '\n'):
           docsWords[doc].pop()
   return docsWords

def getCollectionList():
   return collectionList

#def getCollectionLengthList(collection):
#    collectionLengthList = []
#    for doc in range(len(collection)):
#        collectionLengthList.append(len(collection[doc]))
#    return collectionLengthList
        
def getDocLengthList(docs):
    docLengthList = []
    docLengthDict = {}
    for doc in docs:
        docLengthDict[doc] = {}
        docLengthDict[doc]['docLength'] = len(docs[doc])
        docLengthDict[doc]['docIndex'] = len(docLengthList)
        docLengthList.append(len(docs[doc]))
    return docLengthList,docLengthDict
    