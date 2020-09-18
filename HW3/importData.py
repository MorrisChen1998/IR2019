# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 17:37:41 2019

@author: morri
"""    
def getQuerys():
    querys={}
    queryListDoc = open("query_list.txt",'r')
    queryList=[]
    for query in queryListDoc:
        queryList.append(query.strip())
    queryListDoc.close()
    for query in queryList:
        queryDoc=open("Query/"+query,'r')
        querys[query]=queryDoc.read()
        queryDoc.close()
    return querys

def getDocs():
    docs={}
    docListDoc = open("doc_list.txt",'r')
    docList=[]
    for doc in docListDoc:
        docList.append(doc.strip())
    docListDoc.close()
    for doc in docList:
        docDoc=open("Document/"+doc,'r')
        docs[doc]=docDoc.read()
        docDoc.close()
    return docs

def getBGs():
    BGs={}
    BGListDoc = open("BGLM.txt",'r')
    BGList = []
    for BG in BGListDoc:
        BGList.append(BG.strip())
    BGListDoc.close()
    for BG in BGList:
        BG = BG.split("   ")
        BGs[BG[0]] = float(BG[1])
    return BGs

def getCollection():
    collectionDoc = open("collection.txt",'r')
    collectionList = []
    for collection in collectionDoc:
        collectionList.append(collection.strip())
    collectionDoc.close()
    return collectionList