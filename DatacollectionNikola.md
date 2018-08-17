
## 020 Nginx

was running capture-nginx.sh 5
error: capture-nginx.sh: 14: capture-nginx.sh: Syntax error: "}" unexpected

but data is generated with correct timestamps


## 021 Wget

was running ../capture.sh 5
error: ../capture.sh: 12: ../capture.sh: Syntax error: "}" unexpected

but data is generated with correct timestamps

## 030 scrappy

was running ../capture.sh 5
error: ../capture.sh: 12: ../capture.sh: Syntax error: "}" unexpected

but data is generated without timestamps (just one pcap file, not two for client and server)

## 040 apache

was running capture-apache.sh 5
same error

data generated with timestamps, but empty 

## 041 apache

was running ../capture.sh 5
same error

data generated with timestamps and with packets

## 050 vsftpd

running capture-vsftpd.sh 1, and also capture-vsftpd.sh 1
error: capture-vsftpd.sh: 15: capture-vsftpd.sh: Bad substitution

correct timestamp, empty data

