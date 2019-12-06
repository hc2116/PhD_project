#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:00:52 2019

@author: henry
"""

import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch import optim
#import time
import random
print(torch.cuda.is_available())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device")

inputs_Noise_50_Chaff=pd.read_csv('DeepCorr_Data/noise_50_Chaff.txt',header=None,sep=";")    

Seqs1=inputs_Noise_50_Chaff.iloc[:,3:(2403)]


SOS_token=0
EOS_token=1

input_seqs = packet_seq_loader(Seqs1,600, SOS_token, EOS_token)
input_seqs.combine_direction_size()

class packet_seq_loader:
    def __init__(self, packet_seq, n_packets, SOS_token, EOS_token):
        self.packet_seq = packet_seq
        self.directions = []
        self.n_packets = n_packets
        self.index2packet = {0: "SOS", 1: "EOS"}
        self.packet2count = {}
        self.packet2index = {"SOS":0, "EOS":1}
        self.alphabet_size = 2
        self.SOS_token = SOS_token
        self.EOS_token = EOS_token
        
    def addpacket(self, packet, count):
        if packet not in self.packet2index:
            self.packet2index[packet] = self.alphabet_size
            self.packet2count[packet] = count
            self.index2packet[self.alphabet_size] = packet
            self.alphabet_size += 1
        else:
            self.packet2count[packet] += 1
            
    def combine_direction_flags(self):
        directions_index= [x for x in range(0,4*self.n_packets,4)]
        flags_index= [x for x in range(12,12+5*self.n_packets,4)]
        self.directions=self.packet_seq.iloc[:,directions_index]
        flags=self.packet_seq.iloc[:,flags_index]
        flags.columns=self.directions.columns
        self.directions=self.directions+'_'+flags

        alphabet_values=pd.Series(pd.value_counts(self.directions.values.ravel('K')))
        alphabet = alphabet_values.index

        for i in range(len(alphabet)):
            self.addpacket(alphabet[i],alphabet_values[i])

    def combine_direction_size(self,q=[0.025,0.05,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.35,0.4,0.45,
                                                     0.5,0.55,0.6,0.65,0.7,0.75,0.85]):
        directions_index= [x for x in range(0,4*self.n_packets,4)]
        #flags_index= [x for x in range(12,12+5*self.n_packets,5)]
        size_index= [x for x in range(1,1+4*self.n_packets,4)]
        self.directions=self.packet_seq.iloc[:,directions_index]
        #flags=self.packet_seq.iloc[:,flags_index]
        sizes=self.packet_seq.iloc[:,size_index]
        #flags.columns=self.directions.columns        
        sizes.columns=self.directions.columns
        sizes2=[]
        for i in range(self.n_packets):
            sizes2.extend(sizes.iloc[:,i].values)
        xxxx=pd.DataFrame(data=sizes2).loc[:,0]
        xxx=pd.DataFrame(data=sizes2).loc[:,0].value_counts()/len(sizes2)
        ImpValues=list((xxx.loc[xxx>0.005]).index)
        ImpValues=ImpValues[0:9]
        sizes3=sizes.astype(str)
        Quantvaluestemp=list(np.quantile(xxxx.loc[~(xxxx.isin(ImpValues))].values, 
                                                  q))
        Quantvalues=[0]
        Quantvalues.extend(Quantvaluestemp)
        sizenames=sizes.columns
        for i in range(self.n_packets):
            for j in range(len(Quantvalues)-1):
                sizes3.loc[(~sizes.iloc[:,i].isin(ImpValues))&
                                   (sizes.iloc[:,i]>Quantvalues[j])&
                                   (sizes.iloc[:,i]<Quantvalues[j+1]),sizenames[i]]="<="+str(Quantvalues[j+1])
        self.directions=self.directions+'_'+'_'+sizes3
        self.directions=self.directions.reset_index(drop=True)
        alphabet_values=pd.Series(pd.value_counts(self.directions.values.ravel('K')))
        alphabet = alphabet_values.index
        for i in range(len(alphabet)):
            self.addpacket(alphabet[i],alphabet_values[i])

    def indexesFromSeq(self,seq):
        return [self.packet2index[packet] for packet in seq]

    def tensorFromSentence(self,rows):
        seq=self.directions.iloc[rows,:]
        if len(seq.shape)==2:
            batch_size=seq.shape[0]
        else:
            batch_size=1
        if batch_size==1:
            if len(seq.shape)==2:
                index_seq = self.indexesFromSeq(seq.iloc[0,:])
            else:
                index_seq = self.indexesFromSeq(seq)
            input_seq = index_seq
            target_seq = [self.SOS_token]
            input_seq.append(self.EOS_token)
            target_seq.extend(index_seq)
        else:
            target_seq = []
            input_seq = []
            for i in range(batch_size):
                indexes = self.indexesFromSeq(seq.iloc[i,:])
                targets=[SOS_token]
                targets.extend(indexes)
                target_seq.append(targets)
                indexes.append(self.EOS_token)
                input_seq.append(indexes)
        return torch.tensor(input_seq, dtype=torch.long, device=device).view(1, batch_size,-1), torch.tensor(target_seq, dtype=torch.long, device=device).view(1, batch_size,-1)



class ChaffNetbidirect(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, n_layers, batch_size ,dropout):
        super(ChaffNetbidirect, self).__init__()
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.n_layers
        self.embedding = nn.Embedding(input_size, embedding_size)
        self.inputLin = nn.Sequential(nn.Linear(embedding_size, embedding_size), nn.ReLU(inplace=True))
        self.LSTM = nn.LSTM(embedding_size, hidden_size,n_layers, 
                            dropout = dropout, bidirectional = True)
        
        #self.bi2onehidden = nn.Linear(hidden_size * 2, hidden_size)
        #self.bi2onecell = nn.Linear(hidden_size * 2, hidden_size)
        self.dropout = nn.Dropout(dropout)
        
        # Initialise forget gate bias to 1
        for names in self.LSTM._all_weights:
            for name in filter(lambda n: "bias" in n,  names):
                bias = getattr(self.LSTM, name)
                n = bias.size(0)
                start, end = n//4, n//2
                bias.data[start:end].fill_(1.)

    def forward(self, input_tensor):

        embedded = self.dropout(self.inputLin(self.embedding(input_tensor)))
        output, (hidden, cell) = self.LSTM(embedded)
                
        print(output)
        #hidden = torch.tanh(self.bi2onehidden(torch.cat((hidden[1,:,:], hidden[0,:,:]), dim = 1)))
        #cell = torch.tanh(self.bi2onecell(torch.cat((cell[0,:,:], cell[1,:,:]), dim = 1)))
        
        return output




def trainBatch(input_tensor, labels,
               ChaffNet, ChaffNet_optimizer, criterion, train=True):
#    batch_size = inputs1.size(0)
    
    ChaffNet_output = ChaffNet(input_tensor)
    loss = criterion(ChaffNet_output.squeeze(), labels)
    #####################################################
    #####################################################

    if train==True:
        ChaffNet_optimizer.zero_grad()
        loss.backward()
        ChaffNet_optimizer.step()
    return ChaffNet_output, loss.item()




def trainIters(ChaffNet, inputs, batch_size, n_packets=300,train=True,
               learning_rate=0.01, weight_decay=5e-4,Printer=True):
    #start = time.time()
    loss_total = 0  
    all_losses = []
    outputs=[]
    ##########################################################
    n_data=inputs.shape[0]
    if batch_size==0:
        batch_size=n_data
    n_iters = int(np.floor(n_data/batch_size))
    input_indices1=[x for x in range(0,2*n_packets)]
    input_indices2=[x for x in range(2*n_packets,4*n_packets)]
    input_indices3=[x for x in range(4*n_packets,6*n_packets)]
    input_indices4=[x for x in range(6*n_packets,8*n_packets)]
    labels_index = 8*n_packets
    
    ##########################################################
    if train==True:
        ChaffNet.train()
    else:
        ChaffNet.eval()
        iter_indexes=[x*batch_size for x in range(0,n_iters+1)]
        if iter_indexes[n_iters]!=n_data:
            n_iters+=1
            iter_indexes.append(n_data)
    ChaffNet_optimizer = optim.Adam(ChaffNet.parameters(), lr=learning_rate, weight_decay=weight_decay)
    criterion = nn.BCEWithLogitsLoss()
    #########################################################
    printtoken=10
    for iteration in range(1, n_iters + 1):
        if (iteration%printtoken==0):
            if Printer==True:
                print('iteration='+str(iteration))
            if iteration==(printtoken*10):
                printtoken=printtoken*10
        
        if train==True:
            input_samples = random.sample(range(0, n_data), int(n_iters*batch_size))
            batch_index = input_samples[((iteration-1)*batch_size):(iteration*batch_size)]
        else:
            batch_index = [x for x in range(iter_indexes[iteration-1],iter_indexes[iteration])]
            batch_size=len(batch_index)
        input1 = torch.tensor(inputs.iloc[batch_index,input_indices1].values,device=device).view(batch_size,1,2,-1)
        input2 = torch.tensor(inputs.iloc[batch_index,input_indices2].values,device=device).view(batch_size,1,2,-1)
        input3 = torch.tensor(inputs.iloc[batch_index,input_indices3].values,device=device).view(batch_size,1,2,-1)
        input4 = torch.tensor(inputs.iloc[batch_index,input_indices4].values,device=device).view(batch_size,1,2,-1)
        labels =  torch.tensor(inputs.iloc[batch_index,labels_index].values,dtype=torch.float32, device=device)
        
        ChaffNet_output, loss = trainBatch(input1, input2, input3, input4, labels,
                     ChaffNet, ChaffNet_optimizer, criterion, train)
        
        outputs.extend(ChaffNet_output.flatten().tolist())
        all_losses.append(loss)
        loss=loss/n_iters
        loss_total+=loss
        all_losses.append(loss*n_iters)    
    
    return outputs, loss_total, all_losses


def trainEpochs(ChaffNet, inputs, batch_size, name='ChaffNet', epochs=250, learning_rate=0.01, 
                tr_split=0.7, val_split=1.0, weight_decay=5e-4):
    dataname=name
    #weight_decay = 5e-4
    lr_freq_adj = 50
    best_loss = 1000000000
    train_losses=[]
    val_losses=[]
    all_train_losses=[]
    all_val_losses=[]
    ############################################
    #Get training inputs
    n_data=inputs.shape[0]
    input_samples = random.sample(range(0, n_data), int(val_split*n_data))
    train_samples=input_samples[0:int(np.floor((n_data)*tr_split))]
    val_samples=input_samples[int(np.floor((n_data)*tr_split)):int(np.floor((n_data)*val_split))]
    
    train_inputs=inputs.iloc[train_samples,:].reset_index(drop=True)
    val_inputs=inputs.iloc[val_samples,:].reset_index(drop=True)
    ############################################
    
    printtoken=10
    for epoch in range(0, epochs):
        Printer=False
        if (epoch%printtoken==0):
            print('epoch='+str(epoch))
            #Printer=True
            if epoch==(printtoken*10):
                printtoken=printtoken*10
    
        lr = learning_rate*(0.5**(epoch//lr_freq_adj))
        
        outputs, train_loss, all_train_loss = trainIters(ChaffNet, train_inputs, batch_size, train=True,
                                                learning_rate=lr, weight_decay=weight_decay,
                                                Printer=Printer)
        train_losses.append(train_loss)
        all_train_losses.extend(all_train_loss)
        if (epoch%printtoken==0):
            print("train epoch ended, calculate validation loss")
        outputs, val_loss, all_val_loss = trainIters(ChaffNet, val_inputs, batch_size, train=False,
                                            learning_rate=lr, weight_decay=weight_decay,
                                            Printer=Printer)
        if (epoch%printtoken==0):
            print("validation loss calculated, choose if best")
            print("Best loss:"+str(best_loss)+", val loss:"+str(val_loss))
        if val_loss < best_loss:
            torch.save({'epoch': epoch,'model_state_dict': ChaffNet.state_dict(),
                        #'optimizer_state_dict': encoder_optimizer.state_dict(),
                        'loss': val_loss}, dataname+'ChaffNet.tar')

        best_loss = min(val_loss, best_loss)
        val_losses.append(val_loss)
        all_val_losses.extend(all_val_loss)
#        save_checkpoint({'epoch':epoch+1, 'state_dict':model.state_dict(), 'best_loss':best_loss}, is_best, normal,dataname)
    dftrainlosses=pd.DataFrame(train_losses)
    dfvallosses=pd.DataFrame(val_losses)
    dftrainlosses.to_csv(dataname+'_train_losses.csv', index=False)
    dfvallosses.to_csv(dataname+'_val_losses.csv', index=False)
    dftrainlosses=pd.DataFrame(all_train_losses)
    dfvallosses=pd.DataFrame(all_val_losses)
    dftrainlosses.to_csv(dataname+'_all_train_losses.csv', index=False)
    dfvallosses.to_csv(dataname+'_all_val_losses.csv', index=False)


#########################################################################################
#########################################################################################
#########################################################################################

if __name__=='__main__':
    
    inputs=pd.read_csv('ChaffNet_Data/stepping_stone_pairs.csv')
    n_packets=300
    
    sizesall=np.log(inputs.iloc[:,3:(4*n_packets+3)])
    sizesall=(sizesall-np.mean(sizesall.values))/np.std(sizesall.values)
    timesall=np.log(inputs.iloc[:,(4*n_packets+3):(8*n_packets+3)]+0.012)
    timesall=(timesall-np.mean(timesall.values))/np.std(timesall.values)
    
    paired_inputs=pd.concat([sizesall,timesall],axis=1)
    
    conn1_index=[x for x in range(0,n_packets)]
    conn1_index.extend([x for x in range(2*n_packets,3*n_packets)])
    conn1_index.extend([x for x in range(4*n_packets,5*n_packets)])
    conn1_index.extend([x for x in range(6*n_packets,7*n_packets)])
    
    conn2_index=[x for x in range(n_packets,2*n_packets)]
    conn2_index.extend([x for x in range(3*n_packets,4*n_packets)])
    conn2_index.extend([x for x in range(5*n_packets,6*n_packets)])
    conn2_index.extend([x for x in range(7*n_packets,8*n_packets)])
    
    shifted_index=[x for x in range(1,inputs.shape[0])]
    shifted_index.extend([0])
    ind_inputs1=paired_inputs.iloc[:,conn1_index].reset_index(drop=True)
    ind_inputs2=paired_inputs.iloc[:,conn2_index]
    ind_inputs2=ind_inputs2.iloc[shifted_index,:].reset_index(drop=True)
    ind_inputs=pd.concat([ind_inputs1,ind_inputs2],axis=1)
    paired_inputs['label']=0
    ind_inputs['label']=1
    
    clean_inputs=pd.concat([paired_inputs,ind_inputs],axis=0,sort=False).reset_index(drop=True)
    shuffled_index=random.sample(range(0, clean_inputs.shape[0]), clean_inputs.shape[0])
    clean_inputs=clean_inputs.iloc[shuffled_index,:].reset_index(drop=True)
    
    inputs=clean_inputs#.iloc[0:100,:]
    
    print(inputs.shape)
    
    
    #########################################################################################
    # Comparing different dropout, batch sizes, and weight decay
    #########################################################################################
    
    #very small 
    k1=30
    w1=10
    k2=15
    w2=10
    poolw1=5
    poolw2=5
    n_packets=300
    pad1=1
    pad2=2
    Lin1=50
    Lin2=25
    Lin3=10
    lr=0.001
    
    batch_size=90
    dropout=0.05
    weight_decay=0.001
    name="ChaffNet_Data/JADE/very_small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
    print("Network:"+name)
    ChaffNet_small = ChaffNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                       Lin2, Lin3,pad1,pad2,dropout).to(device)
    trainEpochs(ChaffNet_small, inputs, batch_size, name=name, epochs=200, 
                learning_rate=lr, tr_split=0.55, val_split=1.0, weight_decay=weight_decay)