'''
   This file contains functionaly to parse Sherlock file, extract and generate actions,
   and to derive a FSA/MC for Sherlock data
'''
import os
import csv
from models.dfsa import PTA
from models.ndfsa import *

# Actions we will ignore
# should these be epsilon transformations in a FSA?  
ignored_actions = ['App Mode change','Moriarty end','Moriarty start','Application started','Application end']

def genAction(strname):
    '''
        generate a shorthand action for readability which is just the first letter in each wrod
    '''
    words = strname.split()
    res = ""
    for w in words:
        res = res + w[0]    
    return res

def parse(filename,delimiter=',',header = False,sess_idx = -1,sess_type = -3,sess_act = -5):
    '''
      parses a file and generate sequence of actions for each session
      returns:
         list of list of action of benign and malicious sequences respectively
         map from short-hand action to actual action
    '''
    indx,curr,benign,malicious,sess = 0,0,[],[],[]
    actions = {}
    with open(filename, 'r') as inputfile:
     rd = csv.reader(inputfile, delimiter=delimiter)
     if header:
        next(rd,None)
     sesstype = None
     for row in rd:
         if row:
            if row[sess_act] in ignored_actions:
                continue
            if sesstype == None:
                sesstype = row[sess_type]
                print ("init session: " + sesstype)
            if int(row[sess_idx]) != curr:
                if sesstype == 'malicious':
                    malicious = malicious + [sess]
                else:
                    benign = benign + [sess]
                sess,curr = [],int(row[sess_idx])
            
            act = genAction(row[sess_act])
            actions[act] = row[sess_act]
            sess = sess + [act]
            sesstype = row[sess_type] # new session 
    return (actions,benign,malicious)

def check_negative(fsa,neg_ex):
    '''
        to ensure that no negative examples are satisfied by automata
    '''
    for e in neg_ex:
        if fsa.is_valid(e):
            return False
    return True

def count_test(fsa,neg_ex):
    '''
       counts the number of instances that satisfies or fails for the ex
    '''
    ok = 0
    fail = 0
    for e in neg_ex:
        if fsa.is_valid(e):
            ok = ok + 1
        else:
            fail = fail + 1
    return (ok,fail)

def test_fsa(fsa,pos,neg):
    '''
        checks probability and tests if successful
    '''
    for p in pos:
        (_,pr) = fsa.compute_prob(p)
        (_,apr) = fsa.compute_avg_prob(p)
        print ("Total prob: " + str(pr) + "   Avg prob: " + str(apr))
        if not(fsa.is_valid(p)):
            return False
    print ("** All positive valid")
    for n in neg:
        if fsa.is_valid(n):
            return False
    print ("** All negative invalid")
    return True

def print_actions(acts):
    '''
        prints all the actinos
    '''
    print ("Name \t Description")
    print ("-----------------------")
    for a in acts:
        print (a + "\t" + acts[a])


examples = ['data/Moriarty_2015_Q4','data/Moriarty_2016_Q1','data/Moriarty_2016_Q2','data/Moriarty_2016_Q3',
    'data/Moriarty_2016_Q4']

# for testing purposes
examples = ['test_data/Moriarty_2015_Q4']

#(benign,mal) = parse("data/Moriarty.csv",delimiter=',')
(act,benign,mal) = parse(examples[0],delimiter='\t',sess_idx = -2,sess_type=-4,sess_act=-6)
print (len(benign),len(mal),len(act)) 

pta = PTA("")
for e in benign:
    pta.addAction(e)
fsa = pta_to_bfndfsa(pta)
print ("checking negative")
(ok,fail) = count_test(fsa,mal)
print ("Negative succeeding: " + str(ok) + " negative failing (desirable): " + str(fail))
failing = filter(lambda x: not(fsa.is_valid(x)),mal)
fsa.bluefringe(threshold = 0,strictness=0)#test = lambda fst: check_actions(fst,failing))
fsa.merge_leafs()
print_actions(act)
#fsa.display()

# Code dumped: we should try to run this in parallel
'''
Tests should be run concurrently
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Get a list of files to process
    image_files = glob.glob("*.jpg")

    # Process the list of files, but split the work across the process pool to use all CPUs!
    for image_file, thumbnail_file in zip(image_files, executor.map(make_image_thumbnail, image_files)):
        print(f"A thumbnail for {image_file} was saved as {thumbnail_file}")
'''

