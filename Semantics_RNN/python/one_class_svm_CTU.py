import os
import pandas as pd
import numpy as np
from collections import Counter
from glob import glob
from create_dataset_CTU import *
from aggregate_CTU import *
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('ctu_normal_infected.csv')
df['StartTime'] = pd.to_datetime(df['StartTime'])
prediction_FSA = pd.read_csv('prediction_FSA_all.csv')
prediction_mc= pd.read_csv('prediction_mc_all.csv')



def set_sessions(df, threshold = 8): 
    df2 = df.sort_values(['SrcAddr', 'StartTime'], ascending=[1,1])
    df2 = df2.assign(time_diff = df2['StartTime'].diff())
    df2 = df2.assign(rn = df2.groupby('SrcAddr')['StartTime'].rank(method='first'))
    df2['time_diff_seconds'] = df2.time_diff.astype('timedelta64[s]')
    df['time_diff_ms'] = df2.time_diff.astype('timedelta64[ms]')
    def create_start_session(x):
        if np.isnan(x) or x>threshold or x<0:
            return(1)
        else:
            return(0)
    df2['session_start'] = df2.time_diff_seconds.apply(create_start_session)
    df2 = df2.assign(session_id = df2.groupby('SrcAddr')['session_start'].cumsum())
    return(df2)
df = set_sessions(df, threshold = 5)



def create_aggregated_dataset(df2, threshold = 8, image_path = image_path, do_plots = False):
    """ 
    we create session in order to aggregate behaviour by session
    from the exploratory analysis, we create a threshold at 9s, as 90% of the
    time between flows is less then 9s
    """
    proto_dummies = pd.get_dummies(df2.Proto)
    #df2 = df.sort_values(["SrcAddr", "StartTime"], ascending=[1,1])
    #df2 = df2.assign(time_diff = df2["StartTime"].diff())
    #df2 = df2.assign(rn = df2.groupby("SrcAddr")["StartTime"].rank(method="first"))
    #df2['time_diff_seconds'] = df2.loc[:,'time_diff'].astype('timedelta64[s]')
    #   
    #def create_start_session(x):
    #    if np.isnan(x) or x>threshold or x<0:
    #        return(1)
    #    else:
    #        return(0)
    #df2['session_start'] = df2.time_diff_seconds.apply(create_start_session)
    #df2 = df2.assign(session_id = df2.groupby('SrcAddr')['session_start'].cumsum())
    #   
    ### We create the first set of features:
    # For each SrcAddr, and each session_id we create:
    # 1. Total number of flows
    # 2. Of the above, how many times did SrcAddr connect to the same address
    # 3. avg Bytes per packet
    # 4. std Bytes per packet
    # 5. count of different protocols
    # 6. count of flows per protocol?
    proto_dummies = pd.get_dummies(df2.Proto)
    df2 = pd.concat([df2, proto_dummies], axis=1)
    df3 = df2.set_index(['SrcAddr', 'session_id'])
    def count_max(x):
        return(x.value_counts().max())
    def len_unique(x):
        return(len(x.unique()))
    df3_aggr = df3.groupby(['SrcAddr', 'session_id', 'label_bot', 'scenario']).agg({'DstAddr':[len, count_max],
                           'BytesPkt':[np.mean,np.std],
                           'TotPkts':[np.sum,np.mean,np.std],
                           'Proto':len_unique,
                           'arp':np.sum,
                           #'esp':np.sum,
                           'icmp':np.sum,
                           'igmp':np.sum,
                           #'ipv6':np.sum,
                           #'ipv6-icmp':np.sum,
                           #'ipx/spx':np.sum,
                           #'llc':np.sum,
                           #'pim':np.sum,
                           #'rtcp':np.sum,
                           'rtp':np.sum,
                           'tcp':np.sum,
                           'udp':np.sum}).reset_index()
                           #'udt':np.sum}).reset_index()
    df3_aggr.columns=['SrcAddr', 'session_id', 'label_bot', 'scenario', 'DstAddr_count', 'Dst_Addr_count_max',
                      'BytesPkt_mean', 'BytesPkt_std', 'SrcPkts_count', 'SrcPkts_mean', 
                      'SrcPkts_std', 'Proto_len_unique', 'arp_count',
                      'icmp_count', 'igmp_count', 'rtp_count', 'tcp_count', 'udp_count']
    if do_plots:
        sns_plot = sns.boxplot(x="label_bot", y="DstAddr_count", data = df3_aggr)
        sns_plot.save_fig(os.path.join(image_path, 'box_plot_count_flows.png'))
        sns_plot = sns.boxplot(x = "label_bot", y = "BytesPkt_mean", data=df3_aggr)
        sns_plot.save_fig(os.path.join(image_path, 'box_plot_bytesPkt_mean.png'))
        sns_plot = sns.boxplot(x = "label_bot", y="SrcPkts_count", data=df3_aggr)
        sns_plot.save_fig(os.path.join(image_path, "boxplot_SrcPkts_count.png"))
    return(df3_aggr)

def create_bin_label(s):
    if s == 'infected':
        return 1
    else:
        return 0


def get_highest_threshold(thresholds, scores):
    MAX = 0
    output = 0
    for t in thresholds:
        pred = np.zeros(Y_test.shape)
        pred = scores>t
        f1 = fbeta_score(Y_test, pred, beta=0.6)
        if f1>MAX:
            MAX = f1
            output = t
    return MAX, output


def report_scenario(label, sc):
    Y_test, pred = sc.label_bot_bin.values, sc.pred.values
    prec = precision_score(Y_test, pred)
    recall = recall_score(Y_test, pred)
    f1 = fbeta_score(Y_test, pred, beta=0.6)
    number_sessions = sc.shape[0]
    P = sc.label_bot_bin.value_counts()[1]
    TP = sc[(sc.pred==1) & (sc.label_bot_bin==1)].shape[0]
    FP = sc[(sc.pred==1) & (sc.label_bot_bin==0)].shape[0]
    N = sc.label_bot_bin.value_counts()[0]
    fpr, tpr, thresholds = roc_curve(Y_test, sc.avg_previous_pred_session.values)
    AUC = auc(fpr, tpr)
    output = {'AUC':AUC, 'prec':prec, 'recall':recall, 'fbeta':f1, 'scenario':label, 'count':number_sessions, 'P':P, 'N':N,'TP':TP, 'FP':FP}
    return pd.DataFrame(output, index=[label])





df2 = create_aggregated_dataset(df, threshold = 5)
df2['label_bot_bin'] = 1
df2['label_bot_bin'][df2.label_bot=='normal'] = 0

df3 = df2.merge(right = prediction_FSA[['SrcAddr','session_id','fsa_edit_dist']], how="inner", on=["SrcAddr", "session_id"])
df3 = df3.merge(right = prediction_mc[['SrcAddr','session_id','average_score']], how="inner", on=["SrcAddr", "session_id"])



# we do One-class SVM
scenarios_test = [1,2,5,6,7,8,9,11,12,13]
df_train = df3[-df3.scenario.isin(scenarios_test)]
df_test = df3[df3.scenario.isin(scenarios_test)]

df_train.BytesPkt_std[np.isnan(df_train.BytesPkt_std)] = 1000
df_train.SrcPkts_std[np.isnan(df_train.SrcPkts_std)] = 1000 
df_test.BytesPkt_std[np.isnan(df_test.BytesPkt_std)] = 1000 
df_test.SrcPkts_std[np.isnan(df_test.SrcPkts_std)] = 1000 

df_train = df_train[df_train.label_bot=='normal'].drop(["arp_count", "igmp_count", "rtp_count"], axis = 1)
df_test = df_test.drop(["arp_count", "igmp_count", "rtp_count"], axis = 1)

X_train = df_train.drop(['SrcAddr', 'session_id', 'label_bot', 'label_bot_bin', 'scenario'], axis=1).values
Y_train = df_train['label_bot_bin'].values
X_test = df_test.drop(['SrcAddr', 'session_id', 'label_bot', 'label_bot_bin', 'scenario'], axis=1).values
Y_test = df_test['label_bot_bin'].values

scaler = StandardScaler().fit(X_train)
scaler.mean_
scaler.scale_

X_train_transformed = scaler.transform(X_train)
X_test_transformed = scaler.transform(X_test)

clf = OneClassSVM(nu=0.1, kernel='rbf', gamma=0.08)
clf.fit(X_train_transformed)
Y_pred = clf.predict(X_test_transformed)
Y_pred[Y_pred==1] = 0 
Y_pred[Y_pred==-1] = 1 
prec = precision_score(Y_test, Y_pred)
recall = recall_score(Y_test, Y_pred)
confusion_matrix(Y_test, Y_pred)



# scores
scores = clf.decision_function(X_test_transformed)
fpr, tpr, thresholds = roc_curve(Y_test, scores*(-1))
AUC = auc(fpr, tpr)



df_test = df_test.assign(scores = scores*(-1))

# cumulative average
df_test = df_test.assign(sum_scores = df_test.groupby(['SrcAddr', 'scenario'])['scores'].cumsum())
df_test = df_test.assign(count_session=df_test.groupby(['SrcAddr','scenario'])['scores'].cumcount()+1)
df_test = df_test.assign(avg_previous_pred_session=lambda x: x['sum_scores']/x['count_session'])

scores = df_test.avg_previous_pred_session.values
fpr, tpr, thresholds = roc_curve(Y_test, scores)
AUC = auc(fpr, tpr)



MAX_f1, t = get_highest_threshold(thresholds, scores)
pred = scores>t
prec = precision_score(Y_test, pred)
recall = recall_score(Y_test, pred)
fbeta = fbeta_score(Y_test, pred,beta=0.6)

evaluation_overall_OneClassSVM = pd.DataFrame({'prec':prec, 'recall':recall,'AUC':AUC,'fbeta':fbeta}, index=['OneClass'])
evaluation_overall_OneClassSVM.to_csv('evaluation_overall_OneClassSVM.csv', index=False)

# we check what happens per scenario
# we check what happens per scenario
df_test = df_test.assign(pred = pred)


l = []
for label, group in df_test.groupby('scenario'):
    l.append(report_scenario(label, group))

report = pd.concat(l, axis=0)
report.to_csv('report_one_class_svm.csv', index=False)





