import os
import numpy as np
import pandas as pd
import scipy
import re



"""
In this script we read and understand 3 tables from the free subsample of the Sherlock dataset:
 - T4: contains systems statistics acquired from the Linux /proc folder
 - Moriarty: this table contains the Labels! The Version field gives us information about the malicious app
 - Applications: this table gives us application behaviours every 5 seconds!
"""


os.chdir(os.path.join(os.environ["HOME"],"Projects/Cybersecurity/detlearsom"))


# T4 table contains systems statistics acquired from the Linux /proc folder
df_T4 = pd.read_csv("data/input/Sherlock/T4.csv")
df_T4.columns = [col.lower() for col in df_T4.columns]

# Moriarty table contains the Labels! The Version field gives us information about the malicious app
moriarty = pd.read_csv("data/input/Sherlock/Moriarty.csv")  # I get the following error: Expected 8 fields in line 18, saw 9
# if we check the corresponding line in a text editor, we see that there are commas in a parenthesis!

# we do some regular expression magic in order to remove commas within parentheses
moriarty = []
with open("data/input/Sherlock/Moriarty.csv") as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n','')
        line = line.replace('\ufeff', '')
        line = re.sub(r"\([^{}]+\)", lambda x: x.group(0).replace(",", ";"), line)
        line = line.split(",")
        moriarty.append(line)

df_moriarty = pd.DataFrame.from_records(moriarty[1:], columns=moriarty[0])
df_moriarty['UUID'] = df_moriarty['UUID'].astype(dtype=float)
df_moriarty.loc[np.where(df_moriarty['UUID'].isnull())]

# we remove the last row
df_moriarty.drop(df_moriarty.index[np.where(df_moriarty['UUID'].isnull())], inplace = True)


# column names to lower 
df_moriarty.columns = [col.lower() for col in df_moriarty.columns]


# we get timestamp from UUID
df_moriarty['timestamp'] = pd.to_datetime(df_moriarty['uuid'], unit='ms')
df_T4['timestamp'] = pd.to_datetime(df_T4['uuid'], unit='ms')

# we need to create a df like Figure1 in  http://bigdata.ise.bgu.ac.il/sherlock/#/dataset
# in order to know what the filed 'version' in df_moriarty corresponds to
apps = ['Puzzle Game', 'Web Browser', 'Utiliz Widget', 'Sports App', 'Angry Birds',
        'Game', 'Game', 'Lock Screen', 'File Manager', 'None', 
        'Music Player', 'Web Media Player']
malicious_behaviour = ['Contact Thefts', 'Spyware', 'Photo Theft', 'SMS Bank Thief',
                       'Phishing', 'Adware', 'Madware', 'Ransom-ware', 
                       'Click-Jacking', 'Device Theft', 'Botnet', 'Recon. Infiltration']
malware_sample = ['SaveMe_SocialPath', 'Code4hk_xRAT', 'Photsy_Phopsy', 'Spy.Agent.SI',
                  'Xbot','Adware','Madware', 'Simplelocker.A_SLocker', 'Shedum (GhotstPush)',
                  'Theft', 'Tascudap.A_Nitmo.A', '']
lk_table = pd.DataFrame({'version':range(1,13), 'benign_application': apps,
                         'malicious_bahvaiour' : malicious_behaviour, 'malware_sample' : malware_sample})

# Unique values
df['Userid'].unique()
df['UUID'].unique().shape



# WE NEED TO merge Moriarty with T4 using UUID (or TimeStamp)
# like this we will be able to relate malicious/benign events with phone behaviour  
#TODO


# Applications table gives us Application behaviours! 
# To start, we read the file ApplicationName created from the UNIX terminal, taking the 3rd field of Applications.csv
# The Applications.csv has a size of 4GB, so it's too big to do this first exploratory analysis
# unix command: cut -f 3 -d "," Applications.csv > ApplicationName.csv
applicationName = pd.read_csv("data/input/Sherlock/ApplicationName.csv")
l = list(applicationName['ApplicationName'].unique())
l.sort()
# there is the Moriarty application
# TODO: create the SQL database to query from Applications. We will be able to query normal, and malicious applications
# and load into memory only the records we are interested in

