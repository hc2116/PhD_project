import os
import numpy as np
import pandas as pd


DATA_PATH = '/home/henry/Desktop/Project/Data/CTU/'

def read_data(scenario, inputfile, infected_hosts, normal_hosts):
    print('scenario: {}\n'.format(scenario))
    df = pd.read_csv(inputfile, header=(0))
    df['BytesPkt'] = df.TotBytes/df.TotPkts
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    df['scenario'] = scenario
    df = df.sort_values('StartTime', ascending=True)
    #df = df[['scenario']]
    if scenario == 1:
        df = df[-df.Label.str.contains('Background')]
        df = df.assign(is_normal = df.Label.str.contains('Normal'))
        df = df.assign(label_bot = 'normal')
        df.loc[df.is_normal==False, 'label_bot'] = 'infected'
        #df = df['StartTime', 'Proto', 'SrcAddr', 'Dport', 'DstAddr', 'scenario']
    else:
        #df_background = df[-df.SrcAddr.isin(infected_hosts+normal_hosts)]
        df = df[df.SrcAddr.isin(infected_hosts+normal_hosts)]
        df = df.assign(label_bot = 'normal')#df['label_bot'] = 'normal'
        df.loc[df.SrcAddr.isin(infected_hosts), 'label_bot'] = 'infected'
        #df['label_bot'][df.SrcAddr.isin(infected_hosts)] = 'infected'
    df = df[['StartTime', 'Proto', 'SrcAddr', 'Dport', 'DstAddr', 'scenario', 'BytesPkt', 'TotPkts', 'label_bot']]
    #df_background['label_bot'] = 'background'
    #return(df, df_background)
    return(df)

def create_metadata():
    d = dict()
    # scenario 1 from https://mcfp.weebly.com/ctu-malware-capture-botnet-42.html
    d[1] = dict()
    d[1]['infected_hosts'] = []
    d[1]['normal_hosts'] = []
    d[1]['scenario'] = 1
    d[1]['inputfile'] = os.path.join(DATA_PATH, 'capture20110810.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-43/
    d[2]=dict()
    d[2]['infected_hosts'] = ['147.32.84.165']
    d[2]['normal_hosts'] = ['147.32.84.170', '147.32.84.164', '147.32.87.36', '147.32.80.9','147.32.87.11']
    d[2]['scenario'] = 2
    d[2]['inputfile'] = os.path.join(DATA_PATH, 'capture20110811.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-44/
    d[3] = dict()
    d[3]['infected_hosts'] = ['147.32.84.165']
    d[3]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[3]['scenario'] = 3
    d[3]['inputfile'] = os.path.join(DATA_PATH, 'capture20110812.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-45/
    d[4] = dict()
    d[4]['infected_hosts'] = ['147.32.84.165']
    d[4]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[4]['scenario'] = 4
    d[4]['inputfile'] = os.path.join(DATA_PATH, 'capture20110815.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-46/
    d[5] = dict()
    d[5]['infected_hosts'] = ['147.32.84.165']
    d[5]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[5]['scenario'] = 5
    d[5]['inputfile'] = os.path.join(DATA_PATH, 'capture20110815-2.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-47/
    d[6] = dict()
    d[6]['infected_hosts'] = ['147.32.84.165']
    d[6]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[6]['scenario'] = 6
    d[6]['inputfile'] = os.path.join(DATA_PATH, 'capture20110816.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-48/
    d[7] = dict()
    d[7]['infected_hosts'] = ['147.32.84.165']
    d[7]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9']
    d[7]['scenario'] = 7
    d[7]['inputfile'] = os.path.join(DATA_PATH, 'capture20110816-2.binetflow.2format')


    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-49/
    d[8] = dict()
    d[8]['infected_hosts'] = ['147.32.84.165']
    d[8]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[8]['scenario'] = 8
    d[8]['inputfile'] = os.path.join(DATA_PATH, 'capture20110816-3.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-50/
    d[9] = dict()
    d[9]['infected_hosts'] = ['147.32.84.165', '147.32.84.191','147.32.84.192', '147.32.84.193', '147.32.84.204', '147.32.84.205', '147.32.84.206', '147.32.84.207', '147.32.84.208', '147.32.84.209']
    d[9]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[9]['scenario'] = 9
    d[9]['inputfile'] = os.path.join(DATA_PATH, 'capture20110817.binetflow.2format')


    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-51/
    d[10] = dict()
    d[10]['infected_hosts'] = ['147.32.84.165', '147.32.84.191','147.32.84.192', '147.32.84.193', '147.32.84.204', '147.32.84.205', '147.32.84.206', '147.32.84.207', '147.32.84.208', '147.32.84.209']
    d[10]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[10]['scenario'] = 10
    d[10]['inputfile'] = os.path.join(DATA_PATH, 'capture20110818.binetflow.2format')


    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-52/
    d[11] = dict()
    d[11]['infected_hosts'] = ['147.32.84.165', '147.32.84.191','147.32.84.192'] 
    d[11]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[11]['scenario'] = 11
    d[11]['inputfile'] = os.path.join(DATA_PATH, 'capture20110818-2.binetflow.2format')

    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-53/
    d[12] = dict()
    d[12]['infected_hosts'] = ['147.32.84.165', '147.32.84.191','147.32.84.192'] 
    d[12]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[12]['scenario'] = 12
    d[12]['inputfile'] = os.path.join(DATA_PATH, 'capture20110819.binetflow.2format')


    # infected and normal hosts list from https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-54/
    d[13] = dict()
    d[13]['infected_hosts'] = ['147.32.84.165']
    d[13]['normal_hosts'] = ['147.32.84.170', '147.32.84.134', '147.32.84.164', '147.32.87.36', '147.32.80.9', '147.32.87.11']
    d[13]['scenario'] = 13
    d[13]['inputfile'] = os.path.join(DATA_PATH, 'capture20110815-3.binetflow.2format')

    return(d)


def create_dataset(d):
    l = [read_data(d[k]['scenario'], d[k]['inputfile'], d[k]['infected_hosts'], d[k]['normal_hosts']) for k in d.keys()]
#    for i, (df) in enumerate(l):
#        print('scenario {}'.format(i))
#        df.label_bot.value_counts()
    #ll_normal_infected = [it[0] for it in l]
    #ll_background = [it[1] for it in l]
    #df = pd.concat(ll_normal_infected, axis=0)
    df = pd.concat(l, axis=0)
    #df_background = pd.concat(ll_background, axis=0) 
    #return(df, df_background)
    return(df)


