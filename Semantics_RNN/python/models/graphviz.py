''' Files to generate graphviz
'''
import os
import pygraphviz as pgv
# requires: no actions aclled "__init"


def mc_generate_dot(self, filename='mc.dot'):
    A = pgv.AGraph(directed=True)
    A.add_node("__init")
    init = A.get_node("__init")
    init.attr['label'] = ' '
    init.attr['shape'] = 'point'
    for (f, t) in self.prob:
        print(f, t)
        if f == self.start:
            f = "__init"
        A.add_edge(f, t)
        edge = A.get_edge(f, t)
        if f == "__init":
            f = self.start
        prob = format(self.prob[(f, t)], '.5f')
        edge.attr['label'] = prob
    for n in self.endstates:
        node = A.get_node(n)
        node.attr['shape'] = 'doublecircle'
    A.write(filename)  # write to simple.dot

def mc_display(self, dotfile='mc.dot', pngfile='mc.png'):
    self.generate_dot()
    os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile)

def fsa_generate_dot(self, filename = 'fsa.dot'):
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

def fsa_display(self, dotfile = 'fsa.dot',pngfile = 'fsa.png'):
    self.generate_dot()
    os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile)

def ndfsa_generate_dot(self, filename = 'ndfsa.dot'):
        A = pgv.AGraph(strict = False,directed=True)
        A.add_node("__into__init")
        init = A.get_node("__into__init")
        init.attr['label'] = ' '
        init.attr['shape'] = 'point'
        A.add_edge("__into__init",self.init)
        steps = {}
        # just one edge between two states to simplify diagram
        for s1 in self.trans:
            for a in self.trans[s1]:
                for s2 in self.trans[s1][a]:
                    if self.trans_total[s1] > 0:
                        prob0 = float(self.trans_action[s1,a,s2]) / self.trans_total[s1]
                        prob = format(prob0, '.3f')
                        pstr = a + "/" + prob
                    else:
                        pstr = a + "/NP"
                    if (s1,s2) in steps:
                        steps[(s1,s2)] =  steps[(s1,s2)] + " , " + pstr
                    else:
                        steps[(s1,s2)] =  pstr
        for (s1,s2) in steps:
            A.add_edge(s1,s2)
            edge = A.get_edge(s1,s2)
            edge.attr['label'] = steps[(s1,s2)]
        A.write(filename) # write to simple.dot 

def ndfsa_display(self, dotfile = 'ndfsa.dot',pngfile = 'ndsa.png'):
        self.generate_dot()
        os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile) 

def ndfsa_generate_coloured_dot(self, filename = 'cndfsa.dot'):
        A = pgv.AGraph(strict = False,directed=True)
        A.add_node("__into__init")
        init = A.get_node("__into__init")
        init.attr['label'] = ' '
        init.attr['shape'] = 'point'
        A.add_edge("__into__init",self.init)
        steps = {}
        coloured = set()
        # just one edge between two states to simplify diagram
        for s1 in self.trans:
            for a in self.trans[s1]:
                for s2 in self.trans[s1][a]:
                    if self.trans_total[s1] > 0:
                        prob0 = float(self.trans_action[s1,a,s2]) / self.trans_total[s1]
                        prob = format(prob0, '.3f')
                        pstr = a + "/" + prob
                    else:
                        pstr = a + "/NP"
                    if (s1,s2) in steps:
                        steps[(s1,s2)] =  steps[(s1,s2)] + " , " + pstr
                    else:
                        steps[(s1,s2)] =  pstr
        for (s1,s2) in steps:
            A.add_edge(s1,s2)
            edge = A.get_edge(s1,s2)
            edge.attr['label'] = steps[(s1,s2)]
            # add colours:
            if not(s1 in coloured) and s1 in self.blue:
                ns1 = A.get_node(s1)
                ns1.attr['style'] = 'filled'
                ns1.attr['fillcolor'] = 'deepskyblue1'
                coloured.add(s1)
            if not(s1 in coloured) and s1 in self.red:
                ns1 = A.get_node(s1)
                ns1.attr['style'] = 'filled'
                ns1.attr['fillcolor'] = 'orangered'
                coloured.add(s1)    
            if not(s2 in coloured) and s2 in self.blue:
                ns2 = A.get_node(s2)
                ns2.attr['style'] = 'filled'
                ns2.attr['fillcolor'] = 'deepskyblue1'
                coloured.add(s2)
            if not(s2 in coloured) and s2 in self.red:
                ns2 = A.get_node(s2)
                ns2.attr['style'] = 'filled'
                ns2.attr['fillcolor'] = 'orangered'
                coloured.add(s2)                                      
        A.write(filename) # write to simple.dot

def ndfsa_display_coloured(self, dotfile = 'cndfsa.dot',pngfile = 'cndfsa.png'):
        self.generate_coloured_dot()
        os.system("dot -Tpng " + dotfile + " -o "+ pngfile + "; display " + pngfile)
