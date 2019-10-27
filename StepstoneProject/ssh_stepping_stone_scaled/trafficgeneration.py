#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 17:41:15 2019

@author: henry
"""

#import os
import sys
import numpy as np
import random
import string
#import matplotlib.pyplot as plt

netcat_para1 = 10000
while netcat_para1>3:
    netcat_para1 = float(abs(np.random.standard_cauchy(1))*0.1+0.0001)

netcat_para2 = 1000000000
while netcat_para2>100000:
    netcat_para2 = float(abs(np.random.standard_cauchy(1))*5000+500)

netcat_para3 = 100000
while netcat_para3>2000:
    netcat_para3 = int(abs(np.random.standard_cauchy(1))*100)

#####################################################################

netcat_para4 = 10000
while netcat_para4>3:
    netcat_para4 = float(abs(np.random.standard_cauchy(1))*0.1+0.0001)

netcat_para5 = 1000000000
while netcat_para5>100000:
    netcat_para5 = float(abs(np.random.standard_cauchy(1))*5000+500)

netcat_para6 = 100000
while netcat_para6>2000:
    netcat_para6 = int(abs(np.random.standard_cauchy(1))*100)

#####################################################################

delay_para1 = 10000
while delay_para1>300:
    delay_para1 = int(abs(np.random.normal(1))*20+1)

delay_para2 = 10000
while delay_para2>50:
    delay_para2 = int(abs(np.random.normal(1))*8+1)

delay_para3 = int(abs(np.random.uniform(1,200)))

delay_para4 = delay_para3 #int(abs(np.random.uniform(delay_para3,1001)))

delay_para5 = 10000
while delay_para5>300:
    delay_para5 = int(abs(np.random.normal(1))*20+1)

delay_para6 = 10000
while delay_para6>50:
    delay_para6 = int(abs(np.random.normal(1))*8+1)

#####################################################################


commands = ['ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'rm','ls', 'sleep', 'mkdir', 'touch', 'echo',
             'pwd', 'exit']

def create_ssh_file(suffix=""):
    filename="scripts/ssh_scripts/ssh-trafficgenerator"+suffix+".sh"
    fid = open(filename, 'w')
    fid.write('#!/bin/sh\n')
    fid.write('HOST=$1\n')
    fid.write('PORT=$2\n')
    fid.write('USER="root"\n')
    fid.write('PASS="root"\n')

    flip = np.random.randint(0, 1)
    if flip==0:
        fid.write('sshpass -p $PASS ssh -v -4 -o StrictHostKeyChecking=no -p $PORT $USER@$HOST << !\n')
        writestring=''
        while writestring!='exit':
            writestring=commands[np.random.randint(0,len(commands))]
            ##############################################################
            if writestring=='sleep':
                sleeptime = 4000
                while sleeptime>400:
                    sleeptime = int(abs(np.random.standard_cauchy(1))*10)
                writestring+=' '+str(sleeptime)
            ##############################################################
            if writestring=='mkdir':
                dirlen = 4000
                while dirlen>254:
                    dirlen = int(abs(np.random.standard_cauchy(1))*10)+2
                dirname=''.join(random.choices(string.ascii_uppercase + string.digits, k=dirlen))
                writestring+=' /'+str(dirname)
            ##############################################################
            if writestring=='touch':
                dirlen = 4000
                while dirlen>254:
                    dirlen = int(abs(np.random.standard_cauchy(1))*10)+2
                dirname=''.join(random.choices(string.ascii_uppercase + string.digits, k=dirlen))
                writestring+=' /dataToShare/'+str(dirname)
            ##############################################################
            if writestring=='ls':
                flip2 = np.random.randint(0, 2)
                if flip2==1:
                    writestring+=' /dataToShare'
            ##############################################################
            if writestring=='echo':
                dirlen = 4000
                while dirlen>254:
                    dirlen = int(abs(np.random.standard_cauchy(1))*10)+2
                dirname=''.join(random.choices(string.ascii_uppercase + string.digits, k=dirlen))
                content = 400001
                while content>400000:
                    content = int(abs(np.random.standard_cauchy(1))*1000)+2
                content=''.join(random.choices(string.ascii_uppercase + string.digits, k=content))
                writestring+=' '+str(content)+' > /'+str(dirname)
            ##############################################################
            if writestring in ['head','tail','rm']:
                writestring+=' /dataToShare/$(ls /dataToShare | sort -R | tail -1)\n'
                fid.write('echo "removed"\n')
            ##############################################################
            if writestring=='exit':            
                fid.write('sleep 1\n')
                
            fid.write(writestring+'\n')
    
    
    fid.write('!\n')
    fid.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='distinguish ssh-scripts')
    parser.add_argument('-s', '--suffix', default=None,
            help='specify the ssh-script suffix')
    
    args = parser.parse_args()
    
    create_ssh_file(str(args.suffix))
    #import time
    #time.sleep(100)
    print(netcat_para1)
    print(netcat_para2)
    print(netcat_para3)
    print(netcat_para4)
    print(netcat_para5)
    print(netcat_para6)

    print(delay_para1)
    print(delay_para2)
    print(delay_para3)
    print(delay_para4)
    print(delay_para5)
    print(delay_para6)



#plt.hist(np.exp(np.random.uniform(0,np.log(3),10000)),bins=100)
#plt.hist(abs(np.random.normal(0,0.2,10000)),bins=100)
#x=abs(np.random.standard_cauchy(10000))*10
#plt.hist(x[x<400],bins=100)
#np.mean(x[x<3])
#np.quantile(abs(np.random.normal(0,0.2,10000)),q=[0.5,0.8,0.9,0.95,0.99])
#x=np.random.uniform(1,30000,10000)
#xx=100000*(np.tan(0.5*x/32767*np.pi))
#plt.hist(xx,bins=100)
