# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:03:42 2019

@author: morri
"""
import re
reCompiler = re.compile("[^a-z^A-Z^0-9^ ]")

def getTrainQueryList():
    queryListDoc = open("train/query_list.txt",'r')
    queryList=[]
    for query in queryListDoc:
        queryList.append(query.strip())
    queryListDoc.close()
    return queryList

def getTrainQueries(queryList):
    queries=[]
    for query in range(len(queryList)):
        queryQuery=open("train/query/"+queryList[query],'r')
        queries.append(reCompiler.sub('', queryQuery.read()))
        queryQuery.close()
    return queries

def getTrainNeg(queryList):
    negDoc = open("train/Neg.txt",'r')
    negs = {}
    for query in queryList:
        negs[query]=[]
    for neg in negDoc:
        neg = neg.strip().split(' ')
        negs[neg[0]].append(neg[1])
    negDoc.close()
    return negs

def getTrainPos(queryList):
    posDoc = open("train/Pos.txt",'r')
    poses = {}
    for query in queryList:
        poses[query]=[]
    for pos in posDoc:
        pos = pos.strip().split(' ')
        poses[pos[0]].append(pos[1])
    posDoc.close()
    return poses

def getTestQueryList():
    queryListDoc = open("test/query_list.txt",'r')
    queryList=[]
    for query in queryListDoc:
        queryList.append(query.strip())
    queryListDoc.close()
    return queryList

def getTestQueries(queryList):
    queries=[]
    for query in range(len(queryList)):
        queryQuery=open("test/query/"+queryList[query],'r')
        queries.append(reCompiler.sub('', queryQuery.read()))
        queryQuery.close()
    return queries
        
def getDocList():
    docListDoc = open("doc/hw5.txt",'r')
    docList=[]
    for doc in docListDoc:
        docList.append(doc.strip())
    docListDoc.close()
    return docList

def getDocs(docList):
    docs=[]
    for doc in range(len(docList)):
        docDoc=open("doc/"+docList[doc],'r')
        docs.append(reCompiler.sub('', docDoc.read()))
        docDoc.close()
    return docs