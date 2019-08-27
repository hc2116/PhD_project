from __future__ import print_function, division
from scapy.all import *
import sys

def pcap2flow2(pcap_file_name,dport):
    
    packets = PcapReader(pcap_file_name)
    for line in packets:
        if not(line.name=='Ethernet'):
            continue
        
        line=line[1]
        if (not(line.name=='IP') or not(line.proto==6)):
            continue
        if (line.src=='172.16.238.9') and (line.dst=='172.16.238.10') and (line.dport==dport):
            SourcePort=line.sport
            return SourcePort
    

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='convert txt file to flows')
    parser.add_argument('-f', '--pcap', default=None,
            help='specify the pcap file you want to process')
    parser.add_argument('-d', '--dport', default=7777,
            help='specify the chosen forwarded destination port')

    args = parser.parse_args()
    
    pcap_file_name=str(args.pcap)
    if args.dport:
        dport=int(args.dport)
    else:
        dport=7777
    SourcePort=pcap2flow2(args.pcap,dport)
    print(SourcePort)