import csv

def actions_csv(acts):
    res = ""
    for seq in acts:
        for a in seq:
            res = res + a + ","
        res = res[:-1] + "\n"
    return res

def write_csv(actions,tofile):
    s = actions_csv(actions)
    f = open(tofile, 'w')
    f.write(s)
    f.close()

def write_csv_from_file(fromfile,tofile):
    examples = parse(fromfile)
    create_basket(examples,tofile)

'''
seqs = parse_actions("ctu.basket")
mc = MarkovChain()
mc.train(seqs)
mc.display()
'''



'''
def parse_actions(filename,header = False):
    res,sess = [],[]
    with open(filename, 'r') as inputfile:
     rd = csv.reader(inputfile, delimiter=',')
     if header:
        next(rd,None)
     for row in rd:
        for a in row:
             sess = sess + [a]
        res = res + [sess]
        sess = []
    return res
'''