# Simplified markovchainL
#  an action is a state, and only one state of action
#  meaning we are loosing a lot of structure of the computation.

#import pygraphviz as pgv
import os 

class MarkovChain:
    def __init__(self,start = ''):
        self.trans = {}
        self.total = {}
        self.prob = {}
        self.endstates = set()
        self.start = start
        self._current = start

    def add_trans(self,F,T):
        if (F,T) in self.trans:
            self.trans[(F,T)] = self.trans[(F,T)] + 1
        else:
            self.trans[(F,T)] = 1
        if F in self.total:
            self.total[F] = self.total[F] + 1
        else:
            self.total[F] = 1

    # for adding a single action at a time: resets to start        
    def reset(self):
        self._current = self.start
    
    def add_action(self,A):
        self.add_trans(self._current,A)
        self._current = A   
        
    def compute_prob(self):
        for (f,t) in self.trans:
                self.prob[(f,t)] = (float(self.trans[(f,t)]) / self.total[f])
    
    # handles missing states in the training data (will get 0 probability)
    def prob_of(self,f,t):
        if (f,t) in self.prob:
            return self.prob[(f,t)]
        else:
            return 0.0

    ## can we "normalise" based on lenght of chain?
    ## long chains will always 
    def prob_of_action_seq(self,chain):
        res = 1
        st = self.start
        for c in chain:
            res = res * self.prob_of(st,c)
            st = c
        if st in self.endstates:
            return (True,res)
        else:
            return (False,res)
    
    def avg_prob_of_actions(self,chain):
        steps = 1
        sum = 0
        st = self.start
        for c in chain:
            sum = sum + self.prob_of(st,c)
            steps = steps + 1
            st = c
        if st in self.endstates:
            return (True,sum / steps)
        else:
            return (False,sum / steps)    

    def train(self,examples):
        for ex in examples:
            curr = self.start
            for st in ex:
                self.add_trans(curr,st)
                curr = st
            self.endstates.add(curr)
        self.compute_prob()

    '''
    # requires: no actions aclled "__init"
    def generate_dot(self, filename = 'mc.dot'):
        A = pgv.AGraph(directed=True)
        A.add_node("__init")
        init = A.get_node("__init")
        init.attr['label'] = ' '
        init.attr['shape'] = 'point'
        for (f,t) in self.prob:
            print (f,t)
            if f == self.start:
                f = "__init"
            A.add_edge(f,t)
            edge = A.get_edge(f,t)
            if f == "__init":
                f = self.start
            prob = format(self.prob[(f,t)], '.5f')
            edge.attr['label'] = prob
        for n in self.endstates:
            node = A.get_node(n)
            node.attr['shape'] = 'doublecircle'
        #print(A.string()) # print to screen
        A.write(filename) # write to simple.dot
    '''
    #combines with 
    def combine(self,mc):
        for (f,t) in mc.trans:
            if (f,t) in self.trans:
                self.trans[(f,t)] = self.trans[(f,t)] + mc.trans[(f,t)]
            else:
                self.trans[(f,t)] = mc.trans[(f,t)]
        for f in mc.total:
            if f in self.total:
                self.total[f] = self.total[f] + mc.total[f]
            else:   
                self.total[f] = mc.total[f]
        self.compute_prob()
        self.endstates.union(mc.endstates)
'''
    def display(self, dotfile = 'mc.dot',pngfile = 'mc.png'):
        self.generate_dot()
        os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile)
'''
## testing
if __name__ == "__main__":
    ex = [['AS'],['ST','AMC','AMC','SD'],['ST','AMC','SD'],['AMC','AMC','ST','AMC']]
    mc = MarkovChain()
    mc.train(ex)
    v1 = mc.prob_of_action_seq(['AMC','SD'])
    v2 = mc.avg_prob_of_actions(['AMC','SD'])
    print (v1,v2)
   # mc.display()

