# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:39:45 2019

@author: morri
"""
import datetime


def printOutAnswer(querysSim):
    file= open(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")+"answer.txt","w+")
    #file = open("answer.txt", "w+")
    file.write("Query,RetrievedDocuments\n")
    for query in querysSim:
        file.write("%s," % query)
        for doc in range(len(querysSim[query])):
            file.write(" %s" % querysSim[query][doc][0])
        file.write("\n")
    file.close()
