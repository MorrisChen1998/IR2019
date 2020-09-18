# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 00:15:21 2019

@author: morri
"""
import math
import time
import importData
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# %% load file
start_time = time.time()
print('......loading file......')
trainQueryList = importData.getTrainQueryList()
docList = importData.getDocList()
testQueryList = importData.getTestQueryList()
trainQueries = importData.getTrainQueries(trainQueryList)
trainQueriesNeg = importData.getTrainNeg(trainQueryList)
trainQueriesPos = importData.getTrainPos(trainQueryList)
testQueries = importData.getTestQueries(testQueryList)
docs = importData.getDocs(docList)
print(time.time() - start_time)

# %%
DOC_LEN_BATCH = 450

query = trainQueries[0]
tokens_tensors = []
i = 0
for d in range(len(docs)):
    document = docs[d].split()
    stream = math.ceil(len(document)/DOC_LEN_BATCH)
    myBatch = math.ceil(len(document)/stream) if stream > 0 else len(document)

    for i in range(stream):
        doc_segment = ' '.join(document[i*myBatch:(i+1)*myBatch])
        tokens_tensor = tokenizer.encode(query + " [SEP] " + doc_segment)
        if(len(tokens_tensor) > 510):
            i += 1
        tokens_tensors.append(tokens_tensor)
i
# %%
import datetime
import json
with open('answer12080057.json', 'r') as reader:
    jf = json.loads(reader.read())

fileName = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")+"answer.txt"
file = open(fileName, "w+")
file.write("Query,RetrievedDocuments\n")
for query in jf:
    file.write("%s," % query)
    for doc in range(0, len(jf[query]), 2):
        file.write(" %s" % jf[query][doc])
    file.write("\n")
file.close()
