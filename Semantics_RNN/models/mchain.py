''' Simplified markovchain: 
     an action is a state, and only one state of action  meaning 
    we are loosing a lot of structure of the computation. '''

class MarkovChain:
    def __init__(self,start = ''):
        self.trans = {} 
        self.total = {}
        self.prob = {}
        self.endstates = set()
        self.start = start
        self._current = start

    def add_trans(self,F,T):
        '''
            adds a transition to the 
        '''
        if (F,T) in self.trans:
            self.trans[(F,T)] = self.trans[(F,T)] + 1
        else:
            self.trans[(F,T)] = 1
        if F in self.total:
            self.total[F] = self.total[F] + 1
        else:
            self.total[F] = 1
    
    def reset(self):
        '''
         resets to the inital position: used when adding actions one by one (e.g. from pandas)
        '''
        self._current = start
    
    def add_action(self,A):
        self.add_trans(self._current,A)
        self._current = A   
        
    def compute_prob(self):
        for (f,t) in self.trans:
                self.prob[(f,t)] = (float(self.trans[(f,t)]) / self.total[f])
    
    def prob_of(self,f,t):
        '''
            Computes probabilityL handles missing states in the training data (will get 0 probability)
        '''
        if (f,t) in self.prob:
            return self.prob[(f,t)]
        else:
            return 0.0

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
        '''
            returns the average probability for a sequence of actions
        '''
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

    def combine(self,mc):
        '''
         combines the MC with another MC
        '''
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

def dot_mc(mc,filename = "mc.dot"):
    str = "digraph{\n"
    for (f, t) in mc.prob:
        prob = format(mc.prob[(f, t)], '.5f')
        if f == mc.start:
            f = "init"
        str = str + "  " + f + "->" + t + "[label=\"" + prob + "\"]\n"
    str = str + "}"
    obj = open(filename, 'wb')
    obj.write(bytes(str, 'UTF-8'))
    obj.close
       

## testing
if __name__ == "__main__":
    ex = [['AS'],['ST','AMC','AMC','SD'],['ST','AMC','SD'],['AMC','AMC','ST','AMC']]
    mc = MarkovChain()
    mc.train(ex)
    v1 = mc.prob_of_action_seq(['AMC','SD'])
    v2 = mc.avg_prob_of_actions(['AMC','SD'])
    print (v1,v2)
    dot_mc(mc)
    #mc.display()

