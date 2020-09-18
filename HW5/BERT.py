# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 03:25:21 2019

@author: morri
"""
import time
import torch
import math
from tqdm import tqdm
from transformers import *
from torch.utils.data import DataLoader
from IPython.display import clear_output

import importData
#%% load file
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
tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')

#%%
tokens_tensors = []

for q in tqdm(range(len(trainQueries))):
    for d in range(len(docs)):
        text_a = trainQueries[q]
        text_b = docs[d]
        tokens_tensor = tokenizer.encode(text_b, add_special_tokens=False)
        
        separate = math.ceil(len(tokens_tensor)/499)
        for i in range(separate):
            tokens_tensors.append(tokenizer.encode(text_a + "[SEP]" + tokenizer.decode(tokens_tensor[i*499:(i+1)*499])))

for q in tqdm(range(len(testQueries))):
    for d in range(len(docs)):
        text_a = testQueries[q]
        text_b = docs[d]
        tokens_tensor = tokenizer.encode(text_b, add_special_tokens=False)
        
        separate = math.ceil(len(tokens_tensor)/499)
        for i in range(separate):
            tokens_tensors.append(tokenizer.encode(text_a + "[SEP]" + tokenizer.decode(tokens_tensor[i*499:(i+1)*499])))
            
#%%
#
#class SimpleBertIR(torch.nn.Module):
#    def __init__(self):
#        super(SimpleBertIR,self).__init__()
#        self.bert=BertModel.from_pretrained('bert-base-uncased')
#        self.Out_FC=torch.nn.Linear(768,1)
#        
#    def forward(self,_input_ids):
#        outputs=self.bert(_input_ids.squeeze(1))
#        CLS_representation=outputs[0][0][0]
#        Pred_out=self.Out_FC(CLS_representation)
#        return Pred_out
##%%
#PosAns=torch.tensor([1.]).to(device)
#NegAns=torch.tensor([0.]).to(device)
#
#model=SimpleBertIR().to(device)
##model.train()
#
##%%
#for query in tqdm(testQueries):
#    #inputArray=[]
#    electable=[]
#    model_out=[]
#    for doc in docs:
#        bertInput = testQueries[query]+docs[doc][1:]
#        if(len(bertInput)<=512):
#            #inputArray.append(bertInput)
#            #electable.append(doc)#, PosAns if doc in trainQueriesPos[query] else NegAns])
#            model_out.append(model(torch.tensor([bertInput]).to(device)))
#
#
##x_input_ids=torch.tensor(inputArray).to(device)
##model_out=model(x_input_ids)
##optimizerSGD=torch.optim.SGD(model.parameters(),lr=0.001,momentum=0.9)
##MSEloss=torch.nn.MSELoss()
##ans=PosAns
##output=MSEloss(model_out,NegAns)
##output.backward()
##optimizerSGD.step()
##optimizerSGD.zero_grad()
#model_out
