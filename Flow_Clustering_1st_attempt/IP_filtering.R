
setwd("~/Desktop/Project/Flow_Clustering_1st_attempt/")
N2=0
N=1000000

Flows <- read.table("netflow_day-02",sep=",",skip=N2,nrows=N,header=FALSE, stringsAsFactors = FALSE,fill=TRUE)
colnames(Flows) <- c("time","duration","src","dst",
                     "prot","srcport","dstport","srcpackets",
                     "dstpackets","srcbytes","dstbytes")
Comps <- sort(unique(Flows[,3]))[2:101]
Flow_Examples <- NULL
Flows[1:10,]
length(table(Flows[,3]))
N2=100*N
Flows <- read.table("netflow_day-02",sep=",",skip=N2,nrows=N,header=FALSE, stringsAsFactors = FALSE,fill=TRUE)



Comps=c("Comp364445","Comp000116", "Comp000219", "Comp000244", "Comp000253", "Comp000577", "Comp000595", "Comp000688",
       "Comp000944", "Comp001022", "Comp001050", "Comp001101", "Comp001706", "Comp001884", "Comp002286",
       "Comp002466", "Comp002475", "Comp002524", "Comp002760", "Comp002779", "Comp002915", "Comp002930",
       "Comp003192", "Comp003403", "Comp003448", "Comp003489", "Comp003602", "Comp003688", "Comp003795",
       "Comp004276", "Comp004336", "Comp004355", "Comp004479", "Comp004601", "Comp004603", "Comp004821",
       "Comp004852", "Comp004860", "Comp004880", "Comp004959", "Comp005115", "Comp005118", "Comp005295",
       "Comp005364", "Comp005591", "Comp005666", "Comp005809", "Comp005823", "Comp005825", "Comp005873",
       "Comp005926", "Comp005966", "Comp006069", "Comp006160", "Comp006224", "Comp006396", "Comp006410",
       "Comp006420", "Comp006560", "Comp006679", "Comp006850", "Comp007371", "Comp007377", "Comp007434",
       "Comp007589", "Comp007753", "Comp007792", "Comp008022", "Comp008056", "Comp008061", "Comp008279",
       "Comp008372", "Comp008398", "Comp008581", "Comp008608", "Comp008675", "Comp008789", "Comp008817",
       "Comp009032", "Comp009136", "Comp009312", "Comp009410", "Comp009583", "Comp009588", "Comp009700",
       "Comp009724", "Comp010016", "Comp010183", "Comp010250", "Comp010338", "Comp010413", "Comp010646",
       "Comp010804", "Comp010880", "Comp010933", "Comp011101", "Comp011108", "Comp011116", "Comp011251",
       "Comp011278", "Comp011341")

setwd("~/Desktop/Project/Flow_Clustering_1st_attempt/")
CompFlows1 <- read.table("Compflows1.txt",sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)
CompFlows2 <- read.table("Compflows2.txt",sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)
CompFlows3 <- read.table("Compflows3.txt",sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)
#CompFlows_test <- read.table("Compflows_test.txt",sep=",",header=FALSE, stringsAsFactors = FALSE,fill=TRUE)


colnames(CompFlows1) <- c("time","duration","src","dst",
                     "prot","srcport","dstport","srcpackets",
                     "dstpackets","srcbytes","dstbytes")
colnames(CompFlows2) <- c("time","duration","src","dst",
                         "prot","srcport","dstport","srcpackets",
                         "dstpackets","srcbytes","dstbytes")
colnames(CompFlows3) <- c("time","duration","src","dst",
                         "prot","srcport","dstport","srcpackets",
                         "dstpackets","srcbytes","dstbytes")


i=0
Comps=Comps[cc]

i=i+1
Comp1 <- rbind(CompFlows1[CompFlows1[,3]==Comps[i]|CompFlows1[,4]==Comps[i],],
               CompFlows2[CompFlows2[,3]==Comps[i]|CompFlows2[,4]==Comps[i],],
               CompFlows3[CompFlows3[,3]==Comps[i]|CompFlows3[,4]==Comps[i],])
length(unique(Comp1[,3]))
length(unique(Comp1[,4]))
dim(Comp1)
a=table(floor(Comp1[,1]/300))
plot(log(Comp1[,8]),log(Comp1[,9]),pch=16,cex=0.6)
plot(log(Comp1[,10]),log(Comp1[,11]),pch=16,cex=0.6)

plot(as.numeric(rownames(a))/12,as.numeric(a),type="l",xlim=c(30,50))
head(Comp1)

cc=c(5,35,44,48,65,66,72,84)


dim(Comp1)
plot(Comp1[,1]/3600,jitter(Comp1[,1]*0),pch=16,cex=0.7)
