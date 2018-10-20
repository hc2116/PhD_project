import csv
from option import none,value
from enum import Enum
from collections import defaultdict
import pygraphviz as pgv
import os 
import copy
import heapq
import time

# Support for non-determinism
class FSA(object):

    def __init__(self): 
        self.init = "s1"
        self.trans = {}
        self.states = set()
        self.states.add(self.init)
        self.counter = 1
        self.current = self.init
        # inv: if any two states cannot be merged, then so cannot any merging of these states with others
        self.not_mergable = set()
        # for probabilities (use 0 as default to simplify code)
        self.state_total = defaultdict(lambda : 0)
        self.total = defaultdict(lambda : defaultdict(int))
        # keep track of merged
        self.top_merge = 0 # top-level merge
        self.determ_merge = 0 # merge to reduce non-determinsm
        # union-find datastructure to keep track of merged states
        self.merged = {}

    def new_state(self):
        self.counter = self.counter + 1
        state = "s" + str(self.counter)
        self.states.add(state)
        return state

    # note that this will override previous ones 
    # should never happen from PTA though
    def add_trans(self,s1,act,s2):
        if not(s1 in self.trans):
            self.trans[s1] = {}
        self.trans[s1][act] = s2
        self.state_total[s1] = self.state_total[s1] + 1
        self.total[s1][act] = self.total[s1][act] + 1

    def is_valid(self, act): 
        _st = self.init
        while len(act) > 0:
            # decreases: act either reduced or loop terminated 
            if act[0] in self.trans[_st]:
                _st = self.trans[_st][act[0]]
                act = act[1:]
            else:
                return False
        return True

    def start(self):
        self.current = self.init

    def step(self, action):
        if self.current in self.trans and action in self.trans[self.current]:
            self.current = self.trans[self.current][action]
            return True
        else:
            return False

    ## from current state
    def get_actions(self):
        return list(self.trans[self.current].keys())

    def is_accepting(self):
        return self.current in self.acc

    def all_state_pairs(self):
        pairs = set()
        # naive implementation
        for s1 in self.states:
            for s2 in self.states:
                if s1 < s2 and not(set([s1,s2]) in self.not_mergable):
                    pairs.add((s1,s2))
        #print self.states
        #print pairs
        return pairs

    def not_mergable_pair(self,s1,s2):
        return set([s1,s2]) in self.not_mergable

    def updated_mergable(self,into_state,from_state):
        for pairs in self.not_mergable:
            if from_state in pairs:
                self.not_mergable.remove(pairs)
                newset = (pairs - set(from_state)) ^ set(into_state)
                self.not_mergable.add(newset)

    # return root of node
    def find_merged(self,node):
        while node in self.merged:
            #print (node,self.merged[node])
            node = self.merged[node]
        #print "****************** END *************"
        return node

    def unreachable_states(self,ignored):
        incoming = set()
        for s in self.trans:
            for a in self.trans[s]:
                    incoming.add(self.trans[s][a])
        missing = self.states - incoming
        for (s1,s2) in ignored:
            if s1 in missing:
                missing.remove(s1)
            if s2 in missing:
                missing.remove(s2)
        if self.init in missing:
            missing.remove(self.init)
        return missing

    

    def remove_nondetermism(self,pairs,test = lambda x : True,threshold = 0,strictness = 0,check_threshold = False):
        # we don't need to care about keeping old state as this will be reset by caller (merge_states)
        while len(pairs) > 0:
            invalid = self.unreachable_states(pairs)
            if len(invalid) > 0:
                print "Invalid: " + str(invalid)
            # invariant: all nodes (except self.init) should have at least one incoming wire 
            ss1,ss2 = pairs[0]
            # in case either has changed
            s1,s2 = self.find_merged(ss1),self.find_merged(ss2)
            # TODO: add check that if ss1 != s1 => ss1 is not a state!
            pairs = pairs[1:]
            if s1 == s2:
                continue
            if s2 == self.init:
                s1,s2 = s2,s1
            if self.not_mergable_pair(s1,s2):
                return False
            # if we should check threshold on recursive merges
            if check_threshold:
                score = self.calculateScore(s1,s2,strictness = strictness)
                if score < threshold:
                    return False
            # INCOMING WIRES
            # should really not update in for loop so split into two loops
            # not in this case
            tochange = []
            for s in self.trans:
                for a in self.trans[s]:
                    if self.trans[s][a] == s2:
                        tochange = tochange + [(s,a)]
            # all s2 should have incoming edges so should never be 0
            #if tochange == []:
            #    print "No incoming " + s2 
            #    print pairs
            for (s,a) in tochange:
                self.trans[s][a] = s1 
            # OUTGOING WIRES
            if s2 in self.trans:
                for a in self.trans[s2]:
                    # handle non-determinism
                    if s1 in self.trans and a in self.trans[s1] and self.trans[s1][a] != self.trans[s2][a]:
                        pairs = pairs + [(self.trans[s1][a],self.trans[s2][a])]      
                    else:
                        # doesn't matter if we loose trans[s1][a] transition as this state will be merged with self.trans[s2][a]
                        #   which we already have a linked to (and have copied over probabilities)
                        # Q: is this the case? Lost input edges to some node when added below
                        if not(s1 in self.trans):
                            self.trans[s1] = {}
                        self.trans[s1][a] = self.trans[s2][a]
                # in case s1 does not have any transitions
                #if not(s1 in self.trans):
                #    self.trans[s1] = {}
                # update as they will be merging (if they are not overlapping then the other is just 0)
                self.total[s1][a] = self.total[s1][a] + self.total[s2][a]
            self.state_total[s1] = self.state_total[s1] + self.state_total[s2]
            self.states.remove(s2)
            if s2 in self.trans:
                del self.trans[s2]
            self.merged[s2] = s1 # s2 should now be s1
            self.determ_merge = self.determ_merge + 1
            if not(test(self)):
                return False
        return True



    # s2 becomes s1
    # also merges destination if it introduces non-determinism
    #  will always terminates as each merge will remove a state
    # INVARIANTS:
    #  all nodes (except init) should have an incoming edge [unless they are in nterm]
    def merge_states(self,s1,s2, test = lambda x : True,threshold = 0,strictness = 0):
        # Require/assume that this will never be the case
        if s1 == s2:
            return True
        if self.not_mergable_pair(s1,s2):
            return False
        old = copy.deepcopy(self)
        # should never delete init - but can merge into it
        if s2 == self.init:
            return self.merge_states(s2,s1,test)
        # to store pairs of states that causes non-determinism (will be merged)
        ndeterm = []
        # update incoming - 2 steps to avoid for-loop
        tochange = []
        for s in self.trans:
            for a in self.trans[s]:
                if self.trans[s][a] == s2:
                    tochange = tochange + [(s,a)]
        for (s,a) in tochange:
            self.trans[s][a] = s1 
        # update outgoing - may lead to non-determinism
        if s2 in self.trans:
            for a in self.trans[s2]:
                # handle non-determinism
                if s1 in self.trans and a in self.trans[s1] and self.trans[s1][a] != self.trans[s2][a]:
                    ndeterm = ndeterm + [(self.trans[s1][a],self.trans[s2][a])]      
                else:
                    # doesn't matter if we loose trans[s1][a] transition as this state will be merged
                    # Q: is this the case? Lost input edges to some node when added below
                    if not(s1 in self.trans):
                        self.trans[s1] = {}
                    self.trans[s1][a] = self.trans[s2][a]
                # in case s1 does not have any transitions
                if not(s1 in self.trans):
                    self.trans[s1] = {}
                # update as they will be merging (if they are not overlapping then the other is just 0)
                self.total[s1][a] = self.total[s1][a] + self.total[s2][a]
        self.state_total[s1] = self.state_total[s1] + self.state_total[s2]
        # delete state (we have now updated all incoming and outgoing edges)
        #print ("State " + s2 + " removed")
        self.states.remove(s2)
        if s2 in self.trans:
            del self.trans[s2]
        self.merged[s2] = s1 # s2 should now be s1
        # recursively merge to make it deterministic
        res = self.remove_nondetermism(ndeterm,test,threshold = threshold,strictness = strictness)
        # reset and return false if given test fails.
        if (res == False) or not(test(self)):
            self.init = old.init
            self.trans = old.trans
            self.states = old.states
            self.state_total = old.state_total
            self.total = old.total
            self.top_merge = old.top_merge
            self.determ_merge = old.determ_merge
            # remove any recursive update to not_mergable:
            self.not_mergable = old.not_mergable
            # these states should not be attempted again 
            self.not_mergable.add(set([s1,s2]))
            self.merged = old.merged
            return False
        else:
            self.top_merge = self.top_merge + 1
            print ("-- Top-level: " + str(self.top_merge) + " --- Non-determinism: " + str(self.determ_merge) + " --- states: " + str(len(self.states)))
            return True

    def equivalentActions(self,s1,s2):
        acts1 = set()
        acts2 = set()
        if s1 in self.trans:
            acts1 = set(self.trans[s1].keys())
        if s2 in self.trans:
            acts2 = set(self.trans[s2].keys())
        common = acts1 & acts2
        disjoint = (acts1 ^ acts2) - common
        return (common,disjoint)

    # from Walkinshaw et al: similarity score of two trans; slight variation!
    # steps to ensure recursion.
    def calculateScore(self,s1,s2,steps = 3,strictness = 0):
        """Calculates score of merging two .

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
        # else do nothing (ignore)

        for a in common:
            score = score + 1
            rest = self.calculateScore(self.trans[s1][a],self.trans[s2][a],strictness,steps-1)
            score = score + rest
        return score

    # naive computing of similar and merging
    def merge_similar(self,threshold = 0,strictness = 0,test = lambda t : True):
        high_score = -1
        hs1,hs2 = "",""
        # recursive so cannot reset not mergable
        #self.not_mergable = set()
        # FIXME: should not use for here!
        for s1,s2 in self.all_state_pairs():
            score = self.calculateScore(s1,s2,strictness = strictness)
            if score > high_score:
                high_score,hs1,hs2 = score,s1,s2
        #print high_score
        if high_score >= threshold:
            self.merge_states(hs1,hs2,test = test)
            self.merge_similar(threshold,strictness)

    def generate_dot(self, filename = 'fsa.dot'):
        A = pgv.AGraph(strict = False,directed=True)
        A.add_node("__into__init")
        init = A.get_node("__into__init")
        init.attr['label'] = ' '
        init.attr['shape'] = 'point'
        A.add_edge("__into__init",self.init)
        steps = {}
        # just one edge between two states to simplify diagram
        for s in self.trans:
            for a in self.trans[s]:
                prob0 = float(self.total[s][a]) / self.state_total[s]
                prob = format(prob0, '.3f')
                pstr =  a + "/" + prob
                if (s,self.trans[s][a]) in steps:
                    steps[(s,self.trans[s][a])] =  steps[(s,self.trans[s][a])] + " , " + pstr
                else:
                    steps[(s,self.trans[s][a])] =  pstr
        for (s1,s2) in steps:
            A.add_edge(s1,s2)
            edge = A.get_edge(s1,s2)
            edge.attr['label'] = steps[(s1,s2)]
        '''
        for s in self.trans:
            for a in self.trans[s]:
                A.add_edge(s,self.trans[s][a])
                edge = A.get_edge(s,self.trans[s][a])
                prob = float(self.total[s][a]) / self.state_total[s]
                edge.attr['label'] = a + "/" + str(prob) '''
        #print(A.string()) # print qto screen
        A.write(filename) # write to simple.dot 

    def display(self, dotfile = 'fsa.dot',pngfile = 'fsa.png'):
        self.generate_dot()
        os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile)

class PTA:

    def __init__(self,action):
        self.action = action
        self.counter = 1
        self.accept = False
        self.children = {}
    
    def __str__(self):
        ret = ""
        for e in self.children:
            ret = ret + self.children[e].str(" ")        
        return ret

    def str(self,tab):
        if self.accept:
            ret = tab +  "|" + self.action + "|" + "\n"
        else:
            ret = tab + self.action + "\n"            
        for e in self.children:
            ret = ret + self.children[e].str(tab + " ")
        return ret

    def addAction(self,act):
        self.counter = self.counter + 1
        if not(act[0] in self.children):
            self.children[act[0]] = PTA(act[0])
        if act[1:]:
            self.children[act[0]].addAction(act[1:])
        else:
            self.children[act[0]].accept = True

    # iterative version (recursion causes issues for large examples)
    def add_action_iter(self,act):
        curr = self
        while len(act) > 0:
            curr.counter = curr.counter + 1
            if not(act[0] in curr.children):
                curr.children[act[0]] = PTA(act[0])
            curr = curr.children[act[0]]
            act = act[1:]
        curr.accept = True

    #membership (root only)
    def member(self,x):
        if not(x[0] in self.children):
            return False
        return self.children[x[0]].member_dtree(x)
    
    #membership for non-root nodes
    def member_dtree(self,x):
        if not(x[0] in self.children):
            return False
        if x[1:]:
            return self.children[x[0]].member_dtree(x[1:])
        else:
            return self.children[x[0]].accept  

    def to_fsa_step(self,fsa,state):
        nst = fsa.new_state()
        fsa.add_trans(state,self.action,nst)
        for c in self.children:
            self.children[c].to_fsa_step(fsa,nst)

    def to_fsa(self):
        fsa = FSA()
        ## root does not have any action 
        for c in self.children:
            self.children[c].to_fsa_step(fsa,fsa.init)
        return fsa

    '''def to_ndfsa_step(self,fsa,state):
        nst = fsa.new_state()
        fsa.add_trans(state,self.action,nst)
        for c in self.children:
            self.children[c].to_fsa_step(fsa,nst)

    def to_ndfsa(self):
        fsa = NDFSA()
        ## root does not have any action 
        for c in self.children:
            self.children[c].to_ndfsa_step(fsa,fsa.init)
        return fsa

    # probably a better way of doing this (by using superclass)
    def to_BFNDFSA(self):
        fsa = BlueFringeNDFSA()
        ## root does not have any action 
        for c in self.children:
            self.children[c].to_ndfsa_step(fsa,fsa.init)
        return fsa'''



def check_actions(fsa,neg):
    for n in neg:
        if fsa.is_valid(n):
            return False
    return True

## testing
if __name__ == "__main__":
    pta = PTA("")
    examples = [['a','b','c'],['a','c'],['b','c']]
    for e in examples:
        pta.addAction(e)
    #print pta
    #fsa = pta.to_ndfsa()
    fsa = pta.to_fsa()
    #fsa.merge_states('s4','s6')
    #fsa.merge_states('s5','s7')
    #fsa.merge_states('s1','s4')
    #for s1,s2 in fsa.all_state_pairs():
    #    print fsa.calculateScore(s1,s2)
    #print fsa.is_valid(["b","b"])
    #print check_actions(fsa,[["c","b"]])

    #fsa.merge_similar(threshold = 0,strictness=0,test = lambda fst: check_actions(fst,[["a","b","b"]]))
    #fsa.bluefringe(threshold = 0,strictness=0,test = lambda fst: check_actions(fst,[["a","b","b"]]))
    #fsa.merge_leafs()
    #print fsa.is_valid(["b","b"])
    #print fsa.trans
    #for a in examples:
    #    print fsa.is_valid(a)
    #print fsa.compute_avg_prob(['a','b','c'])
    #print fsa.compute_prob(['a','b','c']) 
    #print fsa.edit_distance(['a','a','b','d'])   
    #fsa.display_coloured()





