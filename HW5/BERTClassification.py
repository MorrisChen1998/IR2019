# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:45:45 2019

@author: morri
"""
import time
import importData
import torch
import numpy as np
from tqdm import tqdm
import torch.nn.functional as F
from torch.utils.data import Dataset
from transformers import *
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

#%% load file
#start_time = time.time()
#print('......loading file......')
#trainQueryList = importData.getTrainQueryList()
#docList = importData.getDocList()
#testQueryList = importData.getTestQueryList()
#trainQueries = importData.getTrainQueries(trainQueryList)
#trainQueriesNeg = importData.getTrainNeg(trainQueryList)
#trainQueriesPos = importData.getTrainPos(trainQueryList)
#testQueries = importData.getTestQueries(testQueryList)
#docs = importData.getDocs(docList)
#print(time.time() - start_time)

#%%
start_time = time.time()
print('......data set......')
class IRDataset(Dataset):
    def __init__(self, mode, tokenizer):
        assert mode in ["trainQueries", "testQueries"]
        self.mode = mode
        self.trainQueryList = importData.getTrainQueryList()
        self.docList = importData.getDocList()
        self.testQueryList = importData.getTestQueryList()
        self.trainQueries = importData.getTrainQueries(self.trainQueryList)
        self.trainQueriesNeg = importData.getTrainNeg(self.trainQueryList)
        self.trainQueriesPos = importData.getTrainPos(self.trainQueryList)
        self.testQueries = importData.getTestQueries(self.testQueryList)
        self.docs = importData.getDocs(self.docList)
        self.tokenizer = tokenizer
        self.len = len(self.docList)
        
    # 定義回傳一筆訓練 / 測試數據的函式
    def __getitem__(self, qidx):
        tokens_tensors=[]
        label_tensors=[]
        if self.mode == "testQueries":
            label_tensor = None
            text_a = self.testQueries[qidx]
            #for didx in tqdm(range(6)):
            for didx in tqdm(range(len(self.docList))):
                text_b = self.docs[didx]
                tokens_tensor = self.getOneData(text_a,text_b)
                tokens_tensors.append(tokens_tensor)
                label_tensors.append(label_tensor)
        else:
            text_a = self.trainQueries[qidx]
            #for didx in tqdm(range(6)):
            for didx in tqdm(range(len(self.docList))):
                text_b = self.docs[didx]
                if(self.docList[didx] in self.trainQueriesPos[self.trainQueryList[qidx]]):
                    label_tensor = torch.tensor([1.])
                else:
                    if(self.docList[didx] in self.trainQueriesNeg[self.trainQueryList[qidx]]):
                        label_tensor = torch.tensor([-1.])
                    else:
                        label_tensor = torch.tensor([0.])
                tokens_tensor = self.getOneData(text_a,text_b)
                tokens_tensors.append(tokens_tensor)
                label_tensors.append(label_tensor)
        return (tokens_tensors, label_tensors)

    def __len__(self):
        return self.len
    
    def getOneData(self,text_a,text_b):
        tokens_tensor = self.tokenizer.encode("[CLS] " + text_a + " [SEP] " + text_b + " [SEP]")
        return torch.tensor([tokens_tensor])
    
tokenizer=BertTokenizer.from_pretrained('bert-base-uncased')
dataset = IRDataset("testQueries", tokenizer=tokenizer)
print(time.time() - start_time)

#%%
start_time = time.time()
print('......model......')
class SimpleBertIR(torch.nn.Module):
    def __init__(self):
        super(SimpleBertIR,self).__init__()
        self.bert=BertModel.from_pretrained('bert-base-uncased')
        self.Out_FC=torch.nn.Linear(768,1)
        
    def forward(self,_input_ids):
        outputs=self.bert(_input_ids.squeeze(1))
        CLS_representation=outputs[0][0][0]
        Pred_out=self.Out_FC(CLS_representation)
        return Pred_out
    
#%%
device = torch.device('cpu')
print("device:", device)
model=SimpleBertIR().to(device)
#model.train()
#
## 使用 Adam Optim 更新整個分類模型的參數
#optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
#
#EPOCHS = 10
#for qidx in tqdm(range(len(trainset.trainQueries))):
#    for epoch in range(EPOCHS):
#        tokens_tensors, label_tensors = trainset[qidx]
#        for didx in range(len(tokens_tensors)):
#            optimizer.zero_grad()
#            tokens_tensor = tokens_tensors[didx]
#            label_tensor = label_tensors[didx]
#            model_out=model(tokens_tensor.to(device))
#            MSEloss=torch.nn.MSELoss()
#            output=MSEloss(model_out,label_tensor.to(device))
#            output.backward()
#            optimizer.step()
#%%
model_out=[]
for qidx in tqdm(range(len(dataset.testQueries))):
    tokens_tensors, label_tensors = dataset[qidx]
    for didx in range(len(tokens_tensors)):
        model_out.append(model(tokens_tensors[didx].to(device)))








