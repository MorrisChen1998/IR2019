# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 17:37:41 2019

@author: morri
"""
querys={}
docs={}
    
queryListDoc = open("query_list.txt",'r')
docListDoc = open("doc_list.txt",'r')
queryList=[]
docList=[]
    
for query in queryListDoc:
    queryList.append(query.strip())
    
for doc in docListDoc:
    docList.append(doc.strip())
        
queryListDoc.close()
docListDoc.close()
    
for query in queryList:
    queryDoc=open("Query/"+query,'r')
    querys[query]=queryDoc.read()
    queryDoc.close()
for doc in docList:
    docDoc=open("Document/"+doc,'r')
    docs[doc]=docDoc.read()
    docDoc.close()
    
def getQuerys():
    return querys;
def getDocs():
    return docs;
