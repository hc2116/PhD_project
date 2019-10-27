#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:46:41 2019

@author: henry
"""
import pandas as pd
import matplotlib.pyplot as plt

all_train1=pd.read_csv('JADE/lr:0.1wd:0.0001_all_train_losses.csv')
all_train2=pd.read_csv('JADE/lr:0.1wd:0.0006_all_train_losses.csv')
all_train3=pd.read_csv('JADE/lr:0.01wd:0.0001_all_train_losses.csv')
all_train4=pd.read_csv('JADE/lr:0.01wd:0.0006_all_train_losses.csv')
all_train5=pd.read_csv('JADE/lr:0.001wd:0.0001_all_train_losses.csv')
all_train6=pd.read_csv('JADE/lr:0.001wd:0.0006_all_train_losses.csv')

train1=pd.read_csv('JADE/lr:0.1wd:0.0001_train_losses.csv')
train2=pd.read_csv('JADE/lr:0.1wd:0.0006_train_losses.csv')
train3=pd.read_csv('JADE/lr:0.01wd:0.0001_train_losses.csv')
train4=pd.read_csv('JADE/lr:0.01wd:0.0006_train_losses.csv')
train5=pd.read_csv('JADE/lr:0.001wd:0.0001_train_losses.csv')
train6=pd.read_csv('JADE/lr:0.001wd:0.0006_train_losses.csv')

all_val1=pd.read_csv('JADE/lr:0.1wd:0.0001_all_val_losses.csv')
all_val2=pd.read_csv('JADE/lr:0.1wd:0.0006_all_val_losses.csv')
all_val3=pd.read_csv('JADE/lr:0.01wd:0.0001_all_val_losses.csv')
all_val4=pd.read_csv('JADE/lr:0.01wd:0.0006_all_val_losses.csv')
all_val5=pd.read_csv('JADE/lr:0.001wd:0.0001_all_val_losses.csv')
all_val6=pd.read_csv('JADE/lr:0.001wd:0.0006_all_val_losses.csv')

val1=pd.read_csv('JADE/lr:0.1wd:0.0001_val_losses.csv')
val2=pd.read_csv('JADE/lr:0.1wd:0.0006_val_losses.csv')
val3=pd.read_csv('JADE/lr:0.01wd:0.0001_val_losses.csv')
val4=pd.read_csv('JADE/lr:0.01wd:0.0006_val_losses.csv')
val5=pd.read_csv('JADE/lr:0.001wd:0.0001_val_losses.csv')
val6=pd.read_csv('JADE/lr:0.001wd:0.0006_val_losses.csv')



plt.plot(train1,color='blue')
plt.plot(train2,color='red')
plt.plot(train3,color='green')
plt.plot(train4,color='yellow')
plt.plot(train5,color='purple')
plt.plot(train6,color='black')


#plt.plot(val1,color='blue')
plt.plot(val2,color='red')
plt.plot(val3,color='green')
plt.plot(val4,color='yellow')
plt.plot(val5,color='purple')
plt.plot(val6,color='black')

#######################################################################################################
#######################################################################################################

all_train1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_all_train_losses.csv')
all_train2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_all_train_losses.csv')
all_train3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_all_train_losses.csv')
all_train4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_all_train_losses.csv')

train1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_train_losses.csv')
train2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_train_losses.csv')
train3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_train_losses.csv')
train4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_train_losses.csv')

all_val1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_all_val_losses.csv')
all_val2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_all_val_losses.csv')
all_val3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_all_val_losses.csv')
all_val4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_all_val_losses.csv')

val1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_val_losses.csv')
val2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_val_losses.csv')
val3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_val_losses.csv')
val4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_val_losses.csv')

plt.plot(train1,color='blue')
plt.plot(train2,color='red')
plt.plot(train3,color='green')
plt.plot(train4,color='yellow')


plt.plot(val1,color='blue')
plt.plot(val2,color='red')
plt.plot(val3,color='green')
plt.plot(val4,color='yellow')

plt.plot(train3,color='green')
plt.plot(val3,color='blue')


#######################################################################################################
#######################################################################################################

all_train1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_all_train_losses.csv')
all_train2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_all_train_losses.csv')
all_train3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_all_train_losses.csv')
all_train4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_all_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_train5=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:30_all_train_losses.csv')
all_train6=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:90_all_train_losses.csv')
all_train7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30_all_train_losses.csv')
all_train8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30_all_train_losses.csv')
all_train9=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30dropout:0.05_all_train_losses.csv')
all_train10=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30dropout:0.05_all_train_losses.csv')
all_train11=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_all_train_losses.csv')
all_train12=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_all_train_losses.csv')


train1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_train_losses.csv')
train2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_train_losses.csv')
train3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_train_losses.csv')
train4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
train5=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:30_train_losses.csv')
train6=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:90_train_losses.csv')
train7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30_train_losses.csv')
train8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30_train_losses.csv')
train9=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30dropout:0.05_train_losses.csv')
train10=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30dropout:0.05_train_losses.csv')
train11=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_train_losses.csv')
train12=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_train_losses.csv')


all_val1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_all_val_losses.csv')
all_val2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_all_val_losses.csv')
all_val3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_all_val_losses.csv')
all_val4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_all_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_val5=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:30_all_val_losses.csv')
all_val6=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:90_all_val_losses.csv')
all_val7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30_all_val_losses.csv')
all_val8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30_all_val_losses.csv')
all_val9=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30dropout:0.05_all_val_losses.csv')
all_val10=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30dropout:0.05_all_val_losses.csv')
all_val11=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_all_val_losses.csv')
all_val12=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_all_val_losses.csv')

val1=pd.read_csv('JADE/big_lr:0.001wd:0.0001_val_losses.csv')
val2=pd.read_csv('JADE/big_lr:0.001wd:2e-05_val_losses.csv')
val3=pd.read_csv('JADE/small_lr:0.001wd:0.0001_val_losses.csv')
val4=pd.read_csv('JADE/small_lr:0.001wd:2e-05_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
val5=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:30_val_losses.csv')
val6=pd.read_csv('JADE/big_lr:0.001wd:0.001batch:90_val_losses.csv')
val7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30_val_losses.csv')
val8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30_val_losses.csv')
val9=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:30dropout:0.05_val_losses.csv')
val10=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:30dropout:0.05_val_losses.csv')
val11=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_val_losses.csv')
val12=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_val_losses.csv')



#plt.plot(val1,color='blue')
#plt.plot(val2,color='red')
plt.plot(val3,color='green')
#plt.plot(val4,color='yellow')
#plt.plot(val5,color='purple')
#plt.plot(val6,color='black')
#plt.plot(val7,color='orange')
#plt.plot(val8,color='lightblue')
plt.plot(val9,color='lightgreen')
#plt.plot(val10,color='coral')
plt.plot(val11,color='grey')
plt.plot(val12,color='brown')

#plt.plot(val1[9:50],color='blue')
#plt.plot(val2[9:50],color='red')
plt.plot(val3[9:50],color='green')
#plt.plot(val4[9:50],color='yellow')
#plt.plot(val5[9:50],color='purple')
#plt.plot(val6[9:50],color='black')
#plt.plot(val7[9:50],color='orange')
#plt.plot(val8[9:50],color='lightblue')
plt.plot(val9[9:50],color='lightgreen')
#plt.plot(val10[9:50],color='coral')
plt.plot(val11[9:50],color='grey')
plt.plot(val12[9:50],color='brown')

plt.plot(all_val1,color='blue')
#plt.plot(all_val2,color='red')
plt.plot(all_val3,color='green')
plt.plot(all_val4,color='yellow')
#plt.plot(all_val5,color='purple')
#plt.plot(all_val6,color='black')
#plt.plot(all_val7,color='orange')
#plt.plot(all_val8,color='lightblue')
plt.plot(all_val9,color='lightgreen')
#plt.plot(all_val10,color='coral')
plt.plot(all_val11,color='grey')
plt.plot(all_val12,color='brown')


plt.plot(all_val1[9:-1],color='blue')
plt.plot(all_val2[9:-1],color='red')
plt.plot(all_val3[9:-1],color='green')
plt.plot(all_val4[9:-1],color='yellow')
plt.plot(all_val5[9:-1],color='purple')
plt.plot(all_val6[9:-1],color='black')
plt.plot(all_val7[9:-1],color='orange')
plt.plot(all_val8[9:-1],color='lightblue')
plt.plot(all_val9[9:-1],color='lightgreen')
plt.plot(all_val10[9:-1],color='coral')
plt.plot(all_val11[200:-1],color='grey')
plt.plot(all_val12[200:-1],color='brown')





plt.plot(all_val11[200:-1],color='grey')
plt.plot(all_val12[200:-1],color='brown')
plt.plot(all_train11[200:-1],color='blue')
plt.plot(all_train12[200:-1],color='green')

import numpy as np
np.median(all_val11[200:-1])
np.median(all_val12[200:-1])
np.median(all_train11[200:-1])
np.median(all_train12[200:-1])


plt.plot(val11[9:-1],color='grey')
plt.plot(val12[9:-1],color='brown')
plt.plot(train11[9:-1],color='blue')
plt.plot(train12[9:-1],color='green')




#######################################################################################################
#######################################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
all_train1=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.0_all_train_losses.csv')
all_train2=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:200dropout:0.0_all_train_losses.csv')
all_train3=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.3_all_train_losses.csv')
all_train4=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:200dropout:0.0_all_train_losses.csv')
all_train5=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.0_all_train_losses.csv')
all_train6=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.3_all_train_losses.csv')
all_train7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_all_train_losses.csv')
all_train8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_all_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
train1=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.0_train_losses.csv')
train2=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:200dropout:0.0_train_losses.csv')
train3=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.3_train_losses.csv')
train4=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:200dropout:0.0_train_losses.csv')
train5=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.0_train_losses.csv')
train6=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.3_train_losses.csv')
train7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_train_losses.csv')
train8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_val1=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.0_all_val_losses.csv')
all_val2=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:200dropout:0.0_all_val_losses.csv')
all_val3=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.3_all_val_losses.csv')
all_val4=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:200dropout:0.0_all_val_losses.csv')
all_val5=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.0_all_val_losses.csv')
all_val6=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.3_all_val_losses.csv')
all_val7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_all_val_losses.csv')
all_val8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_all_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
val1=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.0_val_losses.csv')
val2=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:200dropout:0.0_val_losses.csv')
val3=pd.read_csv('JADE/good_fits_lr:0.001wd:0.001batch:90dropout:0.3_val_losses.csv')
val4=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:200dropout:0.0_val_losses.csv')
val5=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.0_val_losses.csv')
val6=pd.read_csv('JADE/good_fits_lr:0.001wd:0.01batch:90dropout:0.3_val_losses.csv')
val7=pd.read_csv('JADE/small_lr:0.001wd:0.001batch:90dropout:0.05_val_losses.csv')
val8=pd.read_csv('JADE/small_lr:0.001wd:0.0001batch:90dropout:0.05_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
plt.plot(val1,color='blue')
#plt.plot(val2,color='red')
#plt.plot(val3,color='green')
#plt.plot(val4,color='yellow')
#plt.plot(val5,color='purple')
#plt.plot(val6,color='black')
plt.plot(val7,color='coral')
plt.plot(val8,color='lightblue')


plt.plot(val1[9:-1],color='blue')
plt.plot(val2[9:-1],color='red')
#plt.plot(val3[9:-1],color='green')
#plt.plot(val4[9:-1],color='yellow')
plt.plot(val5[9:-1],color='purple')
#plt.plot(val6[9:-1],color='black')
plt.plot(val7[9:-1],color='coral')
plt.plot(val8[9:-1],color='lightblue')

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
all_train1=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_all_train_losses.csv')
all_train2=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_all_train_losses.csv')
all_train3=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.006batch:90dropout:0.05_all_train_losses.csv')
all_train4=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.012batch:90dropout:0.05_all_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_train5=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.05_all_train_losses.csv')
all_train6=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_all_train_losses.csv')
all_train7=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.05_all_train_losses.csv')
all_train8=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.0_all_train_losses.csv')
all_train9=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.05_all_train_losses.csv')
all_train10=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.0_all_train_losses.csv')
all_train11=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_all_train_losses.csv')
all_train12=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.0_all_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_val1=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_all_val_losses.csv')
all_val2=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_all_val_losses.csv')
all_val3=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.006batch:90dropout:0.05_all_val_losses.csv')
all_val4=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.012batch:90dropout:0.05_all_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
all_val5=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.05_all_val_losses.csv')
all_val6=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_all_val_losses.csv')
all_val7=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.05_all_val_losses.csv')
all_val8=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.0_all_val_losses.csv')
all_val9=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.05_all_val_losses.csv')
all_val10=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.0_all_val_losses.csv')
all_val11=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_all_val_losses.csv')
all_val12=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.0_all_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
train1=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_train_losses.csv')
train2=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_train_losses.csv')
train3=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.006batch:90dropout:0.05_train_losses.csv')
train4=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.012batch:90dropout:0.05_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
train5=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.05_train_losses.csv')
train6=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_train_losses.csv')
train7=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.05_train_losses.csv')
train8=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.0_train_losses.csv')
train9=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.05_train_losses.csv')
train10=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.0_train_losses.csv')
train11=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_train_losses.csv')
train12=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.0_train_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
val1=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_val_losses.csv')
val2=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_val_losses.csv')
val3=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.006batch:90dropout:0.05_val_losses.csv')
val4=pd.read_csv('JADE/big_good_fits_lr:0.001wd:0.012batch:90dropout:0.05_val_losses.csv')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
val5=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.05_val_losses.csv')
val6=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:200dropout:0.0_val_losses.csv')
val7=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.05_val_losses.csv')
val8=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.0001batch:90dropout:0.0_val_losses.csv')
val9=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.05_val_losses.csv')
val10=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:200dropout:0.0_val_losses.csv')
val11=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.05_val_losses.csv')
val12=pd.read_csv('JADE/small_good_fits_lr:0.001wd:0.001batch:90dropout:0.0_val_losses.csv')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

plt.plot(val1,color='blue')
plt.plot(val2,color='red')
#plt.plot(val3,color='green')
plt.plot(val4,color='yellow')
plt.plot(val5,color='purple')
plt.plot(val6,color='black')
plt.plot(val7,color='coral')
plt.plot(val8,color='lightblue')
plt.plot(val9,color='magenta')
plt.plot(val10,color='brown')
plt.plot(val11,color='grey')
plt.plot(val12,color='orange')


#plt.plot(val1[9:-1],color='blue')
plt.plot(val2[9:-1],color='red')
#plt.plot(val3[9:-1],color='green')
#plt.plot(val4[9:-1],color='yellow')
#plt.plot(val5[9:-1],color='purple')
#plt.plot(val6[9:-1],color='black')
#plt.plot(val7[9:-1],color='coral')
#plt.plot(val8[9:-1],color='lightblue')
#plt.plot(val9[9:-1],color='magenta')
#plt.plot(val10[9:-1],color='brown')
plt.plot(val11[9:-1],color='grey')
#plt.plot(val12[9:-1],color='orange')


