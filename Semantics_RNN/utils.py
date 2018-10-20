
# gets all the flows
def all_flows(path):
    print ("-- fetching all flows\n")
    all_flows = []
    for root, dirs, files in os.walk(path):
        for f in files:
            #print("File: " + os.path.join(root, f))
            if f[-9:] == "binetflow":
                print("Flow file found: " + root+f)
                all_flows = all_flows + [os.path.join(root, f)]
    return all_flows
    