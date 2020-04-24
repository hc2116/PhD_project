#!/bin/bash

directory=$1
outputfile=$2

touch outputfile
for filename in /Data/*.pcap; do
	~/go/bin/flowtbag "$filename" > test.txt
	cat test.txt >> outputfile
	rm test.txt

done