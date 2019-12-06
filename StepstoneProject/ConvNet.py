#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:11:27 2019

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


class ConvNet(nn.Module):
    def __init__(self, l, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                 Lin2, Lin3, pad1, pad2, dropout):
        super(ConvNet, self).__init__()
        self.k1=k1
        self.k2=k2
        self.w1=w1
        self.w2=w2
        self.l=l
        self.pad1=pad1
        self.pad2=pad2
        self.poolw1=poolw1
        self.poolw2=poolw2
        self.Lin1=Lin1
        self.Lin2=Lin2
        self.Lin3=Lin3
        #input dim: batch_sizex1x2xl
        self.convtime1 = nn.Conv2d(1, self.k1, (2,self.w1), stride=(2,1), padding=(0,self.pad1))
        self.convtime2 = nn.Conv2d(1, self.k1, (2,self.w1), stride=(2,1), padding=(0,self.pad1))
        self.convsize1 = nn.Conv2d(1, self.k1, (2,self.w1), stride=(2,1), padding=(0,self.pad1))
        self.convsize2 = nn.Conv2d(1, self.k1, (2,self.w1), stride=(2,1), padding=(0,self.pad1))
        self.relu=nn.ReLU()
        self.convtime1_bn = nn.BatchNorm2d(self.k1)
        self.convtime2_bn = nn.BatchNorm2d(self.k1)
        self.convsize1_bn = nn.BatchNorm2d(self.k1)
        self.convsize2_bn = nn.BatchNorm2d(self.k1)
        self.dropout = nn.Dropout(dropout)
        #output dim: batch_sizex1x1x(l-w1+1+pad)
        self.pool1 = nn.MaxPool2d((1,self.poolw1), stride=(1,1))
        #output dim: batch_sizex1x1x(l-w1-poolw1+1+pad)
        
        self.convcomb = nn.Conv2d(self.k1, self.k2, (4,self.w2), stride=(4,1), padding=(0,self.pad2))
        self.convcomb_bn = nn.BatchNorm2d(self.k2)
        #output dim: batch_sizex1x1x(l-w1-poolw1+1+pad)
        
        self.pool2 = nn.MaxPool2d((1,self.poolw2), stride=(1,1))
        
        self.fc1 = nn.Linear(self.k2*(self.l-self.w1+1+2*self.pad1-
                                      self.poolw1+1-self.w2+1+2*self.pad2-
                                      self.poolw2+1), self.Lin1)
        self.fc2 = nn.Linear(self.Lin1, self.Lin2)
        self.fc3 = nn.Linear(self.Lin2, self.Lin3)
        self.fc1_bn = nn.BatchNorm1d(self.Lin1)
        self.fc2_bn = nn.BatchNorm1d(self.Lin2)
        self.fc3_bn = nn.BatchNorm1d(self.Lin3)
        self.fcoutput = nn.Linear(self.Lin3,1)
#        self.sigmoid = nn.LogSigmoid()
        
    def forward(self, input1, input2, input3, input4):
        #input dim: batch_sizex1x2xl
        batchsize=input1.shape[0]
        timefeatures1 = self.dropout(self.convtime1_bn(self.relu(self.convtime1(input1))))
        timefeatures2 = self.dropout(self.convtime2_bn(self.relu(self.convtime2(input2))))
        sizefeatures1 = self.dropout(self.convsize1_bn(self.relu(self.convsize1(input3))))
        sizefeatures2 = self.dropout(self.convsize2_bn(self.relu(self.convsize2(input4))))
        #output dim: batch_sizexk1x1x(l-w1+1+2*pad1)        
        timefeatures1 = self.pool1(timefeatures1)
        timefeatures2 = self.pool1(timefeatures2)
        sizefeatures1 = self.pool1(sizefeatures1)
        sizefeatures2 = self.pool1(sizefeatures2)
        #output dim: batch_sizexk1x1x(l-w1+1+2*pad1-poolw1+1)        
        combfeatures = torch.cat([timefeatures1,timefeatures2,
                               sizefeatures1,sizefeatures2], dim=2)
        #output dim: batch_sizexk1x4x(l-w1+1+2*pad1-poolw1+1)        
#        combfeatures = self.relu(self.convcomb(combfeatures))
        combfeatures = self.convcomb_bn(self.relu(self.convcomb(combfeatures)))
        #output dim: batch_sizexk2x1x(l-w1+1+2*pad1-poolw1+1-w2+1+2*pad2)                
        poolcombfeatures = self.pool2(self.dropout(combfeatures))
        #output dim: batch_sizexk2x1x(l-w1+1+2*pad1-poolw1+1-w2+1+2*pad2-poolw2+1)        
        poolcombfeatures = poolcombfeatures.squeeze(2).view(batchsize,-1)

        Linfeatures1 = self.dropout(self.fc1_bn(self.relu(self.fc1(poolcombfeatures))))
        Linfeatures2 = self.dropout(self.fc2_bn(self.relu(self.fc2(Linfeatures1))))
        Linfeatures3 = self.dropout(self.fc3_bn(self.relu(self.fc3(Linfeatures2))))
        Output = self.fcoutput(Linfeatures3)
        return Output



def trainBatch(input1, input2, input3, input4, labels,
               DeepCorr, DeepCorr_optimizer, criterion, train=True):
#    batch_size = inputs1.size(0)
    
    DeepCorr_output = DeepCorr(input1.float(), input2.float(), 
                               input3.float(), input4.float())
    loss = criterion(DeepCorr_output.squeeze(), labels)
    #####################################################
    #####################################################

    if train==True:
        DeepCorr_optimizer.zero_grad()
        loss.backward()
        DeepCorr_optimizer.step()
    return DeepCorr_output, loss.item()




def trainIters(DeepCorr, inputs, batch_size, n_packets=300,train=True,
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
        DeepCorr.train()
    else:
        DeepCorr.eval()
        iter_indexes=[x*batch_size for x in range(0,n_iters+1)]
        if iter_indexes[n_iters]!=n_data:
            n_iters+=1
            iter_indexes.append(n_data)
    DeepCorr_optimizer = optim.Adam(DeepCorr.parameters(), lr=learning_rate, weight_decay=weight_decay)
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
        
        DeepCorr_output, loss = trainBatch(input1, input2, input3, input4, labels,
                     DeepCorr, DeepCorr_optimizer, criterion, train)
        
        outputs.extend(DeepCorr_output.flatten().tolist())
        all_losses.append(loss)
        loss=loss/n_iters
        loss_total+=loss
        all_losses.append(loss*n_iters)    
    
    return outputs, loss_total, all_losses


def trainEpochs(DeepCorr, inputs, batch_size, name='DeepCorrnet', epochs=250, learning_rate=0.01, 
                tr_split=0.7, val_split=1.0, weight_decay=5e-4):
    dataname=name
    #weight_decay = 5e-4
    lr_freq_adj = 35
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
        
        outputs, train_loss, all_train_loss = trainIters(DeepCorr, train_inputs, batch_size, train=True,
                                                learning_rate=lr, weight_decay=weight_decay,
                                                Printer=Printer)
        train_losses.append(train_loss)
        all_train_losses.extend(all_train_loss)
        if (epoch%printtoken==0):
            print("train epoch ended, calculate validation loss")
        outputs, val_loss, all_val_loss = trainIters(DeepCorr, val_inputs, batch_size, train=False,
                                            learning_rate=lr, weight_decay=weight_decay,
                                            Printer=Printer)
        if (epoch%printtoken==0):
            print("validation loss calculated, choose if best")
            print("Best loss:"+str(best_loss)+", val loss:"+str(val_loss))
        if val_loss < best_loss:
            torch.save({'epoch': epoch,'model_state_dict': DeepCorr.state_dict(),
                        #'optimizer_state_dict': encoder_optimizer.state_dict(),
                        'loss': val_loss}, dataname+'DeepCorr.tar')

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
    
    #inputs=pd.read_csv('DeepCorr_Data/stepping_stone_pairs.csv')
    inputs_SSH=pd.read_csv('DeepCorr_Data/stepping_stone_pairs.csv')    
    columns=inputs_SSH.columns    
#    inputs_Noise_50=pd.read_csv('DeepCorr_Data/noise_50_Conv.txt',header=None)    
#    inputs_Noise_51=pd.read_csv('DeepCorr_Data/noise_51_Conv.txt',header=None)    
#    inputs_Noise_52=pd.read_csv('DeepCorr_Data/noise_52_Conv.txt',header=None)    
#    inputs_Noise_53=pd.read_csv('DeepCorr_Data/noise_53_Conv.txt',header=None)
    inputs_Noise_52=pd.read_csv('DeepCorr_Data/NoNoise/noise52_relay_stepstone-2019-11-29_18-47-14-sc1-1.csv_Conv.txt',header=None)    
    inputs_Noise_53=pd.read_csv('DeepCorr_Data/NoNoise/noise53_relay_stepstone-2019-11-29_18-48-26-sc1-1.csv_Conv.txt',header=None)    
    inputs_Noise_54=pd.read_csv('DeepCorr_Data/NoNoise/noise54_relay_stepstone-2019-11-29_18-50-23-sc1-1.csv_Conv.txt',header=None)
    inputs_Noise_55=pd.read_csv('DeepCorr_Data/NoNoise/noise55_relay_stepstone-2019-11-29_18-53-03-sc1-1.csv_Conv.txt',header=None)    
    inputs_Noise_56=pd.read_csv('DeepCorr_Data/NoNoise/noise56_relay_stepstone-2019-11-29_18-57-49-sc1-1.csv_Conv.txt',header=None)    
    inputs_Noise_57=pd.read_csv('DeepCorr_Data/NoNoise/noise57_relay_stepstone-2019-11-29_18-56-49-sc1-1.csv_Conv.txt',header=None)
    inputs_Noise_52.columns=columns
    inputs_Noise_53.columns=columns
    inputs_Noise_54.columns=columns
    inputs_Noise_55.columns=columns
    inputs_Noise_56.columns=columns
    inputs_Noise_57.columns=columns
    inputs=pd.concat([inputs_Noise_52,inputs_Noise_53,inputs_Noise_54,inputs_Noise_55,inputs_Noise_56,inputs_Noise_57],
                     ignore_index=True)
    
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
    # Increasing learning rate stabilise val loss
    # next steps:
    # Try even larger learning rate
    # increase regularisation
    # change batch size
    #########################################################################################
   
    # larger learning rate ##################################################################
    #small 
    k1=60
    w1=20
    k2=30
    w2=20
    poolw1=5
    poolw2=5
    n_packets=300
    pad1=1
    pad2=2
    Lin1=100
    Lin2=50
    Lin3=20
    lr=0.005
    
    batch_size=90
    dropout=0.2
    weight_decay=0.02
    name="DeepCorr_Data/JADE/small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
    print("Network:"+name)
    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                       Lin2, Lin3,pad1,pad2,dropout).to(device)
    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=202, 
                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
    
    
    #large
    k1=250
    w1=30
    k2=100
    w2=10
    poolw1=5
    poolw2=5
    n_packets=300
    pad1=1
    pad2=2
    Lin1=300
    Lin2=80
    Lin3=20
    lr=0.005
    
    batch_size=90
    dropout=0.2
    weight_decay=0.02
    name="DeepCorr_Data/JADE/large_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
    print("Network:"+name)
    DeepCorr_large = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                       Lin2, Lin3,pad1,pad2,dropout).to(device)
    trainEpochs(DeepCorr_large, inputs, batch_size, name=name, epochs=202, 
                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
        
    print("Terminated")

#    # larger weight decay ##################################################################
#    #small 
#    k1=60
#    w1=20
#    k2=30
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=100
#    Lin2=50
#    Lin3=20
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.1
#    weight_decay=0.01
#    name="DeepCorr_Data/JADE/small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    
#    #large
#    k1=250
#    w1=30
#    k2=100
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=300
#    Lin2=80
#    Lin3=20
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.1
#    weight_decay=0.01
#    name="DeepCorr_Data/JADE/large_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_large = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_large, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)

    
    
#    #########################################################################################
#    # Initial size comparison - inconclusive, training loss goes down for all, 
#    # but val loss increases steadily
#    # might want to try more regularisation
#    # maybe too little data
#    #########################################################################################
#    
#    #very small 
#    k1=30
#    w1=10
#    k2=15
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=50
#    Lin2=25
#    Lin3=10
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/very_small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_vsmall = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_vsmall, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #small 
#    k1=60
#    w1=20
#    k2=30
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=100
#    Lin2=50
#    Lin3=20
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #medium
#    k1=120
#    w1=40
#    k2=60
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=200
#    Lin2=80
#    Lin3=30
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/medium_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_med = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_med, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #large
#    k1=250
#    w1=30
#    k2=100
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=300
#    Lin2=80
#    Lin3=20
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/large_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_large = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_large, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#        
#
##    #########################################################################################
##    Bigger learning rate
##    #########################################################################################
#
#    #very small 
#    k1=30
#    w1=10
#    k2=15
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=50
#    Lin2=25
#    Lin3=10
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/very_small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_vsmall = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_vsmall, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #small 
#    k1=60
#    w1=20
#    k2=30
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=100
#    Lin2=50
#    Lin3=20
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #medium
#    k1=120
#    w1=40
#    k2=60
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=200
#    Lin2=80
#    Lin3=30
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/medium_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_med = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_med, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#    
#    #large
#    k1=250
#    w1=30
#    k2=100
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=300
#    Lin2=80
#    Lin3=20
#    lr=0.005
#    
#    batch_size=90
#    dropout=0.2
#    weight_decay=0.02
#    name="DeepCorr_Data/JADE/large_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_large = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_large, inputs, batch_size, name=name, epochs=202, 
#                learning_rate=lr, tr_split=0.75, val_split=1.0, weight_decay=weight_decay)
#        
#    print("Terminated")
    

    
    
    
    
#    #########################################################################################
#    # Initial size comparison - inconclusive, training loss goes down for all, 
#    # but val loss increases steadily
#    # might want to try more regularisation
#    # maybe too little data
#    #########################################################################################
#    
#    #very small 
#    k1=30
#    w1=10
#    k2=15
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=50
#    Lin2=25
#    Lin3=10
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.05
#    weight_decay=0.001
#    name="DeepCorr_Data/JADE/very_small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=200, 
#                learning_rate=lr, tr_split=0.55, val_split=1.0, weight_decay=weight_decay)
#    
#    #small 
#    k1=60
#    w1=20
#    k2=30
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=100
#    Lin2=50
#    Lin3=20
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.05
#    weight_decay=0.001
#    name="DeepCorr_Data/JADE/small_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=200, 
#                learning_rate=lr, tr_split=0.55, val_split=1.0, weight_decay=weight_decay)
#    
#    #medium
#    k1=120
#    w1=40
#    k2=60
#    w2=20
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=200
#    Lin2=80
#    Lin3=30
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.05
#    weight_decay=0.001
#    name="DeepCorr_Data/JADE/medium_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=200, 
#                learning_rate=lr, tr_split=0.55, val_split=1.0, weight_decay=weight_decay)
#    
#    #large
#    k1=250
#    w1=30
#    k2=100
#    w2=10
#    poolw1=5
#    poolw2=5
#    n_packets=300
#    pad1=1
#    pad2=2
#    Lin1=300
#    Lin2=80
#    Lin3=20
#    lr=0.001
#    
#    batch_size=90
#    dropout=0.05
#    weight_decay=0.001
#    name="DeepCorr_Data/JADE/large_lr:"+str(lr)+"wd:"+str(weight_decay)+"batch:"+str(batch_size)+"dropout:"+str(dropout)
#    print("Network:"+name)
#    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
#                       Lin2, Lin3,pad1,pad2,dropout).to(device)
#    trainEpochs(DeepCorr_small, inputs, batch_size, name=name, epochs=200, 
#                learning_rate=lr, tr_split=0.55, val_split=1.0, weight_decay=weight_decay)
#        
#    print("Terminated")
#    
#
