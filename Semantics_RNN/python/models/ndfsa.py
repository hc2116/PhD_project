'''
    Implements non-deterministic automata and Blue-Fringe algorithm. This is handled as a class hierarchy where
    the pure NDFSA doesn't not support blue-fringe.
'''

import csv
from enum import Enum
from collections import defaultdict
import os 
import copy
import heapq
import time
# FIXME: need to remove the "from ." to import with 
from . import dfsa
#import dfsa
import json

class NDFSA(object):
    '''
        Non-deterministic FSA implementation 
    '''

    def __init__(self):
        self.init = "s1"
        self.trans = {} # map to set of wires
        self.states = set()
        self.states.add(self.init)
        self.counter = 1
        self.current = self.init
        # union-find datastructure used to keep track of merged as these naturally fall into equivalent classes
        self.merged = {} 
        self.not_mergable = {}
        self.trans_action = defaultdict(lambda : 0)
        self.trans_total = defaultdict(lambda : 0)

    def is_valid(self, act): 
        '''
            checks if an action sequence is valid
        '''
        states = set([self.init])
        while len(act) > 0:
            nsts = set()
            a = act[0]
            act = act[1:]
            for s in states:
                if s in self.trans and a in self.trans[s]:
                    nsts = nsts.union(self.trans[s][a])
            if len(nsts) == 0:
                return False
            else:
                states = nsts
        return True

    def compute_prob(self,actions):
        '''
            computes the probability of action sequence
              similar assumption as Markov chain (re prob. independence) thus
              just product of each transition prob.
        '''
        states = [(self.init,1.0)]
        act = actions
        while len(act) > 0:
            nsts = []
            a = act[0]
            act = act[1:]
            for (s,p) in states:
                if s in self.trans and a in self.trans[s]:
                    for t in self.trans[s][a]:
                        prob = float(self.trans_action[s,a,t]) / self.trans_total[s]
                        nsts = nsts + [(t,p*prob)]
            if len(nsts) == 0:
                return (False,0.0)
            else:
                states = nsts
        # get largest probability
        res = max([p for (t,p) in states])
        return (True,res)

    def compute_avg_prob(self,actions):
        '''
            Average probability of transitions computed
        '''
        states = [(self.init,0.0)]
        act = actions
        print (len(actions))
        while len(act) > 0:
            nsts = []
            a = act[0]
            act = act[1:]
            for (s,p) in states:
                if s in self.trans and a in self.trans[s]:
                    for t in self.trans[s][a]:
                        prob = float(self.trans_action[s,a,t]) / self.trans_total[s]
                        nsts = nsts + [(t,p + prob)]
            if len(nsts) == 0:
                return (False,0.0) # could also return result so far
            else:
                states = nsts
        # get largest probability
        res = max([p for (t,p) in states])
        return (True,res / len(actions))

    def edit_distance(self,actions):
        '''
            Idea: a lot of repeation for naive (exponential) solution:
             - a lot of similar repeated solution for same problem
             - typically few states:
             - plan work backwards and store solution:
               - shortest edit distance from each state to end
               - should only need to make one edit and lookup solution
               - no solution -> remaining length
            Assumption
             - we never actually changes 
            Plan: use dynamic programming
        '''
        MAX = len(actions)
        i = MAX-1
        res = {}
        # backwards
        max_res = 0
        while i >= 0:
            max_res = max_res + 1
            # for each find shortest edit distance
            # if not existing then it is equal to max_res
            # cannot do insert at this point
            for s in self.trans: # note we only do those with outgoing trans...
                min = max_res
                # delete
                if (s,i+1) in res:
                    tmp_res = res[(s,i+1)]
                    min = tmp_res + 1
                # if not then this wil just be max_res
                for a in self.trans[s]:
                    for t in self.trans[s][a]:
                        if (t,i+1) in res:
                            tmp_res = res[(t,i+1)]
                        else:
                            tmp_res = max_res-1
                        # no change
                        if actions[i] == a:
                            if tmp_res < min:
                                min = tmp_res
                        # sub
                        else:
                            if tmp_res + 1 < min:
                                min = tmp_res + 1
                res[(s,i)] = min        
            # insert
            #   need to do after all other on same level computed
            #   due to transitivity: reducing edit dist for one state here may 
            #   mean that other is reduced. So have to do this until the end 
            changed = True
            while changed:
                changed = False
                for s in self.trans:
                    for a in self.trans[s]:
                        for t in self.trans[s][a]:
                            if (t,i) in res and (s,i) in res:
                                if res[(t,i)] + 1 < res[(s,i)]:
                                    res[(s,i)] = res[(t,i)] + 1
                                    changed = True 
            # next iteration
            i = i - 1
        # return min from init state at level 0
        if (self.init,0) in res:
            min = res[(self.init,0)]
            return ((min,float(min) / MAX))
        else:
            return (MAX,1.0) # should not happen
    
    def edit_distance_direct(self,actions):
        '''
          Computes edit distance (full edit distance, i.e. Levenshtein: remove,delete,change,equal)
        '''
        MAX = len(actions)
        min = MAX
        states = [(self.init,0,actions)]
        while len(states) > 0: 
            print(len(states))         
            nsts = []
            for (st,d,acts) in states:
                # filter out end of action or passed the current smallest
                if len(acts) == 0 or d >= min:
                    if d < min:
                        min = d    
                    continue
                if st in self.trans:
                    for a in self.trans[st]:
                        for t in self.trans[st][a]:
                            # replace/equal
                            if a == acts[0]: # equal
                                nsts = nsts + [(t,d,acts[1:])]
                            else: # make a change
                                nsts = nsts + [(t,d+1,acts[1:])]
                            # insert (even if action is okay as it may shorter)
                                nsts = nsts + [(t,d+1,acts)]
                            # delete (remain in same state)
                                nsts = nsts + [(st,d+1,acts[1:])]
            states = nsts
        # full and normalised Levenshtein distance
        return (min,float(min) / MAX)

    def new_state(self):
        self.counter = self.counter + 1
        state = "s" + str(self.counter)
        self.states.add(state)
        return state

    def add_trans(self,s1,act,s2):
        if not(s1 in self.trans):
            self.trans[s1] = {}
        if not(act in self.trans[s1]):
            self.trans[s1][act] = set()
        self.trans[s1][act].add(s2)
        self.trans_total[s1] = self.trans_total[s1] + 1
        self.trans_action[(s1,act,s2)] = self.trans_action[(s1,act,s2)] + 1

    # FIXME: don't need self + update parent to flatten tree
    def root(self,tree,node):
        '''
            find "represenative" node in union-find to check for equivalence
        '''
        while node in tree:
            node = tree[node]
        return node        

    def find_merged(self,node):
        '''
            find representative node (root) to look up which nodes are now the same
        '''
        return self.root(self.merged,node)

    def check_not_mergable(self,s1,s2):
        '''
            Need to find representative as nodes may be merged between finding possible nodes to 
            merge and actually starting to merge them
        '''
        root1 = self.root(self.not_mergable,s1)
        root2 = self.root(self.not_mergable,s2)
        return root1 == root2

    def set_not_mergable(self,s1,s2):
        root1 = self.root(self.not_mergable,s1)
        root2 = self.root(self.not_mergable,s2)
        if root1 != root2:
            self.not_mergable[root1] = root2

    def merge_states(self,s1,s2, test = lambda x : True,threshold = 0,strictness = 0):
        '''
           Merges states s1 and s2: state s2 is removed and all in/out edges are sent to s2 with probs updated
             will NOT remove non-determinism as this is supported.abs
             algorithm will always terminate as each merge will remove a state
               - inv: all nodes (except init) should have an incoming edge [unless they are in nterm]
           Args:
             test: negative example can be used undo merge (x is the fsa)
             threshold: minium score computed for similarity of s1 and s2: 
             strictness: how to deal with negative outgoing transitions:
                negative: ignore
                0: subtract the number from score
                positive: don't allow
       '''
        if s1 == s2:
            return True
        if self.check_not_mergable(s1,s2):
            return False
        old = copy.deepcopy(self)
        # should never delete init - but can merge into it
        if s2 == self.init:
            return self.merge_states(s2,s1,test)
        # update incoming - 2 steps to avoid for-loop
        tochange = []
        for s in self.trans:
            for a in self.trans[s]:
                if s2 in self.trans[s][a]:
                    tochange = tochange + [(s,a)]
        for (s,a) in tochange:           
            self.trans[s][a].add(s1)
            self.trans[s][a].remove(s2)
        # update outgoing
        if s2 in self.trans:
            for a in self.trans[s2]:
                if not(s1 in self.trans):
                    self.trans[s1] = {}
                if not(a in self.trans[s1]):
                    self.trans[s1][a] = set()
                self.trans[s1][a] = self.trans[s1][a].union(self.trans[s2][a])
        # update counter
        toadd = []
        in_toadd = []
        for (fst,a,tst) in self.trans_action:
            if fst == s2:
                if tst == s2:
                    toadd = toadd + [(a,s1,self.trans_action[(fst,a,tst)])]
                else:
                    toadd = toadd + [(a,tst,self.trans_action[(fst,a,tst)])]
            if tst == s2:
                if fst != s2: #already handled as output???
                    in_toadd = in_toadd + [(fst,a,self.trans_action[(fst,a,tst)])]                
        for (a,tst,val) in toadd:
            self.trans_action[(s1,a,tst)] = self.trans_action[(s1,a,tst)] + val
        for (fst,a,val) in in_toadd:
            self.trans_action[(fst,a,s1)] = self.trans_action[(fst,a,s1)] + val            
        self.trans_total[s1] = self.trans_total[s1] + self.trans_total[s2]
        self.states.remove(s2)
        if s2 in self.trans:
            del self.trans[s2]
        # reset and return false if given test fails.
        # print ("  Starting Testing")
        # start = time.time()
        test_res = test(self)
        #end = time.time()
        #print (  "  Testing completed - running time (s) " + str(end - start))
        if not(test_res):
            # print("  - Counter-example found: merge cancelled")
            self.set_not_mergable(s1,s2)
            self.trans = old.trans
            self.states = old.states
            self.trans_action = old.trans_action
            self.trans_total = old.trans_total
            return False
        else:
            # print("  - No counter-example found")
            return True

    def all_state_pairs(self):
        '''
            Naive implementation to compute all possible state pairs (to merge)
        '''
        pairs = set()
        for s1 in self.states:
            for s2 in self.states:
                if s1 < s2 and not(self.check_not_mergable(s1,s2)):
                    pairs.add((s1,s2))
        return pairs

    def equivalentActions(self,s1,s2):
        '''
            Returns common and disjoint outgoing actions for s1 and s2 states
        '''
        acts1 = set()
        acts2 = set()
        if s1 in self.trans:
            acts1 = set(self.trans[s1].keys())
        if s2 in self.trans:
            acts2 = set(self.trans[s2].keys())
        common = acts1 & acts2
        disjoint = (acts1 ^ acts2) - common
        return (common,disjoint)

    def calculateScore(self,s1,s2,steps = 3,strictness = 0):
        """Calculates score of merging two .
            Adapted from Walkinshaw et al: similarity score of two trans; slight variation!
               steps to ensure termination in presence of loops (default go upto 3 steps)
               
            Keyword arguments:
                steps -- the number of transitions made from this node to compare (default 3)
                strictness -- how to handle disjoint transition:
                    negative -- ignore
                    0 -- each reducuces score by -1
                    1 -- fail: give a very high negative score without overflow (int does not have -infinity)
        """
        if steps < 1:
            return 0
        score = 0
        (common,disjoint) = self.equivalentActions(s1,s2)
        # subtract the total number of transitions that are not common
        if strictness == 0:
            score = score - len(disjoint)
        # strict and negative examples
        elif strictness > 0 and len(disjoint) > 0:
            return -10000
        for a in common:
            score = score + 1
            # pick best route
            max = 0
            for ns1 in self.trans[s1][a]:
                for ns2 in self.trans[s2][a]:
                    res = self.calculateScore(ns1,ns2,strictness,steps-1)
                    if res > max:
                        max = res
            score = score + max
        return score

    def merge_similar(self,threshold = 0,strictness = 0,test = lambda t : True):
        '''
            Naive implementation that merges as many nodes as possible (until not more possible)

            Keyword arguments:
                test -- rule out negative example (if test for given merge fails the merge is undone)
                steps -- the number of transitions made from this node to compare (default 3)
                strictness -- how to handle disjoint transition:
                    negative -- ignore
                    0 -- each reducuces score by -1
                    1 -- fail: give a very high negative score without overflow (int does not have -infinity)
      
        '''
        print ("Merging - total states: " + str(len(self.states)))
        high_score = -1
        hs1,hs2 = "",""
        for s1,s2 in self.all_state_pairs():
            score = self.calculateScore(s1,s2,strictness = strictness)
            if score > high_score:
                high_score,hs1,hs2 = score,s1,s2
        if high_score >= threshold:
            self.merge_states(hs1,hs2,test = test)
            self.merge_similar(threshold,strictness,test = test)  

    def merge_leafs(self):
        '''
          Merges all the leaf nodes with the same incoming action
        '''
        # tests are actually not required
        for s in self.trans:
            for a in self.trans[s]:
                m = [tt for tt in self.trans[s][a] if not(tt in self.trans)]
                while len(m) > 1:
                    s1 = m[0]
                    s2 = m[1]
                    m = m[1:] # s2 will stay
                    self.merge_states(s2,s1)   

class Color(Enum):
    '''
        Used to label nodes in Blue-Fringe algorithm
    '''
    RED = 1
    BLUE = 2
    WHITE = 3 # not really required as we only colour red or blue and white if not coloured.

class BlueFringeNDFSA(NDFSA):
    '''
        Extends NDFSA with much more efficient implementation of Blue-Fringe to merge states 
    '''
    
    def __init__(self):
        super(BlueFringeNDFSA, self).__init__()
        self.good_merges = 0
        self.failed_merges = 0
        self.start_time = 0.0
        self.resetColor()
    
    def resetColor(self):
        '''
            resets colour in the beginning (root is red, children blue, rest white)
        '''
        # keep an ordered list of red and blue
        self.red = [self.init]
        self.blue = []
        if self.init in self.trans:
            for act in self.trans[self.init]:
                for t in self.trans[self.init][act]:
                    #self.color[trans[self.init][act]] = Color.BLUE
                    self.blue = self.blue + [t]      

    def red_blue_pairs(self,threshold = 0,steps = 3):
        '''
            Computes all red/blue pairs, i.e. all pairs that can be merged
        '''
        pairs = []
        added = set()
        for r in self.red:
            for b in self.blue:
                # not sure if this is necessary
                if self.check_not_mergable(r,b):
                    continue
                s = self.calculateScore(r,b,steps = steps)
                if s > threshold:
                    # order by score instead?
                    pairs = pairs + [(s,(r,b))]
                    added.add(b)
        # only need the first element in self.blue that can be removed.
        return (pairs,[nb for nb in self.blue if not(nb in added)])

    
    def promote_blue(self,promote):
        '''
            Promote blue node to red (and updates fringe to blue)
        '''
        p = promote[0]
        self.blue.remove(p)
        # at end of list as it should be the end one
        self.red = self.red + [p]
        # update white fringe
        if p in self.trans:
            for a in self.trans[p]:
                for nst in self.trans[p][a]:
                    if not(nst in self.red or nst in self.blue):
                        self.blue = self.blue + [nst]

    def merge_red_blue(self,pairs,test,threshold,strictness):
        '''
            Actually merges red and blue and updates colour
        '''
        (s,(r,b)) = max(pairs,key = lambda v: v[0])
        if s >= threshold:
            res = self.merge_states(r,b,test = test,threshold = threshold, strictness = strictness)
            if res:
                self.good_merges = self.good_merges + 1
                self.blue.remove(b)
                # update white fringe
                if r in self.trans:
                    for a in self.trans[r]:
                        for nst in self.trans[r][a]:
                            if not(nst in self.red or nst in self.blue):
                                self.blue = self.blue + [nst]
            else:
                self.set_not_mergable(b,r)
                self.failed_merges = self.failed_merges + 1

    def bluefringe(self,threshold = 0,strictness = 0,steps = 3, test = lambda t : True, promote_first = True):
        '''
            Implementation of Blue-Fringe algorithm. 

            Arguments:
                threshold, strictness and test is the same as naive merging
                promote_first relates to two different versions of algoritms:
                  True: we first promote all blue that cannot be first
                  False: we merge before we promote

                  True is default as this is argued to be faster in literature
        
            Properties:
             each step will 
               either merge (and becomes red) or 
               turn blue to red (and update others)
             Thurs eventually all states will be red assuming all nodes are connected to init
        '''

        self.resetColor()
        # reset
        self.not_mergable = {}
        self.start_time = time.time()
        while self.red != self.states:
            if self.good_merges % 20 == 0:
                self.print_progress()
            (pairs,promote) = self.red_blue_pairs(threshold = threshold,steps = steps)
            if promote_first:
                # promote shallowest (invariant should ensure that the shallowest is first in list)
                if len(promote) > 0:
                    self.promote_blue(promote)
                elif len(pairs) > 0:
                    self.merge_red_blue(pairs,test,threshold,strictness)
                else: # pairs empty and not promoted: halt
                    return
            else: # merge first - SEEMS SLOWER BUT WILL DO MORE MERGES (not checked though)
                if len(pairs) > 0: 
                    self.merge_red_blue(pairs,test,threshold,strictness)
                elif len(promote) > 0:
                    self.promote_blue(promote)    
                else: # pairs empty and not promoted: halt
                    return

    def print_progress(self):
        curr = time.time()
        elapsed = curr - self.start_time
        minutes, seconds = divmod(elapsed, 60)
        print ("Elapsed time: {:0>2}:{:05.2f} Merges: {} Failed: {} States: {}".format(int(minutes),seconds,
                            self.good_merges,self.failed_merges,len(self.states)))

    def to_json(self):
        SEP = "@@"
        record = {}
        trans_rec = {}
        trans_act_rec = {}
        for s in self.trans:
            for a in self.trans[s]:
                # keys must be strings
                trans_rec[s + SEP + a] = list(self.trans[s][a])
                for t in self.trans[s][a]:
                    trans_act_rec[s + SEP + a + SEP + t] = self.trans_action[s,a,t]
        record['init'] = self.init
        record['states'] = list(self.states)
        record['trans'] = trans_rec
        record['current'] = self.current
        record['counter'] = self.counter
        record['merged'] = self.merged
        record['not_mergable'] = self.not_mergable
        record['trans_action'] = trans_act_rec
        record['trans_total'] = self.trans_total
        record['good_merges'] = self.good_merges
        record['failed_merges'] = self.failed_merges 
        # other fields are only needed for blue-fringe algorithm
        rjson = json.dumps(record)
        return rjson

    def from_json(self,rjson):
        SEP = "@@"
        record = json.loads(rjson)
        self.init = record['init']
        self.states = set(record['states'])
        self.current = record['current']
        self.counter = record['counter']
        self.merged = record['merged']
        self.not_mergable = record['not_mergable']
        self.good_merges = record['good_merges']
        self.failed_merges = record['failed_merges']  
        self.trans = {}
        for tr in record['trans']:
            v = tr.split(SEP)
            s = v[0]
            a = v[1]
            if not(s in self.trans):
                self.trans[s] = {}
            self.trans[s][a] = set(record['trans'][tr])

        self.trans_action = defaultdict(lambda : 0)
        for tr in record['trans_action']:
            v = tr.split(SEP)
            s = v[0]
            a = v[1]
            t = v[2]
            self.trans_action[s,a,t] = record['trans_action'][tr]

        # not sure if the defaultvalue is handled by serialision so build from scratch
        self.trans_total = defaultdict(lambda : 0)
        for s in record['trans_total']:
            self.trans_total[s] = record['trans_total'][s]

def save_fsa(filename,fsa):
    '''
      Converts to JSON and stores.
        Note: pickle not working as we have lambdas
    '''
    data = fsa.to_json()
    obj = open(filename, 'wb')
    obj.write(bytes(data, 'UTF-8'))
    obj.close

def load_fsa(filename):
    '''
        Load JSON file and convert into FSA
    '''

    # should be some more high-level ways
    with open(filename, 'r') as myfile:
        data=myfile.read().replace('\n', '')
        fsa = BlueFringeNDFSA()
        fsa.from_json(data)
    return fsa


def pta_to_bfndfsa(pta):
    '''
        Converts given PTA into automata (non-determ with blue-fringe)
          Iterative implementation as (simpler) recursive will give overflow stack with calls due to size 
          of data
    '''
    fsa = BlueFringeNDFSA()
    rest = [(fsa.init,pta.children[c]) for c in pta.children]
    while len(rest) > 0:
        (s,n) = rest[0]
        rest = rest[1:]
        nst = fsa.new_state()
        fsa.add_trans(s,n.action,nst)
        ch = [(nst,n.children[nc]) for nc in n.children]
        rest = rest + ch
    return fsa

def check_actions(fsa,neg):
    '''
        helper function that make sure that no given (negative) example is valid in fsa
    '''
    for n in neg:
        if fsa.is_valid(n):
            return False
    return True

def dot_ndfsa(fsa,filename = "fsa.dot"):
    steps = {}

    # just one edge between two states to simplify diagram
    for s1 in fsa.trans:
        for a in fsa.trans[s1]:
            for s2 in fsa.trans[s1][a]:
                if fsa.trans_total[s1] > 0:
                    prob0 = float(fsa.trans_action[s1,a,s2]) /fsa.trans_total[s1]
                    prob = format(prob0, '.3f')
                    pstr = a + "/" + prob
                else:
                    pstr = a + "/NP"
                if (s1,s2) in steps:
                    steps[(s1,s2)] =  steps[(s1,s2)] + " , " + pstr
                else:
                    steps[(s1,s2)] =  pstr
    str = "digraph {\n"
    for (s1,s2) in steps:
        str = str + "  " + s1 + "->" + s2 + "[label=\"" + steps[(s1,s2)] + "\"]\n"
    str = str + "}"
    obj = open(filename, 'wb')
    obj.write(bytes(str, 'UTF-8'))
    obj.close

## testing
if __name__ == "__main__":
    pta = dfsa.PTA("")
    examples = [['a','b','c'],['a','c'],['b','c']]
    for e in examples:
        pta.addAction(e)
    fsa = pta_to_bfndfsa(pta)
    print (check_actions(fsa,[["c","b"]]))
    #fsa.merge_similar(threshold = 0,strictness=0,test = lambda fst: check_actions(fst,[["a","b","b"]]))
    fsa.bluefringe(threshold = 0,strictness=0,test = lambda fst: check_actions(fst,[["a","b","b"]]))
    fsa.merge_leafs()
    save_fsa("fname.json",fsa)
    nfsa = load_fsa("fname.json")
    #save_fsa('fsa.obj',fsa)
    #del fsa
    #fsa = load_fsa('fsa.obj')
    #print (nfsa.compute_avg_prob(['a','b','c']))
    #print (nfsa.compute_prob(['a','b','c']))
    print (nfsa.edit_distance(['a','a','b','d']))   
    dot_ndfsa(nfsa)



