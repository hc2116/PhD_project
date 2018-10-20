import Orange
from actions import write_csv

# has to be a .basket file
# Note: does not take order into account (i.e. just occurance of two events; ignores which came first)
def learn_rules(fname,support = 0.1, confidence = 0.7):
    data = Orange.data.Table(fname)
    rules = Orange.associate.AssociationRulesSparseInducer(data, support=support, confidence = confidence)
    return rules

# check single rule applicatio
def check_rule(rule,data):
    if rule.applies_left(data):
        if not(rule.applies_right(data)):
            return -1 # rule fail
        else:
            return 1 # rule succeeds
    else:
        return 0 # no match

# should we ignore confidence/support of original rule?
# ignores confidence/support and compute percentage of rules applying
# requires: data and rules are not empty
def check_rules(rules,data):
    total = 0
    ok = 0.0
    nomatch = 0.0
    fail = 0.0
    for d in data:
        for r in rules:
            check = check_rule(r,d)
            ## succeeds or don't match left
            if check != -1:
                ok = ok + 1
            ## fails to apply
            if check == -1:
                fail = fail + 1
            if check == 0:
                nomatch = nomatch + 1
            total = total + 1
    #if total == 0:
    #    return -1
    return {'failure' : fail / total, 'no_match' : nomatch / total, 'success' : ok / total , 'rules' : rules, 'total' : total}

def learn_rules_from_action_seq(learning_data, support = 0.1, confidence = 0.7):
    flearn = 'learn.basket' 
    write_csv(learning_data,flearn)
    return learn_rules(flearn,support,confidence)


def check_fit(learning_data,new_data, support = 0.1, confidence = 0.7):
    flearn = 'learn.basket' 
    write_csv(learning_data,flearn)
    rules = learn_rules(flearn,support,confidence)
    ftest = 'test.basket'
    write_csv(new_data,ftest)
    data = Orange.data.Table(ftest)
    return check_rules(rules,data)

# testing
if __name__ == "__main__":
    learn = [['AS'],['ST','AMC','AMC','SD'],['ST','AMC','SD'],['AMC','AMC','ST','AMC']]
    test = [['AS','AMC']]
    res = check_fit(learn,test)
    print (res)
    rules = res['rules']
    print (rules)

    #rules = learn_rules("actions.basket")
    #data = Orange.data.Table("actions.basket")
    # res1 = check_fit("actions.basket","actions.basket")
    # res2 = check_fit("actions.basket","action_moriarty.basket")
    # print res1
    # print res2