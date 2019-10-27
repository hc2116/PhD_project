#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:24:28 2019

@author: henry
"""
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import random
from ConvNet import ConvNet
print(torch.cuda.is_available())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device")




def predict(DeepCorr, inputs, batch_size=0, Printer=True):
    ############################################
    #Get training inputs
    losses=[]
    outputs=[]
    n_data=inputs.shape[0]
    if batch_size==0:
        batch_size=n_data
    DeepCorr.eval()
    ##########################################################
    n_iters = int(np.floor(n_data/batch_size))
    iter_indexes=[x*batch_size for x in range(0,n_iters+1)]
    if iter_indexes[n_iters]!=n_data:
        iter_indexes.append(n_data)
    input_indices1=[x+1 for x in range(0,2*n_packets)]
    input_indices2=[x+1 for x in range(2*n_packets,4*n_packets)]
    input_indices3=[x+1 for x in range(4*n_packets,6*n_packets)]
    input_indices4=[x+1 for x in range(6*n_packets,8*n_packets)]
    labels_index = 0
    
    criterion = nn.BCEWithLogitsLoss(reduction='none')
    #########################################################
    printtoken=10
    print("#Iterations: "+str(len(iter_indexes)-1))
    for iteration in range(0, len(iter_indexes)-1):
        if (iteration%printtoken==0):
            if Printer==True:
                print('iteration='+str(iteration))
            if iteration==(printtoken*10):
                printtoken=printtoken*10
        
        batch_index = [x for x in range(iter_indexes[iteration],iter_indexes[iteration+1])]
        batch_size=len(batch_index)
        input1 = torch.tensor(inputs.iloc[batch_index,input_indices1].values,device=device).view(batch_size,1,2,-1)
        input2 = torch.tensor(inputs.iloc[batch_index,input_indices2].values,device=device).view(batch_size,1,2,-1)
        input3 = torch.tensor(inputs.iloc[batch_index,input_indices3].values,device=device).view(batch_size,1,2,-1)
        input4 = torch.tensor(inputs.iloc[batch_index,input_indices4].values,device=device).view(batch_size,1,2,-1)
        labels =  torch.tensor(inputs.iloc[batch_index,labels_index].values,dtype=torch.float32, device=device)
        
        DeepCorr_output = DeepCorr(input1.float(), input2.float(), 
                                   input3.float(), input4.float())
        #print(DeepCorr_output)
        outputs.extend(DeepCorr_output.flatten().tolist())
        #print(criterion(DeepCorr_output.squeeze(), labels))
        losses.extend(criterion(DeepCorr_output.squeeze(), labels).tolist())

    return outputs, losses

#############################################################################################
#############################################################################################

if __name__=='__main__':


    
#############################################################################################
#############################################################################################
    
    inputs=pd.read_csv('testdata_pairs.csv')
    #inputs=pd.read_csv('testdata_long_pairs.csv')
    
    para_colnames=['name',"NETCAT_PARA1","NETCAT_PARA2","NETCAT_PARA3","NETCAT_PARA4",
                   "NETCAT_PARA5","NETCAT_PARA6","DELAY_PARA1","DELAY_PARA2","DELAY_PARA3",
                   "DELAY_PARA4","DELAY_PARA5","DELAY_PARA6"]
    inputs_params=pd.read_csv('testdata_params.txt',names=para_colnames)
    #inputs_params=pd.read_csv('testdata_long_params.txt',names=para_colnames)
    n_packets=300
    
    inputs=inputs.sort_values(by='name').reset_index(drop=True)
    inputs_params=inputs_params.sort_values(by='name').reset_index(drop=True)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    sizesall=np.log(inputs.iloc[:,3:(4*n_packets+3)])
    sizesall=(sizesall-np.mean(sizesall.values))/np.std(sizesall.values)
    timesall=np.log(inputs.iloc[:,(4*n_packets+3):(8*n_packets+3)]+0.012)
    timesall=(timesall-np.mean(timesall.values))/np.std(timesall.values)
    
    paired_inputs=pd.concat([sizesall,timesall],axis=1)
    paired_inputs['label']=0
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    conn1_index=[x+3 for x in range(0,n_packets)]
    conn1_index.extend([x+3 for x in range(2*n_packets,3*n_packets)])
    conn1_index.extend([x+3 for x in range(4*n_packets,5*n_packets)])
    conn1_index.extend([x+3 for x in range(6*n_packets,7*n_packets)])
    
    conn2_index=[x+3 for x in range(n_packets,2*n_packets)]
    conn2_index.extend([x+3 for x in range(3*n_packets,4*n_packets)])
    conn2_index.extend([x+3 for x in range(5*n_packets,6*n_packets)])
    conn2_index.extend([x+3 for x in range(7*n_packets,8*n_packets)])
    
    conn1_params_index=[1,2,3,7,8]
    conn2_params_index=[4,5,6,11,12]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    shifted_index=[x for x in range(1,inputs.shape[0])]
    shifted_index.extend([0])
    
    ind_inputs1=inputs.iloc[:,conn1_index].reset_index(drop=True)
    ind_inputs2=inputs.iloc[:,conn2_index]
    ind_inputs2=ind_inputs2.iloc[shifted_index,:].reset_index(drop=True)
    ind_inputs=pd.concat([ind_inputs1,ind_inputs2],axis=1)
    ind_inputs['label']=1
    
    ind_inputs_params1=inputs_params.iloc[:,conn1_params_index].reset_index(drop=True)
    ind_inputs_params2=inputs_params.iloc[:,conn2_params_index]
    ind_inputs_params2=ind_inputs_params2.iloc[shifted_index,:].reset_index(drop=True)
    ind_inputs_params=pd.concat([ind_inputs_params1,ind_inputs_params2],axis=1)
    ind_inputs.columns
    
    clean_inputs=pd.concat([paired_inputs,ind_inputs],axis=0,sort=True).reset_index(drop=True)
    #shuffled_index=random.sample(range(0, clean_inputs.shape[0]), clean_inputs.shape[0])
    #clean_inputs=clean_inputs.iloc[shuffled_index,:].reset_index(drop=True)
    
    inputs=clean_inputs
    print(inputs.shape)
    
#    for iii in range(1,2401):
#        #inputs.iloc[0:int(inputs.shape[0]),iii]=inputs.iloc[random.sample(range(0, int(inputs.shape[0])), int(inputs.shape[0])),iii].reset_index(drop=True)
#        inputs.iloc[0:int(inputs.shape[0]/2),iii]=inputs.iloc[random.sample(range(0, int(inputs.shape[0]/2)), int(inputs.shape[0]/2)),iii].reset_index(drop=True)
#        inputs.iloc[int(inputs.shape[0]/2):inputs.shape[0],iii]=inputs.iloc[random.sample(range( int(inputs.shape[0]/2),inputs.shape[0]), int(inputs.shape[0]/2)),iii]


#    indexes=[0]
#    indexes.extend(random.sample(range(1, 2401), int(2400)))
#    inputs=inputs.iloc[:,indexes]
    
#####################################################################################################
#####################################################################################################
    
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
    dropout=0.05
    
    DeepCorr_small = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                       Lin2, Lin3,pad1,pad2,dropout).to(device)
    
    checkpoint = torch.load('JADE/final_small_good_fits_lr:0.001wd:0.001batch:90dropout:0.05DeepCorr.tar',map_location=device)
    DeepCorr_small.load_state_dict(checkpoint['model_state_dict'])
    
    Outputs_small, losses_small = predict(DeepCorr_small, inputs, batch_size=10)
    #Outputs_small2, losses_small2 = predict(DeepCorr_small, inputs, batch_size=10)

    k1=600
    w1=30
    k2=250
    w2=10
    poolw1=5
    poolw2=5
    pad1=1
    pad2=2
    Lin1=600
    Lin2=200
    Lin3=60
    dropout=0.05

    DeepCorr_big = ConvNet(n_packets, k1, w1, k2, w2, poolw1, poolw2, Lin1, 
                       Lin2, Lin3,pad1,pad2,dropout).to(device)
    checkpoint_big = torch.load('JADE/final_big_good_fits_lr:0.001wd:0.001batch:90dropout:0.05DeepCorr.tar',map_location=device)
    DeepCorr_big.load_state_dict(checkpoint_big['model_state_dict'])
    
    Outputs_big, losses_big = predict(DeepCorr_big, inputs, batch_size=10)


#####################################################################################################
#####################################################################################################
    import matplotlib.pyplot as plt    
    
    nnn=int(inputs.shape[0]/2)
    plt.hist(Outputs_small[0:nnn],bins=40)
    #plt.hist(Outputs_small2[0:nnn],bins=40)
    plt.hist(Outputs_small[nnn:(2*nnn)],bins=40)

    np.mean(Outputs_small[0:nnn])
    np.mean(Outputs_small[nnn:(2*nnn)])
    
    plt.hist(Outputs_big[0:nnn],bins=40)
    plt.hist(Outputs_big[nnn:(2*nnn)],bins=40)

    np.mean(Outputs_big[0:nnn])
    np.mean(Outputs_big[nnn:(2*nnn)])


    plt.hist(losses)
    