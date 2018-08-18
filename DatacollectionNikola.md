
## 020 Nginx

bash capture-nginx.sh 10
10 seconds

## 021 Wget

bash ../capture.sh 10
10 seconds
fix data names

## 030 scrappy

bash ../capture.sh 10
10 seconds
fix data generation

## 040 apache

bash ../capture.sh 10
was running capture-apache.sh 5

data generated with timestamps

## 041 apache

bash ../capture.sh 10
same error

data generated with timestamps, but empty
## 050 vsftpd

running capture-vsftpd.sh 1, and also capture-vsftpd.sh 1
error: capture-vsftpd.sh: 15: capture-vsftpd.sh: Bad substitution

correct timestamp, empty data



# To Do for Nikola

- Shell script to generated multiple pcaps
- Randomized file lengths (string lengths)
- fix data-names for nginx wget
- fix data generation for scrappy
- fix 040 and 041 data generation (empty)