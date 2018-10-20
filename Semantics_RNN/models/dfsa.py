'''
  Implementation of deterministic FSA. Not fully completed/tested as I switched to non-deterministic.
  This includes implementation of PTA as a Trie. This can then be converted to a FSA.
'''
import csv
from enum import Enum
from collections import defaultdict
import copy
import heapq
import time

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
        # keeps track of merged states
        self.top_merge = 0 # top-level merge (meaning not merged to remove non-determinism)
        self.determ_merge = 0 # merge to reduce non-determinsm
        # union-find datastructure to keep track of merged states
        self.merged = {}

    def new_state(self):
        self.counter = self.counter + 1
        state = "s" + str(self.counter)
        self.states.add(state)
        return state

    def add_trans(self,s1,act,s2):
        '''
         add transition. Will override existing (and generally not be well-behaved as it will 
         mess up probabilities). 
        '''
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
        return pairs

    def not_mergable_pair(self,s1,s2):
        return set([s1,s2]) in self.not_mergable

    def updated_mergable(self,into_state,from_state):
        for pairs in self.not_mergable:
            if from_state in pairs:
                self.not_mergable.remove(pairs)
                newset = (pairs - set(from_state)) ^ set(into_state)
                self.not_mergable.add(newset)

    def find_merged(self,node):
        '''
            Union-find datastractred to find node 
            TODO: should also update to flatten three
        '''
        while node in self.merged:
            node = self.merged[node]
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
        '''
            used to remove non-determinism as a result of merging. See merge for description of parameters
        '''
        # we don't need to care about keeping old state as this will be reset by caller (merge_states)
        while len(pairs) > 0:
            invalid = self.unreachable_states(pairs)
            if len(invalid) > 0:
                print ("Invalid: " + str(invalid))
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

    def merge_states(self,s1,s2, test = lambda x : True,threshold = 0,strictness = 0):
        '''
           Merges states s1 and s2: state s2 is removed and all in/out edges are sent to s2 with probs updated
             will also remove introduced non-determinism by merging states that have the same outgoing action (recursively)
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
        # FIXME: should not use iterator here as the it changes
        for s1,s2 in self.all_state_pairs():
            score = self.calculateScore(s1,s2,strictness = strictness)
            if score > high_score:
                high_score,hs1,hs2 = score,s1,s2
        if high_score >= threshold:
            self.merge_states(hs1,hs2,test = test)
            self.merge_similar(threshold,strictness)

class PTA:
    '''
        Prefix Tree Acceptor: to generate from logs and turn into initial automata.
    '''

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

   
    def add_action_iter(self,act):
        '''
          Iterative version: should be used for large examples where recursion causes problem (stackoverflow)
        '''
        curr = self
        while len(act) > 0:
            curr.counter = curr.counter + 1
            if not(act[0] in curr.children):
                curr.children[act[0]] = PTA(act[0])
            curr = curr.children[act[0]]
            act = act[1:]
        curr.accept = True

    def add_single(self,act):
        '''
         Adds a single transition (possible from deep down a PTA tree) and return the child node.
         This is used with dataframes on CTU example
        '''
        if not(act in self.children):
            self.children[act] = PTA(act)
        else:
            self.children[act].counter = self.children[act].counter + 1
        return self.children[act]

    def member(self,x):
        '''
            check if sequence if member: should only be used for calls
        '''
        if not(x[0] in self.children):
            return False
        return self.children[x[0]].member_dtree(x)
    
    
    def member_dtree(self,x):
        '''
            for internal use only (i.e. non-root).
        '''
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
        '''
            converts to FSA (deterministic -- see ndfsa file to generate non-deterministic)
        '''
        fsa = FSA()
        for c in self.children:
            self.children[c].to_fsa_step(fsa,fsa.init)
        return fsa

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
    fsa = pta.to_fsa()





