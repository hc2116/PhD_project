


require(ggplot2)




Flows = read.table(file="Desktop/Project/Data/LANL/Comprehensive_Multi_source_Data_2015/TestflowsJan.txt",
                   sep=",",header=FALSE,
                   col.names=c('time','duration','scomputer','sport','dcomputer',
                                'dport','protocol','packet count','byte count'))
redteam=read.table(file="Desktop/Project/Data/LANL/Comprehensive_Multi_source_Data_2015/redteam.txt",
                      sep=",",header=FALSE,
                   col.names=c('time','User','SComp','DComp'))


################################################################
### C754 #######################################################
################################################################

Comp='C754'
Flows1=Flows[(Flows[,3]==Comp)|(Flows[,5]==Comp),]
red1=redteam[(redteam[,3]==Comp)|(redteam[,4]==Comp),]

Malintervals=matrix(c(8.4,8.43,8.78,8.81,9.6,9.63,13.53,13.56),ncol=2,byrow=TRUE)

hours=floor(Flows1[,1]/(3600*3))

freqs <- aggregate(hours,FUN=length,by=list(hours))

plot(freqs[,1]/8,freqs[,2],pch=16,xlim=c(0,22))
points(red1[,1]/(3600*24),red1[,1]*0,pch=16,col="red")

df1=data.frame(x=freqs[,1]/8,y=freqs[,2],group=1)

df1[(df1$x>8)&(df1$x<=10),3]=2
df1[(df1$x>10)&(df1$x<=13),3]=3
 
df1[(df1$x>13)&(df1$x<=100),3]=4

p1 <-  ggplot(df1,aes(x=x,y=y))+
  geom_ribbon(aes(x=x,ymax=max(y),ymin=y,fill=group),alpha=0.3)+
  guides(fill=FALSE)+
  labs(x="time",y="Events",title="Observations Imperial College Data")+
  geom_line()

  scale_fill_manual(values= c("white",c25)[1:length(Phases)])+
  guides(fill=FALSE)+
  geom_line()+
  #ylim(-100,max(Bin_freq))+
  theme_bw()+
  labs(x="time",y="Events",title="Observations Imperial College Data")+
  scale_x_continuous(breaks=c(14,14.25,14.5,14.75,
                              15,15.25,15.5,15.75,
                              16,16.25,16.5,16.75,17), 
                     labels=c("14:00","14:15","14:30","14:45",
                              "15:00","15:15","15:30","15:45",
                              "16:00","16:15","16:30","16:45","17:00"))+
  theme(legend.title = element_blank())


################################################################
### 'C2519' #######################################################
################################################################


Comp='C2519'
Flows1=Flows[(Flows[,3]==Comp)|(Flows[,5]==Comp),]
red1=redteam[(redteam[,3]==Comp)|(redteam[,4]==Comp),]

hours=floor(Flows1[,1]/(3600*3))

freqs <- aggregate(hours,FUN=length,by=list(hours))

plot(freqs[,1]/8,freqs[,2],pch=16,xlim=c(0,22))
points(red1[,1]/(3600*24),red1[,1]*0,pch=16,col="red")

################################################################
### 'C395' #######################################################
################################################################

Comp='C395'
Flows1=Flows[(Flows[,3]==Comp)|(Flows[,5]==Comp),]
red1=redteam[(redteam[,3]==Comp)|(redteam[,4]==Comp),]

hours=floor(Flows1[,1]/(3600*3))

freqs <- aggregate(hours,FUN=length,by=list(hours))

plot(freqs[,1]/8,freqs[,2],pch=16,xlim=c(0,14),ylim=c(0,6000))
points(red1[,1]/(3600*24),red1[,1]*0,pch=16,col="red")
 











# redteam 

redteam <- read.table("/home/henry/Desktop/Project/Data/LANL/Comprehensive_Multi_source_Data_2015/redteam.txt",
                      sep = ",")

redteam[redteam$V3=="C754"|redteam$V4=="C754",]


################################################################
### Plots evaluation ###########################################
################################################################

Outputs <- read.csv("/home/henry/Desktop/detlearsom/src/python/rnn_output_train.csv")

Outputs1 <- Outputs[Outputs$SrcAddr=="147.32.84.170",]

Outputs2 <- Outputs[Outputs$SrcAddr=="147.32.84.165",]

plot(Outputs1$session_id,Outputs1$mean,pch=16,cex=0.6)
plot(Outputs2$session_id,Outputs2$mean,pch=16,cex=0.6)

mean(Outputs2$mean)
mean(Outputs1$mean)

  # Cheating


x=rbeta(1000,shape1=1.3,shape2=1)

x=runif(1000)

y=x**2-1*x**3+0.02*rnorm(length(x),sd = (0.03+x))-0.234



xline=seq(0,1,0.0001)
line1=xline**2-1*xline**3+0.06*(0.03+xline)-0.234
line2=xline**2-1*xline**3-0.05*(0.03+xline)-0.234


plot(c(x+1.3),y,pch=16,col="navyblue",cex=0.7,xlab = "",ylab="",ylim=c(-0.27,-0.04))

lines(c(xline+1.3),line1,col="springgreen4")
lines(c(xline+1.3),line2,col="springgreen4")

points(1.39,0.115-0.23,col="maroon",pch=16,cex=1.3)
points(2,-0.24,col="maroon",pch=16,cex=1.3)

legend(1.3, -0.05, legend=c("Normal", "Outliers"),
       col=c("navyblue", "maroon"), pch=16, cex=1.3)

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################


Outputs <- read.csv("/home/henry/Desktop/detlearsom/src/python/rnn_output_train.csv")

Clean1 <- Outputs[Outputs$SrcAddr=="147.32.84.170",]
Clean2 <- Outputs[Outputs$SrcAddr=="147.32.84.164",]

Inf1 <- Outputs[Outputs$SrcAddr=="147.32.84.165",]


plot(Clean1$mean,pch=16,cex=0.7)

plot(Clean2$mean,pch=16,cex=0.7)

plot(Inf1$mean,pch=16,cex=0.7)

######################################################################
## Plots LANL ############################################
######################################################################







