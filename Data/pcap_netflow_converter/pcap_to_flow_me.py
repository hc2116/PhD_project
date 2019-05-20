from __future__ import print_function, division
from scapy.all import *


#filename="Desktop/Project/Flow_Clustering_2nd_attempt/dump-011-ping2-2018-08-07-1732.pcap"
#pcap_file_name = "/home/henry/Desktop/Project/Data/pcap_netflow_converter/tests/dosattack.pcap"
#pcap_file_name = "/home/henry/Desktop/Project/Data/CIC/Monday-WorkingHours.pcap"

#pcap_file_name = "/home/henry/Desktop/Project/Data/pcap_netflow_converter/tests/Mycaps_3_00002_20181017180825.pcap"
#pcap_file_name = "/home/henry/Desktop/Project/Data/pcap_netflow_converter/tests/Mycaps_4_00001_20181019183313.pcap"
#packets = PcapReader(pcap_file_name)
#
#    j=0
#    packets = PcapReader(pcap_file_name)
#    j+=1
#    i=0
#    for line in packets:
#        i+=1
#        
#        if line.name=='Ethernet':
#            line=line[1]
#        elif not(line.name in ['IPv6','IP']):
#            continue
#        
#        if not(line.name in ['IP','IPv6']): #
#            continue
#        
#        if line.name=='IP':
#            if line.proto in [6,17]:
#                sport=line.sport
##        t = line.time
##        length = line.len
##        if line.name=='IPv6':
##            if line.nh not in [6,17]:
##                break
#    line
#        #if line.proto not in [6,17]:
#        #    break
#        
#        #if i==j:
#        #    break
#    line=line[1]
#    line


def pcap2flow2(pcap_file_name, flow_file_name, time_out):
    
    packets = PcapReader(pcap_file_name)
    fid = open(flow_file_name, 'w')

    name = ['start_time', 'protocol', 'src_ip', 'src_port', 'dst_ip',
            'dst_port','size','length','npackets']
    fid.write(', '.join(name)+'\n')
    
    i_total=0
    i_written=0
    open_flows = dict()
    ntimeouts=time_out
    
    t_prev=0
    order_tester=0
    max_order_diff=0
    
    for line in packets:
        
        if not(line.name=='Ethernet'):
            continue
        t = line.time
        
        line=line[1]
        
        if not(line.name in ['IP','IPv6']): #
            continue
        
        if line.payload.name=='Raw': 
            continue
        
        if t<t_prev:
            order_tester+=1
            if t_prev-t>max_order_diff:
                max_order_diff=max(max_order_diff,t_prev-t)
                print('Packet number:'+str(i_total))
                print('Difference:'+str(max_order_diff))
        t_prev=t
        flag=''
        i_total+=1
        if line.name=='IP':
            length = line.len
            if line.proto in [6,17]:
                five_tuple = tuple([line.proto, line.src + ',' + str(line.sport), line.dst + ',' + str(line.dport)])
                if line.proto==6:
                    flags=str(line['TCP'].flags)
            else:
                five_tuple = tuple([line.proto, line.src+', 0', line.dst+', 0'])
        else:
            if line.nh in [6,17]:                
                length = line.len
                five_tuple = tuple(['IPv6 '+str(line.nh), line.src + ',' + str(line.sport), line.dst + ',' + str(line.dport)])
            else:
                length = line.plen
                five_tuple = tuple(['IPv6 '+str(line.nh), line.src + ', 0', line.dst + ', 0'])
            
        
        
        if t>ntimeouts:
            ntimeouts+time_out
            remove_flows = []
            for f_tuple, (st_time, last_time, fs, npack) in open_flows.items():            
                if t - last_time > time_out: # time out
                    fd = last_time - st_time
                    fid.write(str(st_time)+','+str(f_tuple[0])+','+f_tuple[1]+','+f_tuple[2] +','+str(fs)+ ','+str(fd)+','+str(npack)+'\n')
                    i_written+=1
                    remove_flows.append(f_tuple)
            for f_tuple in remove_flows:
                del open_flows[f_tuple]

        stored_rec = open_flows.get(five_tuple, None) 
        if stored_rec is None:
            stored_rec2 = open_flows.get(tuple([five_tuple[0],five_tuple[2],five_tuple[1]]), None) 
        if stored_rec is not None: # if already exists
            (st_time_old, last_time_old, fs_old, npack) = stored_rec
            open_flows[five_tuple] = (st_time_old, t, fs_old + length, npack+1)
        elif stored_rec2 is not None:
            (st_time_old, last_time_old, fs_old, npack) = stored_rec2
            if flags=='S':
                del open_flows[tuple([five_tuple[0],five_tuple[2],five_tuple[1]])]
                open_flows[five_tuple] = (st_time_old, t, fs_old + length, npack+1)
            else:
                open_flows[tuple([five_tuple[0],five_tuple[2],five_tuple[1]])] = (st_time_old, t, fs_old + length, npack+1)
        else: # not exisit
            open_flows[five_tuple] = (t, t, length , 1)
            
            
    remove_flows = []
    for f_tuple, (st_time, last_time, fs, npack) in open_flows.items():            
        #if t - last_time > time_out: # time out
        fd = last_time - st_time
        fid.write(str(st_time)+','+str(f_tuple[0])+','+f_tuple[1]+','+f_tuple[2] +','+str(fs)+ ','+str(fd)+','+str(npack)+'\n')
        i_written+=1
        remove_flows.append(f_tuple)
    for f_tuple in remove_flows:
        del open_flows[f_tuple]
            
    print("""
          Total Packets: [%i]
          Exported Flows: [%i]
          Open Flows: [%i]"""%(i_total, i_written, len(open_flows)))
    
    fid.close()


import os
def loop_folder(folder_name, time_out):
    """is not quite sucessful right now"""
    import glob
    for pcap_file_name in glob.glob( os.path.join(folder_name, '*.pcap') ):
        print("--> start to process pcap_file_nam: [%s]"%(pcap_file_name))
        pcap2flow2(
                pcap_file_name,
                pcap_file_name.rsplit('.pcap')[0] + '.flow',
                time_out
                )


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='convert txt file to flows')
    parser.add_argument('-p', '--pcap', default=None,
            help='specify the pcap file you want to process')
    parser.add_argument('-f', '--folder', default=None,
            help='specify the folder you want to loop through')

    parser.add_argument('-t', '--time_out', default=10, type=float,
            help='time out time')

    args = parser.parse_args()
    
    if args.pcap:
        pcap2flow2(args.pcap, args.pcap.rsplit('.pcap')[0] + '.flow', args.time_out)
    elif args.folder:
        loop_folder(args.folder, args.time_out)
    else:
        parser.print_help()