#from __future__ import print_function, division
from scapy.all import *



pcap_file_name = "/home/henry/Desktop/Project/Data/pcap_netflow_converter/tests/Mycaps_4_00001_20181019183313.pcap"
parsed_packets_name="test_packet_parser"
n_packets=5


def writeseq(open_flows,open_flows_packets,flows_written,
             ppf,n_packets,t,time_out=-100):
    remove_flows = []
    #for f_tuple, (st_time, last_time, fs, npack) in open_flows.items():
    for f_tuple, f_tuple_items in open_flows.items():
        st_time=f_tuple_items[0]
        last_time=f_tuple_items[1]
        fs=f_tuple_items[2]
        npack=f_tuple_items[3]
        
        if t - last_time > time_out: # time out
            fd = last_time - st_time
            # check if sequence is full
            packet_seq=open_flows_packets[f_tuple]
            seq_len=int(len(packet_seq)/5)
            if seq_len<n_packets:
                #print("test")
                #print(seq_len)
                for i in range(n_packets-seq_len):
                    packet_seq=packet_seq+("EOS",-1,-1,"EOS",-1)
            ##################
            write_string=str(st_time)+','+str(f_tuple[0])+','+f_tuple[1]+','+f_tuple[2]
            write_string+=','+str(fs)+ ','+str(fd)+','+str(npack)
            print(write_string)
            print("\n")
            write_string+=','.join(map(str,packet_seq))+'\n'
            
            print(packet_seq)
            print("\n")
            print("\n")
            
            ppf.write(write_string)
            flows_written+=1
            remove_flows.append(f_tuple)
    for f_tuple in remove_flows:
        del open_flows[f_tuple]
        del open_flows_packets[f_tuple]
    return open_flows, open_flows_packets, ppf, flows_written

def addPacket(five_tuple,open_flows,open_flows_packets,stored_rec,n_packets,
              t,length,flags,window,direct):
    st_time=stored_rec[0]
    last_time=stored_rec[1]
    fs=stored_rec[2]
    npack=stored_rec[3]
    #direct_old=stored_rec[4]
    
    open_flows[five_tuple] = (st_time, t, fs + length, npack+1, direct)
            
    if npack < n_packets:
        if direct==0: direct_print="Client"
        else: direct_print="Server"
        open_flows_packets[five_tuple] = open_flows_packets[five_tuple]+(direct_print,length,t-last_time,flags,window)
            
    return open_flows, open_flows_packets


def packetparser(pcap_file_name, parsed_packets_name, n_packets,n_skip,time_out):
    
    packets = PcapReader(pcap_file_name)
    ppf = open(parsed_packets_name, 'w')

    packet_storer_names=['Time','protocol', 'src_ip', 'src_port', 'dst_ip',
            'dst_port','size','length','npackets']
    packet_storer_names_append=['direction','size','T_inter','flags','window_size']

    for i in range(n_packets):
        packet_storer_names.extend([s + '_'+ str(i+1) for s in packet_storer_names_append])


    ppf.write(', '.join(packet_storer_names)+'\n')
    

    packets_total=0
    flows_written=0
    open_flows = dict()
    open_flows_packets = dict()
    ntimeouts=time_out
    
    t_prev=0
    order_tester=0
    max_order_diff=0
    
    for line in packets:
#        break    
#    line
        if not(line.name=='Ethernet'):
            continue
        t = line.time
        line=line[1]
        if not(line.name in ['IP','IPv6']): #
            continue
        if line.payload.name=='Raw': 
            continue
        if line.name!='IP':
            continue
        if line.proto!=6:
            continue
        
        ###############################################################
        if t<t_prev:
            order_tester+=1
            if t_prev-t>max_order_diff:
                max_order_diff=max(max_order_diff,t_prev-t)
                print('Packet number:'+str(packets_total))
                print('Difference:'+str(max_order_diff))
        t_prev=t
        ###############################################################        

        packets_total+=1
        if line.name=='IP':
            length = line.len
            if line.proto in [6,17]:
                five_tuple = tuple([line.proto, line.src + ',' + str(line.sport), line.dst + ',' + str(line.dport)])
                if line.proto==6:
                    flags=str(line['TCP'].flags)
                    window=line.window
            else:
                five_tuple = tuple([line.proto, line.src+', 0', line.dst+', 0'])
        else:
            if line.nh in [6,17]:                
                length = line.len
                five_tuple = tuple(['IPv6 '+str(line.nh), line.src + ',' + str(line.sport), line.dst + ',' + str(line.dport)])
            else:
                length = line.plen
                five_tuple = tuple(['IPv6 '+str(line.nh), line.src + ', 0', line.dst + ', 0'])
            
        ###############################################################        
        if t>ntimeouts:
            ntimeouts+=time_out
        
            open_flows, open_flows_packets, ppf, flows_written = writeseq(open_flows,
                                                                          open_flows_packets,
                                                                          flows_written,
                                                                          ppf,n_packets,t,
                                                                          time_out)
        ###############################################################                    

        stored_rec = open_flows.get(five_tuple, None) 
        if stored_rec is None:
            stored_rec2 = open_flows.get(tuple([five_tuple[0],five_tuple[2],five_tuple[1]]), None) 
        if stored_rec is not None: # if already exists
            
            open_flows, open_flows_packets = addPacket(five_tuple,open_flows,open_flows_packets,stored_rec,n_packets,
              t,length,flags,window,direct=0)
            
        elif stored_rec2 is not None:
#            if flags=='S':
#                #del open_flows[tuple([five_tuple[0],five_tuple[2],five_tuple[1]])]
#                open_flows[five_tuple] = (t, t, length, npack, 0)
#                open_flows_packets[five_tuple] = open_flows_packets[five_tuple]+("S",length,0,flags,window)
#            else:
            five_tuple2=tuple([five_tuple[0],five_tuple[2],five_tuple[1]])
            open_flows, open_flows_packets = addPacket(five_tuple2,open_flows,open_flows_packets,stored_rec2,n_packets,
              t,length,flags,window,direct=1)
        
        elif flags=='S':
                open_flows[five_tuple] = (t, t, length , 1, 0)
                
                #['direction','size','T_inter','flags','window_size']
                open_flows_packets[five_tuple] = ("Client",length,0,flags,window)
            
            
    ###############################################################        
    open_flows, open_flows_packets, ppf, flows_written = writeseq(open_flows,
                                                                  open_flows_packets,
                                                                  flows_written,
                                                                  ppf,n_packets,t,
                                                                  time_out=-100)
    ###############################################################                
    print("""
          Total Packets: [%i]
          Exported Flows: [%i]
          Open Flows: [%i]"""%(packets_total, flows_written, len(open_flows)))
    
    ppf.close()


pcap_file_name = "/home/henry/Desktop/Project/Data/pcap_netflow_converter/tests/dump-050-vsftpd-server-2019-01-29_17-37-25-sc1-5.pcap"
parsed_packets_name="test_packet_parser"
n_packets=5

packetparser(pcap_file_name, parsed_packets_name, n_packets=20,n_skip=0,time_out=60)


#import os
#def loop_folder(folder_name, time_out):
#    """is not quite sucessful right now"""
#    import glob
#    for pcap_file_name in glob.glob( os.path.join(folder_name, '*.pcap') ):
#        print("--> start to process pcap_file_nam: [%s]"%(pcap_file_name))
#        pcap2flow2(
#                pcap_file_name,
#                pcap_file_name.rsplit('.pcap')[0] + '.flow',
#                time_out
#                )
#
#
#if __name__ == "__main__":
#    import sys
#    import argparse
#
#    parser = argparse.ArgumentParser(description='convert txt file to flows')
#    parser.add_argument('-p', '--pcap', default=None,
#            help='specify the pcap file you want to process')
#    parser.add_argument('-f', '--folder', default=None,
#            help='specify the folder you want to loop through')
#
#    parser.add_argument('-t', '--time_out', default=10, type=float,
#            help='time out time')
#
#    args = parser.parse_args()
#    
#    if args.pcap:
#        pcap2flow2(args.pcap, args.pcap.rsplit('.pcap')[0] + '.flow', args.time_out)
#    elif args.folder:
#        loop_folder(args.folder, args.time_out)
#    else:
#        parser.print_help()