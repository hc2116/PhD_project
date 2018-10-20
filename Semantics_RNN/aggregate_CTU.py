from create_dataset_CTU import *
import os
import numpy as np
import seaborn as sns
import scipy
import matplotlib.pyplot as plt
from models.mchain import *
from ctu_botnet_actions import *
import models.ndfsa as mfsa
import models.dfsa as mpta
import time


#metadata = create_metadata()
#df = create_dataset(metadata)
image_path = os.path.join(os.environ['HOME'], 'detlearsom', 'images')

def exploratory_analysis(image_path = image_path):
    # check session times
    df = get_data()
    df2 = df.sort_values(["SrcAddr", "StartTime"], ascending=[1,1])
    df2 = df2.assign(time_diff = df2["StartTime"].diff())
    df2 = df2.assign(rn = df2.groupby("SrcAddr")["StartTime"].rank(method="first"))
    df2['time_diff_seconds'] = df2.loc[:,'time_diff'].astype('timedelta64[ms]')
    df3 = df2[df2.rn>1] # we remove the first flow from each SrcAddr because we are interested in the time between flows
    df3 = df3[df3.label_bot == 'normal']

    df3.time_diff_seconds.describe()
    np.percentile(df3.time_diff_seconds, range(0,100,5))

    # histogram
    #plt.figure()
    sns_plot = sns.distplot(df3.time_diff_seconds[df3.time_diff_seconds<15000], bins=40, kde=False)
    sns_plot.set(xlabel="time difference between flows in ms", ylabel="count")
    fig = sns_plot.get_fig()
    fig.savefig(os.path.join(image_path, 'histgoram_time_between_flows.png'))
    # for each scenario, and each host in the scenario, print 
    plt.figure()
    sns_plot = sns.countplot(x="session_id", hue="Proto", data=df2[(df2.scenario==2) & (df2.SrcAddr=="147.32.84.170")])
    plt.show()



def get_data():
    metadata = create_metadata()
    #df, df_background = create_dataset(metadata)
    df = create_dataset(metadata)
    #return (df, df_background)
    return(df)

def split_train_test_scenarios(df):
    """
    there are thirteen different scenarios. This function splits the dataset
    into train set and test set, without mixing scenarios.
    """
    # there are 12 different scenarios. The following commands randomly choose
    # 10 scenarios for the train set and 2 scenarios for the test set
    #sc = df.scenario.unique()
    #sc_train = np.random.choice(sc, size=10, replace=False)
    #df_train = df[df.scenario.isin(sc_train)]
    #df_test = df[-df.scenario.isin(sc_train)]
    #df_train = df[-df.scenario.isin([4,8])]
    training_scenarios = [3,4,10]
    df_train = df[df.scenario.isin(training_scenarios)]
    df_test = df[-df.scenario.isin(training_scenarios)]
    # uncomment the following lines to handcode the scenarios that will be in the
    # training set
    #df_train = df[df.scenario.isin(range(2,11))]
    #df_test = df[-df.scenario.isin(range(2,11))]
    return (df_train, df_test)


def set_mcs_and_fsa(df_train):
    """
    this function creates the Markov Chains that will get the probability per session
    One MC is created per non-infected IP address in the training set
    These MC intend to represent finite automata
    """
    df_normal = df_train[df_train.label_bot == 'normal']
    ls = {}  # last session number 
    la = {}  # last action for mchain
    #lpta = {} # last pta 
    mcs = {} # markov chains (one for each IP address)
    cptas = {} # current PTA (will be in a subtree of ptas - reset to top pta (top-level) at start of session)
    ptas = {} # top-level PTA (first a PTA is learnt then converted to FSA
    fsas = {} # the FSAs to be returned
    IP = df_normal.SrcAddr.unique()[2:]
    df_normal = df_normal[df_normal.SrcAddr.isin(IP)]
    for ip in IP: # initialis
        ls[ip] = -1
        mcs[ip] = MarkovChain()
        ptas[ip] =  mpta.PTA("")
        cptas[ip] = ptas[ip]
    for i, row in df_normal.iterrows():
        if i%100 == 0: 
            print('row {}'.format(i))
        act = action_of_row(row)
        sid = row['session_id']
        ip = row['SrcAddr']
        if sid != ls[ip]: # new session, reset mcs and pta to start
            ls[ip] = sid
            la[ip] = mcs[ip].start
            cptas[ip] = ptas[ip]
        mcs[ip].add_trans(la[ip],act) 
        cptas[ip] = cptas[ip].add_single(act)
        la[ip] = act
    for ip in IP:
        print ("Generates probability(MC) and merges states: " + ip)
        mcs[ip].compute_prob()
        # generates fsa and merges similar states
        init_time = time.time()
        with open('log_fsa.txt', 'a') as f:
            f.write('ip: {}, init time fsa: {}\n'.format(ip, init_time))
        fsas[ip] = mfsa.pta_to_bfndfsa(ptas[ip])
        time1 = time.time()
        with open('log_fsa.txt', 'a') as f:
            f.write('ip: {}, bfndfsa time: {}\n'.format(ip, time1))
        fsas[ip].bluefringe(threshold = 0,strictness=0)
        time2 = time.time()
        with open('log_fsa.txt', 'a') as f:
            f.write('ip: {}, bluefringe time: {}\n'.format(ip, time2))
        fsas[ip].merge_leafs()
        end_time = time.time()
        total_time = end_time-init_time
        with open('log_fsa.txt', 'a') as f:
            f.write('ip: {}, merge leafs timeL {}, total_time: {:.3f}\n'.format(ip, end_time, total_time))
        mfsa.save_fsa('fsa_' + ip + '.json',fsas[ip])
    return(mcs,fsas)


def set_mcs(df_train):
    """
    this function creates the Markov Chains that will get the probability per session
    One MC is created per non-infected IP address in the training set
    These MC intend to represent finite automata
    """
    df_normal = df_train[df_train.label_bot == 'normal']
    ls = {}
    la = {}
    mcs = {}
    IP = df_normal.SrcAddr.unique()
    for ip in IP:
        ls[ip] = -1
        mcs[ip] = MarkovChain()
    for i, row in df_normal.iterrows():
        if i%10 == 0: 
            print('row {}'.format(i))
        act = action_of_row(row)
        sid = row['session_id']
        ip = row['SrcAddr']
        if sid != ls[ip]:
            ls[ip] = sid
            la[ip] = mcs[ip].start
        mcs[ip].add_trans(la[ip],act)
        la[ip] = act
    for ip in IP:
        mcs[ip].compute_prob()
    return(mcs)


def compute_best_score(sess_acts, mcs):
    """
    we compare sessions with the MC probabilities
    """
    sess_acts = list(sess_acts)
    best_prob = -1
    for ip in mcs.keys():
        _,prob =  mcs[ip].prob_of_action_seq(sess_acts)
        if prob > best_prob:
            best_prob = prob
    return best_prob


def compute_best_average(sess_acts, mcs):
    sess_acts = list(sess_acts)
    best_avg = -1.0
    for ip in mcs.keys():
        (_,avg) = mcs[ip].avg_prob_of_actions(sess_acts)
        if avg > best_avg:
            best_avg = avg
    return best_avg 


def compute_edit_dist(sess_acts, fsa):
    sess_acts = list(sess_acts)
    best_score = len(sess_acts)
    for ip in fsa.keys():
        dist =  fsa[ip].edit_distance(sess_acts)
        if dist[1] < best_score:
            # we compare with the normalised distance
            best_score = dist[1]
    return best_score

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



def createAggFeaturesWithMC(df):
    #df, df_background = get_data()
    df = set_sessions(df, threshold = 5)
    # we create the aggregated features on the whole dataset.
    df_aggrFeatures = create_aggregated_dataset(df)
    # in the following command we will create the MC features
    print('split in train - test sets')
    df_train, df_test = split_train_test_scenarios(df)
    print('set mcs and fsa')
    init_time = time.time()
    mcs, fsa = set_mcs_and_fsa(df_train)
    print('fsa and mcs creation time: {:.3f}'.format(init_time - time.time()))
    df_normal_train = df_train[df_train.label_bot == 'normal']
    df_infected_train = df_train[df_train.label_bot == 'infected']
    df_test = pd.concat([df_infected_train, df_test], axis=0)
    df_normal_train['action'] = df_normal_train.apply(action_of_row, axis=1)
    df_normal_train['action2'] = df_normal_train['action'] 
    df_normal_train['fsa_edit_dist'] = df_normal_train['action'] 
    df_aggr_train = df_normal_train.groupby(['SrcAddr', 'session_id']).agg({'action':lambda x: compute_best_score(x, mcs=mcs), 
                                                                            'action2':lambda x: compute_best_average(x, mcs=mcs),
                                                                            'fsa_edit_dist': lambda x: compute_edit_dist(x,fsa=fsa)})
    df_aggr_train.columns = ['session_best_score', 'session_average_score','fsa_edit_dist']
    df_aggr_train = df_aggr_train.reset_index()
    df_test['action'] = df_test.apply(action_of_row, axis=1)
    df_test['action2'] = df_test['action']
    df_test['fsa_edit_dist'] = df_test['action'] 
    df_aggr_test = df_test.groupby(['SrcAddr', 'session_id']).agg({'action':lambda x: compute_best_score(x, mcs=mcs),
                                                                   'action2': lambda x: compute_best_average(x, mcs=mcs),
                                                                   'fsa_edit_dist':lambda x: compute_edit_dist(x, fsa=fsa)})
    df_aggr_test.columns = ['session_best_score', 'session_average_score','fsa_edit_dist']
    df_aggr_test = df_aggr_test.reset_index()
    # we merge the aggregated features with the MC features
    df_aggr_train2 = df_aggr_train.merge(right=df_aggrFeatures, how='inner', on=['SrcAddr', 'session_id'])
    df_aggr_test2 = df_aggr_test.merge(right=df_aggrFeatures, how='inner', on=['SrcAddr', 'session_id'])
    # we do the same for background
    #df_background_features = created_aggregated_dataset(df_background)
    return(df_aggr_train2, df_aggr_test2, mcs)

def createAggFeaturesWithMC_background(df_background, mcs):
    df_background = set_sessions(df_background)
    # we create the aggregated feature on the whole datast
    df_aggrFeatures = create_aggregated_dataset(df_background)
    df_background['action'] = df_background.apply(action_of_row, axis=1)
    df_background['action2'] = df_background['action']
    df_aggr_background = df_background.groupby(['SrcAddr', 'session_id']).agg({'action':lambda x: compute_best_score(x, mcs=mcs),
                                                                               'action2':lambda x: compute_best_average(x, mcs=mcs)})
    df_aggr_background.columns = ['session_best_score', 'session_average_score']
    df_aggr_background = df_aggr_background.reset_index()
    df_aggrFeatures = df_aggrFeatures.merge(right=df_aggr_background, how='inner', on=['SrcAddr', 'session_id'])
    return(df_aggrFeatures)

def create_doc_mcs():
    df = pd.read_csv('ctu_normal_infected.csv')
    df['StartTime'] = pd.to_datetime(df['StartTime']) 
    df_train, df_test = split_train_test_scenarios(df)
    mcs = set_mcs(df_train)
    for key in mcs:
        fname = 'dot_mcs/'+key+'.dot'
        dot_mc(mcs[key], fname)


if __name__ == '__main__':
    df, df_background = get_data()
    df = get_data()
    df.to_csv('ctu_normal_infected.csv', index = False)
    df = pd.read_csv('ctu_normal_infected.csv')
    df['StartTime'] = pd.to_datetime(df['StartTime']) 
    #df = df[df.scenario != 1]
    df_train, df_test, mcs = createAggFeaturesWithMC(df)
    df_train.to_csv('df_train_CTU_Feb.csv', index = False)
    df_test.to_csv('df_test_CTU_Feb.csv', index = False)
    #df_background_aggr = creteAggFeaturesWithMC_background(df_background, mcs)
