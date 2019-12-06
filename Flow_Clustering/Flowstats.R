

Packets <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/Packets2",
                      sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)


Packets2 <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/Packets2",
                       sep="/",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)



Packets[(Packets[,3]=="192.51.127.16"&Packets[,4]=="131.243.140.243")|
          (Packets[,3]=="131.243.140.243"&Packets[,4]=="192.51.127.16"),c(3,4,7)]

Packets[(Packets[,3]=="192.51.127.16"&Packets[,4]=="131.243.140.243")|
          (Packets[,3]=="131.243.140.243"&Packets[,4]=="192.51.127.16"),]



Packets[(Packets[,3]=="131.243.142.113"&Packets[,4]=="218.105.151.125")|
          (Packets[,3]=="218.105.151.125"&Packets[,4]=="131.243.142.113"),c(3,4,7)]

Packets2[aaa,]

131.243.140.243
192.51.127.16





Packets <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/Packets2",
                      sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)

Packets[(Packets[,3]=="192.51.127.16"&Packets[,4]=="131.243.140.243"&
           grepl("54421",Packets[,7]))|
          (Packets[,3]=="131.243.140.243"&
             Packets[,4]=="192.51.127.16"&
             grepl("54421",Packets[,7])),c(3,4,7)]

Packets[(Packets[,3]=="131.243.142.148"&Packets[,4]=="140.32.89.146"&
           grepl("2998",Packets[,7]))|
          (Packets[,3]=="140.32.89.146"&
             Packets[,4]=="131.243.142.148"&
             grepl("2998",Packets[,7])),c(3,4,7)]

Packets[(Packets[,3]=="131.243.141.141"&Packets[,4]=="208.189.11.184"&
           grepl("1525",Packets[,7]))|
          (Packets[,3]=="208.189.11.184"&
             Packets[,4]=="131.243.141.141"&
             grepl("1525",Packets[,7])),c(3,4,7)]

Flows <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/Flows4.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)

Flows <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/FlowsUNSW1.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)

table(Flows[,3])


Packets[(Packets[,3]=="131.243.142.14"&Packets[,4]=="60.244.125.30")|
          (Packets[,3]=="60.244.125.30"&
             Packets[,4]=="131.243.142.14"),c(3,4,7)]

length(table(Flows$Ports))
dim(Flows)

table(Flows$Ports)[1:20]

Flows[which(grepl("TCP",Flows$Ports)),]

Flows
which.max(Flows$B_Ind)


Flows[1:30,]

Flows[1725:1727,]
Flows[833:835,]
Flows[1:10,]

which.min(Flows$NSPack+Flows$NDPack-Flows$B_Packets)


hist(Flows$Curr-Flows$Start)

hist(Flows$NIdle)

hist(Flows$X1B_Packets)
hist(Flows$X8B_Packets)

mean(Flows$B_Counter)
max(Flows$X1B_Packets)
max(Flows$DBytes)

##########################################################

clusterp <- c(5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)+1

Flows <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
FlowsCl <- Flows[,clusterp]
FlowsCl[1:4,]

logarithmic <- c(1,3,9,13,14,17,18)
FlowsCl[1:4,logarithmic]
FlowsCl[,logarithmic] <- log(FlowsCl[,logarithmic]+0.000000001)

plot(FlowsCl$SBytes,FlowsCl$SBytes_max)

plot(FlowsCl$NSPack,FlowsCl$NDPack)

a=jitter(rep(1,1000),amount=0.2)
b=jitter(c(rep(1,500),rep(2,500)),amount=0.7)
plot(a,b,pch=16)

##########################################################

Flows <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/FlowsCIC.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)

Flows <- Flows[-26,]
Flows[which(is.na(as.numeric(Flows$NSPack))),]

which(is.na(as.numeric(Flows$NSPack)))

table(Flows[,3])


##########################################################

Flows <- read.table("~/Desktop/Project/Flow_Clustering_2nd_attempt/FlowsUNSW1.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)

table(Flows[,3])
Flows[1:3,]

clusti <- c(6:13,15:18)

Flows[1:3,clusti]

Flows_cluster=Flows[]


Flows1c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient1.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows1s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver1.txt",
                    sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows2c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient2.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows2s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver2.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows3c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient3.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows3s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver3.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows4c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient4.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows4s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver4.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows5c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient5.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows5s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver5.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows6c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient6.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows6s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver6.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows7c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient7.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows7s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver7.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows8c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient8.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows8s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver8.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows9c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient9.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows9s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver9.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows10c <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowclient10.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)
Flows10s <- read.table("~/detlearsom/detgen/packetstats/Flowfiles/Flowserver10.txt",
                      sep=",",header=TRUE, stringsAsFactors = FALSE,fill=TRUE)





Flows1c[,6:42]

Flows1s[,6:42]


