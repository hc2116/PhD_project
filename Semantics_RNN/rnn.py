"""
The pytorch version that I used to create this code was 0.2.*
Pytorch did some major changes after version 0.4.0.
"""


import os
import numpy as np
import pandas as pd
import torch 
import torch.nn as nn
import torch.utils.data as data
from torch.autograd import Variable
import scipy
import shutil
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve
import math
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--train-normal", action="store", type=int, default=1, help="training on normal or on infected sessions")
parser.add_argument("--predict", action="store", type=int, default=0, help="training or predicting")
args = parser.parse_args()
train_normal= args.train_normal
predict = args.predict

PATH_MODEL = '/home/henry/Desktop/detlearsom-master/src/python/rnn_models'
load_data = True
train = 1-predict

# PREPARING THE DATA
# we get the data
if not load_data:
    df = get_data()
    #df_normal, df_background = df[df.label_bot=='normal'], df[df.label_bot=='infected']
else:
    df = pd.read_csv('ctu_normal_infected.csv')
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    print('data loaded')
    #df_normal, df_background = df[df.label_bot=='normal'], df[df.label_bot=='infected']
# we get the most frequent Proto_Dport
dff = df.groupby(['Proto', 'Dport']).size()
dff = dff.reset_index()
dff.columns = ['Proto', 'Dport', 'count']
dff = dff.sort_values('count', ascending = False)
dff['cumulative'] = dff['count'].cumsum()
dff['perc'] = dff['cumulative']/dff['count'].sum()
dff.head()
dff['Dport2'] = dff['Dport']
dff['Dport2'][dff.perc>0.98] = 'Other'
dff['Proto_Dport'] = dff['Proto'] + '_' + dff['Dport2'].astype('str')
# we create the sessions
def set_sessions(df, threshold = 8):
    df2 = df.sort_values(['SrcAddr', 'StartTime'], ascending=[1,1])
    df2 = df2.assign(time_diff = df2['StartTime'].diff())
    df2 = df2.assign(rn = df2.groupby('SrcAddr')['StartTime'].rank(method='first'))
    df2['time_diff_seconds'] = df2.time_diff.astype('timedelta64[s]')
    def create_start_session(x):
        if np.isnan(x) or x>threshold or x<0:
            return(1)
        else:
            return(0)
    df2['session_start'] = df2.time_diff_seconds.apply(create_start_session)
    df2 = df2.assign(session_id = df2.groupby('SrcAddr')['session_start'].cumsum())
    return(df2)
df = set_sessions(df, threshold = 5)
print('session created')

# look-up table to see the category of the SrcAddr
# in the Sherlock data this could be the type of Application
hosts_category = {'147.32.84.170':'Normal', 
    '147.32.84.164':'Normal', 
    '147.32.87.36':'WebServer',
    '147.32.80.9':'DNSServer', 
    '147.32.87.11':'MatlabServer', 
    '147.32.84.134':'Normal',
    '147.32.84.165':'Normal',
    '147.32.84.191':'Normal',
    '147.32.84.192':'Normal',
    '147.32.84.193':'Normal',
    '147.32.84.204':'Normal',
    '147.32.84.205':'Normal',
    '147.32.84.206':'Normal',
    '147.32.84.207':'Normal',
    '147.32.84.208':'Normal',
    '147.32.84.209':'Normal'}
look_up = pd.DataFrame.from_dict(data=hosts_category, orient='index').reset_index()
look_up.columns = ['SrcAddr', 'category']


# we merge df_normal and dff
df_input = df.merge(right=dff, how='inner', on=['Proto','Dport'])[['SrcAddr', 'session_id','Proto_Dport', 'scenario', 'label_bot']]
df_input = df_input.merge(right=look_up, how='inner', on=['SrcAddr'])

# we create our alphabet of Proto+Dport, and the different categories
alphabet = list(df_input['Proto_Dport'].unique())
alphabet.append('EOS') # we need "EndOfSession" included in the alphabet
categories = list(df_input['category'].unique())

df_normal_input, df_infected_input = df_input[df_input.label_bot=='normal'], df_input[df_input.label_bot=='infected']
print('df_normal and df_infected created')



# We create dataset for our RNN
def makedataset(df_input):
    """
    this function will create the combination of SrcAddr and session_id in our dataset.
    We will use this in the __getitem__ method of the session_loader class, that will be used
    to load sessions to feed into the RNN
    """
    df_aggr = df_input.groupby(['SrcAddr','session_id','category']).size().reset_index()
    dataset = []
    for i, row in df_aggr.iterrows():
        dataset.append((row['SrcAddr'], row['session_id'], row['category']))
    return(dataset)

class session_loader(data.Dataset):
    def __init__(self, df_input, alphabet, categories):
        sessions = makedataset(df_input)
        self.sessions = sessions
        self.df = df_input
        self.alphabet = alphabet
        self.n_letters = len(self.alphabet)
        self.categories = categories
        self.n_categories = len(self.categories)
    
    def inputTensor(self,session):
        """
        One-hot matrix of first to last combination of Proto+Dport (not including EOS)
        for input
        """
        session=session.reset_index()
        tensor = torch.zeros(session.shape[0], 1, self.n_letters)
        for i, row in session.iterrows():
            letter = row['Proto_Dport']
            tensor[i][0][self.alphabet.index(letter)] = 1
        return(tensor)
    
    def targetTensor(self,session):
        """
        LongTensor of second combination of Proto+Dport to end (EOS) for target
        """
        target = []
        session=session.reset_index()
        for i, row in session.iterrows():
            if i>0:
                letter = row['Proto_Dport']
                target.append(self.alphabet.index(letter))
        target.append(self.alphabet.index('EOS'))
        return(torch.LongTensor(target))
    
    def categoryTensor(self,session):
        """
        OneHot vector for category
        """
        tensor = torch.zeros(1, self.n_categories)
        tensor[0][self.categories.index(session['category'].iloc[0])] = 1
        return tensor
    
    def __getitem__(self,index):
        SrcAddr, session_id, category = self.sessions[index]
        session = self.df[(self.df['SrcAddr']==SrcAddr) & (self.df['session_id']==session_id)]
        input_tensor = self.inputTensor(session)
        target_tensor = self.targetTensor(session)
        category = self.categoryTensor(session)
        return(category,input_tensor, target_tensor, SrcAddr, session_id)
    
    def __len__(self):
        return(len(self.sessions))


# RNN definition
class RNN_marc(nn.Module):
    """
    I am taking a simple RNN from http://pytorch.org/tutorials/intermediate/char_rnn_generation_tutorial.html
    where I have added ReLU activation functions.
    TODO: here the session length will be important
    TODO: add more complicated layers. LSTM?
    This RNN predicts the next action in terms of current action, what has happened before and the category of the server/app. 
    So in the end we get a string of actions, which is equivalent to the learned automata. 
    """
    def __init__(self, n_categories, input_size, hidden_size, output_size):
        super(RNN_marc, self).__init__()
        self.hidden_size = hidden_size
        self.i2h = nn.Sequential(
            nn.Linear(n_categories + input_size + hidden_size, hidden_size),
            nn.Sigmoid())
        self.i2o = nn.Sequential(
            nn.Linear(n_categories + input_size + hidden_size, 128),
            nn.Sigmoid())
        self.o2o = nn.Sequential(nn.Linear(hidden_size + 128, 128), nn.ReLU(inplace=True))
        self.o2o2 = nn.Linear(128, output_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax()
    
    def forward(self, category, input, hidden):
        input_combined = torch.cat((category, input, hidden), 1)
        hidden = self.i2h(input_combined)
        output = self.i2o(input_combined)
        output_combined = torch.cat((hidden, output), 1)
        self.dropout(output_combined)
        output = self.o2o(output_combined)
        output = self.o2o2(output)
        output = self.softmax(output)
        return output, hidden
    
    def initHidden(self):
        return Variable(torch.zeros(1, self.hidden_size))

class RNN(nn.Module):
    """
    I am taking a simple RNN from http://pytorch.org/tutorials/intermediate/char_rnn_generation_tutorial.html
    where I have added ReLU activation functions.
    TODO: here the session length will be important
    TODO: add more complicated layers. LSTM?
    This RNN predicts the next action in terms of current action, what has happened before and the category of the server/app. 
    So in the end we get a string of actions, which is equivalent to the learned automata. 
    """
    def __init__(self, n_categories, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.i2h = nn.Sequential(
            nn.Linear(n_categories + input_size + hidden_size, hidden_size),
            nn.Sigmoid())
        self.i2o = nn.Sequential(
            nn.Linear(n_categories + input_size + hidden_size, output_size),
            nn.ReLU(inplace=True))
        self.o2o = nn.Sequential(
            nn.Linear(hidden_size + output_size, output_size),
            nn.ReLU(inplace=True))
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax()
    
    def forward(self, category, input, hidden):
        input_combined = torch.cat((category, input, hidden), 1)
        hidden = self.i2h(input_combined)
        output = self.i2o(input_combined)
        output_combined = torch.cat((hidden, output), 1)
        output = self.o2o(output_combined)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden
    
    def initHidden(self):
        return Variable(torch.zeros(1, self.hidden_size))


def save_checkpoint(state, is_best, normal=True, filename='checkpoint_w.pth.tar'):
    epoch = state['epoch']
    if normal:
        torch.save(state, os.path.join(PATH_MODEL, 'normal_marc_epoch'+str(epoch)+'_'+filename))
        if is_best:
            shutil.copyfile(os.path.join(PATH_MODEL, filename), os.path.join(PATH_MODEL,'normal_model_best_long.pth.tar'))
    else:
        torch.save(state, os.path.join(PATH_MODEL, 'infected_'+filename))
        if is_best:
            shutil.copyfile(os.path.join(PATH_MODEL, filename), os.path.join(PATH_MODEL,'infected_model_best_long.pth.tar'))



def save_checkpoint_cv(state, is_best, scenario_test, filename='checkpoint_cv'):
    torch.save(state, os.path.join(PATH_MODEL, filename+'_'+str(scenario_test)+'.pth.tar'))
    if is_best:
        shutil.copyfile(os.path.join(PATH_MODEL, filename+'_'+str(scenario_test)+'.pth.tar'), os.path.join(PATH_MODEL,'model_best_cv_'+str(scenario)+'.pth.tar'))

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def train_epoch(train_loader, model, criterion, optimizer, epoch, normal):
    """
    Train for one epoch
    """
    model.train()
    print('inside train') 
    for i, (category, input, target, SrcAddr, session_id) in enumerate(train_loader):
        print('i={}'.format(i))
        # we will need to convert them to Variable to use gradients.
        category, input, target = category[0], input[0], target[0]
        category = Variable(category)
        input = Variable(input)
        target = Variable(target)
        hidden = model.initHidden()
        model.zero_grad()
        loss = 0
        for flow in range(input.size()[0]):
            output, hidden = model(category, input[flow], hidden)
            loss+=criterion(output, target[flow])
        loss.backward()
        optimizer.step()
        if normal:
            log_file = 'train_log_normal.txt'
        else:
            log_file = 'train_log_infected.txt'
        with open(log_file, 'a') as f:
            f.write('Epoch: [{0}][{1}/{2}]\t'
                  'loss: {loss}\n'.format(epoch, i, len(train_loader),loss=loss.data[0]))



def validate(val_loader, model, criterion, epoch, normal):
    losses = AverageMeter()
    # switch to evaluation mode so that the Dropout doesn't drop neurons
    model.eval()
    for i, (category, input, target, SrcAddr, session_id) in enumerate(val_loader):
        category, input, target = category[0], input[0], target[0]
        category = Variable(category)
        input = Variable(input)
        target = Variable(target)
        hidden = model.initHidden()
        model.zero_grad()
        loss = 0
        for flow in range(input.size()[0]):
            output, hidden = model(category, input[flow], hidden)
            loss+=criterion(output, target[flow])
        losses.update(loss.data[0], input.size()[0])
        if normal:
            log_file = 'validate_log_normal.txt'
        else:
            log_file = 'validate_log_infected.txt'
        with open('validate_log.txt', 'a') as f:
            f.write('Epoch: [{0}][{1}/{2}]\t'
                  'loss: {loss}\n'.format(epoch, i, len(val_loader),loss=loss.data[0]))
    return(losses.avg)


def getLabel(SrcAddr):
    label = df['label_bot'][df['SrcAddr']==SrcAddr].iloc[0]
    if label == 'infected':
        return 1 # 1 infected
    else:
        return 0 # 0 normal


def predict():
    """
    This function loads the trained rnn and returns prediction scores for normal hosts and infected hosts in test set
    It also returns the cumulative averages of the scores
    """
    print('prediction starts')
    scenarios_test = [1,2,5,6,7,8,9,11,12,13]
    n_categories = len(categories)
    checkpoint = torch.load('rnn_models/normal_marc_epoch8_checkpoint_w.pth.tar')
    model = RNN_marc(n_categories, input_size=len(alphabet), hidden_size=128, output_size=len(alphabet))
    model.load_state_dict(checkpoint['state_dict'])
    df_normal_pred = df_normal_input[df_normal_input.scenario.isin(scenarios_test)]
    df_pred = pd.concat([df_normal_pred, df_infected_input])
    pred_loader = data.DataLoader(session_loader(df_pred, alphabet, categories), batch_size=1, shuffle=False)
    #df_input = df_input[-df_input.scenario.isin(scenarios_test)]
    #pred_loader = data.DataLoader(session_loader(df_input, alphabet, categories), batch_size=1, shuffle=False)
    model.eval()
    output_stats = {'SrcAddr':[], 'session_id':[], 'label': [], 'mean':[], 'median':[]}
    for i, (category, input, target, SrcAddr, session_id) in enumerate(pred_loader):
        if i%10 == 0:
           print("i = {}".format(i)) 
        probs = []
        category, input, target = category[0], input[0], target[0]
        category = Variable(category)
        input = Variable(input)
        target = Variable(target)
        hidden = model.initHidden()
        for flow in range(input.size()[0]):
            output, hidden = model(category, input[flow], hidden)
            prob_next_flow = output.data[0][target.data.numpy()[0]]
            probs.append(1-math.exp(prob_next_flow)) # we do exp because the last layer of RNN is LogSoftmax
        output_stats['mean'].append(np.mean(np.array(probs)))
        output_stats['median'].append(np.median(np.array(probs)))
        output_stats['label'].append(getLabel(SrcAddr[0]))
        output_stats['SrcAddr'].append(SrcAddr[0])
        output_stats['session_id'].append(session_id[0])
    df_output = pd.DataFrame(data=output_stats)
    df_output = df_output.sort_values(['SrcAddr', 'session_id'])
    # for each session, we will also check the previous session to compute cumulative average scores
    df_output2 = df_output.assign(sum_means = df_output.groupby('SrcAddr')['mean'].cumsum())
    df_output2 = df_output2.assign(count_previous = df_output2.groupby('SrcAddr')['mean'].cumcount()+1)
    df_output2 = df_output2.assign(sum_medians = df_output2.groupby('SrcAddr')['median'].cumsum())
    df_output2 = df_output2.assign(avg_previous_means = lambda x: x['sum_means']/x['count_previous'])
    df_output2 = df_output2.assign(avg_previous_medians = lambda x: x['sum_medians']/x['count_previous'])
    #df_output2.to_csv('rnn_output_deep.csv', index=False)
    df_output2.to_csv('rnn_output_train.csv', index=False)
    return df_output2


def predict_all(normal=True):
    """
    This function loads the trained rnn and returns prediction scores for normal hosts and infected hosts in test set
    It also returns the cumulative averages of the scores
    """
    n_categories = len(categories)
    if normal:
        checkpoint = torch.load('rnn_models/normal_model_best_long.pth.tar')
    else:
        checkpoint = torch.load('rnn_models/infected_checkpoint_w.pth.tar')
    model = RNN(n_categories, input_size=len(alphabet), hidden_size=128, output_size=len(alphabet))
    model.load_state_dict(checkpoint['state_dict'])
    #df_normal_pred = df_normal_input[df_normal_input.scenario.isin(scenarios_test)]
    #df_pred = pd.concat([df_normal_pred, df_infected_input])
    pred_loader = data.DataLoader(session_loader(df_input, alphabet, categories), batch_size=1, shuffle=False)
    model.eval()
    output_stats = {'SrcAddr':[], 'session_id':[], 'label': [], 'mean':[], 'median':[]}
    for i, (category, input, target, SrcAddr, session_id) in enumerate(pred_loader):
        if i%10 == 0:
           print("i = {}".format(i)) 
        probs = []
        category, input, target = category[0], input[0], target[0]
        category = Variable(category)
        input = Variable(input)
        target = Variable(target)
        hidden = model.initHidden()
        for flow in range(input.size()[0]):
            output, hidden = model(category, input[flow], hidden)
            prob_next_flow = output.data[0][target.data.numpy()[0]]
            probs.append(math.exp(prob_next_flow)) # we do exp because the last layer of RNN is LogSoftmax
        output_stats['mean'].append(np.mean(np.array(probs)))
        output_stats['median'].append(np.median(np.array(probs)))
        output_stats['label'].append(getLabel(SrcAddr[0]))
        output_stats['SrcAddr'].append(SrcAddr[0])
        output_stats['session_id'].append(session_id[0])
    df_output = pd.DataFrame(data=output_stats)
    df_output = df_output.sort_values(['SrcAddr', 'session_id'])
    # for each session, we will also check the previous session to compute cumulative average scores
    df_output2 = df_output.assign(sum_means = df_output.groupby('SrcAddr')['mean'].cumsum())
    df_output2 = df_output2.assign(count_previous = df_output2.groupby('SrcAddr')['mean'].cumcount()+1)
    df_output2 = df_output2.assign(sum_medians = df_output2.groupby('SrcAddr')['median'].cumsum())
    df_output2 = df_output2.assign(avg_previous_means = lambda x: x['sum_means']/x['count_previous'])
    df_output2 = df_output2.assign(avg_previous_medians = lambda x: x['sum_medians']/x['count_previous'])
    return df_output2

def evaluation_metrics_plots(df_output):
    """
    this function evaluates the prediciton of the RNN providing the following:
        - violinplot of the 'mean' scores (1='normal', 0='infected')
        - roc_curve of the 'mean' scores (1='normal', 0='infected')
        - auc of the 'mean' scores (1='normal', 0='infected')
        - confusion matrix according taking the best threshold in the roc curve
    """
    # violin plot
    sns.set()
    violin = sns.violinplot(x='label', y='mean', data=df_output)
    fig= violin.get_figure()
    fig.savefig('violin_output_rnn.png') 
    # roc curve
    y_true, y_scores = df_output['label'].values, df_output['mean'].values
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = roc_auc_score(y_true, y_scores)
    fig = plt.figure()
    plt.plot(fpr, tpr, color='darkorange',
         lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.title('ROC curve with 1=normal and 0=infected')
    fig.savefig('ROC_curve_positive_normal.png')
    # we change the scores so that 1=infected and 0=normal
    df_output = df_output.assign(mean_reverse = lambda x: 1-x['mean'])
    df_output = df_output.assign(label_reverse = lambda x: 1-x['label'])
    # violing plot with 1-infected and 0=normal
    violin = sns.violinplot(x='label_reverse', y='mean_reverse', data=df_output)
    fig = violin.get_figure()
    fig.savefig('violin_output_rnn_positive_infected.png')
    y_true, y_scores = df_output['label_reverse'].values, df_output['mean_reverse'].values
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = roc_auc_score(y_true, y_scores)
    fig = plt.figure()
    plt.plot(fpr, tpr, color='darkorange',
         lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.title('ROC curve with 0=normal and 1=infected')
    fig.savefig('ROC_curve_positive_infected.png') 
    # distance to (0,1) to get best threshold
    distances2 = [x**2+(1-y)**2 for x,y in zip(fpr, tpr)]
    ind_min = distances2.index(min(distances2))
    threshold = thresholds[ind_min]
    df_output = df_output.assign(pred_y = lambda x: x['mean_reverse']>=threshold)
    pd.crosstab(df_output['pred_y'], df_output['label_reverse'])




def train(normal=True):
    # training hyperparameters. These will probably need to be tuned. 
    print('Starting main')
    epochs = 50
    batch_size = 1
    base_lr= 0.0001
    lr = base_lr
    n_hidden=128
    learning_rate = 0.0005
    weight_decay = 5e-4
    momentum = 0.9
    lr_freq_adj = 1
    n_categories = len(categories)
    #scenarios_test = [4,8]
    scenarios_test = [1,2,5,6,7,8,9,11,12,13]
    best_loss = 1000

    #in_log.txt we define model
    model = RNN_marc(n_categories, input_size=len(alphabet), hidden_size=n_hidden, output_size=len(alphabet))
    # we define loss function
    criterion = nn.NLLLoss() # we define Negatve Loglikelihood lost because We are doing a multinomial classification. 
    
    # train_loader
    if normal:
        df_train = df_normal_input[(-df_normal_input.scenario.isin(scenarios_test) & (df_normal_input.SrcAddr!='147.32.84.164'))] 
        train_loader = data.DataLoader(session_loader(df_train, alphabet, categories),
                                       batch_size=batch_size, shuffle=True)
        # test loader
        test_loader = data.DataLoader(session_loader(df_normal_input[df_normal_input.scenario.isin(scenarios_test)], alphabet, categories),
                                       batch_size=batch_size, shuffle=True)
    else:
        train_loader = data.DataLoader(session_loader(df_infected_input[-df_infected_input.scenario.isin(scenarios_test)], alphabet, categories),
                                       batch_size=batch_size, shuffle=True)
        # test loader
        test_loader = data.DataLoader(session_loader(df_infected_input[df_infected_input.scenario.isin(scenarios_test)], alphabet, categories),
                                       batch_size=batch_size, shuffle=True)
    # optimizer: Stochastic Gradient Descent
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay, momentum=momentum)
    for epoch in range(0, epochs):
        print('epoch={}'.format(epoch))
        # adjust learning rate. Divide it by 2 every 10 epochs
        lr = base_lr*(0.5**(epoch//lr_freq_adj))
        for param_group in optimizer.state_dict()['param_groups']:
            param_group['lr']=lr
        # train for one epoch
        train_epoch(train_loader, model, criterion, optimizer, epoch, normal)
        val_loss = validate(test_loader, model, criterion, epoch, normal)
        is_best = val_loss < best_loss
        best_loss = min(val_loss, best_loss)
        save_checkpoint({'epoch':epoch+1, 'state_dict':model.state_dict(), 'best_loss':best_loss}, is_best, normal)


def train_cv(scenario_test):
    # training hyperparameters. These will probably need to be tuned. 
    print('Starting main')
    epochs = 10
    batch_size = 1
    base_lr= 0.0001
    lr = base_lr
    n_hidden=128
    learning_rate = 0.0005
    weight_decay = 5e-4
    momentum = 0.9
    lr_freq_adj = 1
    n_categories = len(categories)
    best_loss = 1000
    #we define model
    model = RNN(n_categories, input_size=len(alphabet), hidden_size=n_hidden, output_size=len(alphabet))
    # we define loss function
    criterion = nn.NLLLoss() # we define Negatve Loglikelihood lost because We are doing a multinomial classification. 
    
    # train_loader
    train_loader = data.DataLoader(session_loader(df_normal_input[-df_normal_input.scenario.isin(scenario_test)], alphabet, categories),
                                   batch_size=batch_size, shuffle=True)
    # test loader
    test_loader = data.DataLoader(session_loader(df_normal_input[df_normal_input.scenario.isin(scenario_test)], alphabet, categories),
                                   batch_size=batch_size, shuffle=True)
    # optimizer: Stochastic Gradient Descent
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay, momentum=momentum)
    for epoch in range(0, epochs):
        print('epoch={}'.format(epoch))
        # adjust learning rate. Divide it by 2 every 10 epochs
        lr = base_lr*(0.5**(epoch//lr_freq_adj))
        for param_group in optimizer.state_dict()['param_groups']:
            param_group['lr']=lr
        # train for one epoch
        train_epoch(train_loader, model, criterion, optimizer, epoch)
        val_loss = validate(test_loader, model, criterion, epoch)
        is_best = val_loss < best_loss
        best_loss = min(val_loss, best_loss)
        save_checkpoint_cv({'epoch':epoch+1, 'state_dict':model.state_dict(), 'best_loss':best_loss}, is_best, scenario_test)


if __name__=='__main__':
    if train==1:
        if train_normal:
            train(True)
        else:
            train(False)
    else:
        predict()
    print('success')



