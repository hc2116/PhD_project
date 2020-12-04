
require(ggplot2)

Dir <- c(1,2,2,1,2,1,1,2,1,1)
Direction <- c("C","S","S","C","S","C","C","S","C","C")
lens <- c(60,60,60,120,180,60,275,600,1200,681)^0.5
flag <- c("S","S"," ","P","R","P"," ","P"," ","P")
IAT <- abs(rnorm(10))*10+0.4


df3 <- data.frame(Flag=flag,
                  Direction=Direction,
                  xmax=cumsum(rep(3,10))+IAT,
                  xmin=cumsum(c(0,rep(3,9)))+IAT,
                  #xmax=cumsum(sqrt(lens))+IAT,
                  #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                  #ymin=Dir*6-0.5*sqrt(lens),
                  #ymax=Dir*6+0.5*sqrt(lens))
                  ymin=-0.5*lens,
                  ymax=+0.5*lens)

IAT=c(1606311470.615566,
       1606311470.616562,
       1606311470.616562,
       1606311470.616562,
       1606311470.6175613,
       1606311470.6175613,
       1606311470.6175613,
       1606311470.6185608,
       1606311470.6185608,
       1606311470.6185608,
       1606311470.6195602,
       1606311470.6195602,
       1606311470.6195602,
       1606311470.6205592,
       1606311470.6205592,
       1606311470.6205592,
       1606311470.6205592,
       1606311470.6215584,
       1606311470.6225579,
       1606311470.6235573)
#IAT=c(0,diff(IAT))
IAT=IAT-IAT[1]+cumsum(cumsum(rep(0.00002,10)))

lens=c(60,
         60,
         52,
         72,
         73,
         52,
         86,
         52,
         52,
         52,
         70,
         75,
         57,
         61,
         79,
         103,
         58,
         52,
         91,
         76)

Direction <- c('S',
                'D',
                'S',
                'D',
                'S',
                'D',
                'D',
                'S',
                'D',
                'S',
                'S',
                'D',
                'S',
                'D',
                'S',
                'D',
                'S',
                'D',
                'D',
                'D')

flag=c('S',
       'SA',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'A',
       'PA',
       'PA',
       'PA',
       'PA',
       'PA',
       'PA',
       'PA',
       'A',
       'PA',
       'PA')


df3 <- data.frame(Flag=flag,
                  Direction=Direction,
                  xmax=IAT,
                  xmin=IAT+0.0001,
                  #xmax=cumsum(sqrt(lens))+IAT,
                  #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                  #ymin=Dir*6-0.5*sqrt(lens),
                  #ymax=Dir*6+0.5*sqrt(lens))
                  ymin=-0.5*lens,
                  ymax=+0.5*lens)

plot_x <- ggplot(df3, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,fill=Flag))+
          geom_rect(colour="grey40", size=0.5)+
          facet_grid(Direction ~ .) + 
          theme_bw()+
          theme(axis.ticks.y = element_blank(),
                axis.text.y = element_blank())+
          labs(title="HTTP connection",
               y ="Direction", x = "Time [ms]")
          
plot_x
                
                              
                            
####################################################################################


df3 <- data.frame(type=c(1,6,4,6,1,4,1,4,1,1,1,1,6,6,1,1,3,1,4,1,4,6,4,6,4,4,6,4,6,4),
                  count=c(6,1,1,1,2,1,6,3,1,6,8,10,3,1,2,2,1,2,1,1,1,1,1,1,3,3,1,17,1,12) )

ggplot(df3,aes(x=1:nrow(df3),y=rep(1,30))) + geom_bar(stat="identity",aes(color=as.factor(type)))

df3 <- data.frame(type=c(1,6,4,6,1,4,1,4,1,1,1,1,6,6,1,
                         1,3,1,4,1,4,6,4,6,4,4,6,4,6,4),
                  count=c(6,1,1,1,2,1,6,3,1,6,8,10,3,1,2,
                          2,1,2,1,1,1,1,1,1,3,3,1,17,1,12))

library(ggplot2)

df3$type <- factor(df3$type)
df3$ymin <- 0
df3$ymax <- 1
df3$xmax <- cumsum(df3$count)
df3$xmin <- c(0, head(df3$xmax, n=-1))

plot_1 <- ggplot(df3, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, fill=type)) +
  geom_rect(colour="grey40", size=0.5)

#png("plot_1.png", height=200, width=800)
print(plot_1)
#dev.off()


dfx <- df3

dfx$type <- factor(dfx$type)
dfx$ymin <- c(0,1,2)
dfx$ymax <- c(1,2,3)
dfx$xmax <- cumsum(dfx$count)
dfx$xmin <- c(0, head(dfx$xmax, n=-1))

plot_x <- ggplot(dfx, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,fill=type))   +geom_rect(colour="grey40", size=0.5)

png("plot_x.png", height=200, width=800)
print(plot_x)
dev.off()


p1  <-  
  ggplot(dfx, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, fill = event))+
  theme_bw() + 
  geom_rect(colour = "black", size = 0.5) + 
  facet_grid(subject ~ .) + 
  theme(axis.ticks.y=element_blank(), axis.text.y=element_blank())

p1



########################################################
# Experiment 1
########################################################

require(ggplot2)
require(cowplot)

# geom_pointrange(mapping = aes(x = Metric, y = x),
#                 stat = "summary",
#                 fun.min = function(z) {quantile(z,0.25)},
#                 fun.max = function(z) {quantile(z,0.75)},
#                 fun = median)
# stat_summary(fun="mean", fun.min=function(z) { quantile(z,0.05) },fun.max=function(z) { quantile(z,0.95) },colour = "red", size = 1)

# A
N=100
x1 <- abs(rnorm(N,mean=0.002,sd=0.001))
x2 <- abs(rnorm(N,mean=0.002,sd=0.001))
x3 <- abs(rnorm(N,mean=0.002,sd=0.001))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))
dfA=df
df2A=df2
dfA$Set="A"
df2A$Set="A"
# B
x1 <- abs(rnorm(N,mean=0.003,sd=0.001))
x2 <- abs(rnorm(N,mean=0.003,sd=0.001))
x3 <- abs(rnorm(N,mean=0.002,sd=0.001))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))
dfB=df
df2B=df2
dfB$Set="B"
df2B$Set="B"
# C
x1 <- abs(rnorm(N,mean=0.004,sd=0.001))
x2 <- abs(rnorm(N,mean=0.004,sd=0.001))
x3 <- abs(rnorm(N,mean=0.003,sd=0.001))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))
dfC=df
df2C=df2
dfC$Set="C"
df2C$Set="C"
# D
x1 <- abs(rnorm(N,mean=0.0055,sd=0.001))
x2 <- abs(rnorm(N,mean=0.001,sd=0.001))
x3 <- abs(rnorm(N,mean=0.002,sd=0.001))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))
dfD=df
df2D=df2
dfD$Set="D"
df2D$Set="D"
# VM
x1 <- abs(rnorm(N,mean=0.026,sd=0.004))
x2 <- abs(rnorm(N,mean=0.035,sd=0.01))
x3 <- abs(rnorm(N,mean=0.022,sd=0.004))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))
dfVM=df
df2VM=df2
dfVM$Set="VM"
df2VM$Set="VM"

df=rbind(dfA,dfB,dfC,dfD,dfVM)
df2=rbind(df2A,df2B,df2C,df2D,df2VM)

df$x=df$x*100
df2[,1:3]=df2[,1:3]*100


pA <- ggplot(df, aes(x=Metric, y=x)) + 
  #geom_dotplot(binaxis='y', stackdir='center', aes(colour=Metric,fill=Metric),
  #             dotsize =0.3,binwidth=0.01,stackratio = .3)
  geom_point(aes(color=Metric),alpha=0.8)+
  facet_grid(. ~ Set)+
  geom_errorbar(df2,mapping=aes(y=y,x=Metric,ymin=ymin, ymax=ymax), 
                width=.2,size=1,)+
  theme_bw()+labs(y="% of max-dissimilarity",x="")+theme(legend.position = "none")+
  #geom_point(df2,mapping=aes(y=y,x=Metric,color=Metric),fill="white",shape = 21,size=4,show.legend=FALSE)
  geom_point(df2,mapping=aes(y=y,x=Metric),color="black",size=4,show.legend=FALSE)
pA#+scale_y_continuous(trans='log2')

plot_grid(pA, pA,pA,pA, labels = c('A', 'B', 'C','D'), ncol = 4)

####################################################################################################
require(ggplot2)
require(truncdist)
N=400
#DetGen
x1 <- c(rtrunc(n=0.7*N,spec="norm",a=0,b=1,mean=0.1,sd=0.1),
        rtrunc(n=0.3*N,spec="norm",a=0,b=1,mean=0.3,sd=0.3))
x2 <- c(rtrunc(n=0.9*N,spec="norm",a=0,b=1,mean=0.1,sd=0.05),
        rtrunc(n=0.1*N,spec="norm",a=0,b=1,mean=0.4,sd=0.3))
x3 <- c(rtrunc(n=0.7*N,spec="norm",a=0,b=1,mean=0.1,sd=0.1),
        rtrunc(n=0.3*N,spec="norm",a=0,b=1,mean=0.3,sd=0.3))
df1=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)),Data="DetGen")

#N=100
#CAIDA
x1 <- c(rtrunc(n=0.6*N,spec="norm",a=0,b=1,mean=0.1,sd=0.1),
        rtrunc(n=0.4*N,spec="norm",a=0,b=1,mean=0.4,sd=0.3))
x2 <- c(rtrunc(n=0.6*N,spec="norm",a=0,b=1,mean=0.1,sd=0.1),
        rtrunc(n=0.4*N,spec="norm",a=0,b=1,mean=0.4,sd=0.3))
x3 <- c(rtrunc(n=0.6*N,spec="norm",a=0,b=1,mean=0.1,sd=0.1),
        rtrunc(n=0.4*N,spec="norm",a=0,b=1,mean=0.4,sd=0.3))
df2=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)),Data="CAIDA")

#N=100
#CICIDS
x1 <- c(rtrunc(n=0.9*N,spec="norm",a=0,b=1,mean=0.04,sd=0.02),
        rtrunc(n=0.1*N,spec="norm",a=0,b=1,mean=0.2,sd=0.2))
x2 <- c(rtrunc(n=0.7*N,spec="norm",a=0,b=1,mean=0.1,sd=0.06),
        rtrunc(n=0.3*N,spec="norm",a=0,b=1,mean=0.2,sd=0.2))
x3 <- c(rtrunc(n=0.95*N,spec="norm",a=0,b=1,mean=0.03,sd=0.01),
        rtrunc(n=0.05*N,spec="norm",a=0,b=1,mean=0.2,sd=0.2))
df3=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)),Data="CICIDS")

df=rbind(df1,df2,df3)

pA <- ggplot(df, aes(x=x)) + 
  geom_histogram(aes(fill=Metric))+
  facet_grid(Metric ~ Data)+
  theme_bw()+labs(title="HTTP-connection similarity for each data source",
                  y="#connection pairs",x="% of max-dissimilarity")+theme(legend.position = "none")
pA+scale_y_continuous(trans='sqrt')

#plot_grid(pA, pA,pA,pA, labels = c('A', 'B', 'C','D'), ncol = 4)



####################################################################################################
require(ggplot2)
require(truncdist)
require(tmvtnorm)
N=100

xx=c(0,0.01,0.02,0.04,0.06,0.09,0.12,0.15,0.2)

Labels=c("SQL-Injection","SQL-I 2","SQL-I 2","SQL-I 4", 
         "Simple GET-request", "Multi-GET-request",
         "Post-request", "Keep-alive", 
         "Websockets","HTTP streaming",
         "Non-HTTP-traffic")

#"Simple GET-request"
Label=Labels[5]
x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.06)
y=rnorm(N,mean=0.9,sd=0.05)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.03))
y=c(y,rnorm(N,mean=0.9,sd=0.2))

df0=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL

for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d0=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.00)


#"Multi-GET-request",
Label=Labels[6]
#x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
#y=rnorm(N,mean=0.9,sd=0.3)
#x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.05))
#y=c(y,rnorm(N,mean=0.5,sd=0.3))
x=rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.3*N,mean=0.9,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.2,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
y=c(y,rnorm(0.3*N,mean=0.55,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.67,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.1,sd=0.2))

y=y-0.1
df1=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d1=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.002)


#Post
Label=Labels[7]
x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.02,sd=0.05)
y=rnorm(N,mean=1.2,sd=0.1)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.045))
y=c(y,rnorm(N,mean=0.9,sd=0.3))
df2=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d2=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.004)

# "Keep-alive
Label=Labels[8]
x=rtrunc(n=0.6*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.6*N,mean=0.7,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.55,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.45,sd=0.2))
df3=data.frame(x=x,y=y,Activity=Labels[8])
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d3=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.006)

# "HTTP-streaming
Label=Labels[10]
x=rtrunc(n=0.6*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.6*N,mean=0.8,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.55,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
#y=c(y,rnorm(0.3*N,mean=0.7,sd=0.15))
#x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.3,sd=0.2))
df5=data.frame(x=x,y=y,Activity=Labels[8])
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d5=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.006)

#SQL-I
Label=Labels[1]
#rtmvnorm(N,c(0.05,-1.6),sigma=matrix(c(0.02,0.015,0.015,0.035),nrow=2))
x=rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.05,sd=0.015)
y=rnorm(0.3*N,mean=-1.0,sd=0.25)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.03))
y=c(y,rnorm(N,mean=-0.9,sd=0.25))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.11,sd=0.025))
y=c(y,rnorm(0.3*N,mean=-0.5,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.07,sd=0.01))
y=c(y,rnorm(0.3*N,mean=-0.87,sd=0.15))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.13,sd=0.01))
y=c(y,rnorm(0.15*N,mean=-0.1,sd=0.15))
x=c(x,rtrunc(n=0.1*N,spec="norm",a=0,b=100,mean=0.15,sd=0.01))
y=c(y,rnorm(0.1*N,mean=0.03,sd=0.15))


df4=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
d4=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.008)


#df=data.frame(x=c(x0,x1,x2,x3,x4,x5),y=c(y0,y1,y2,y3,y4,y5),
#               Metric=c(rep("O",N),rep("A",N),rep("B",N),rep("C",2*N),rep("M",2*N),rep("M2",N)),Data="DetGen")


df=rbind(df0,df1,df2,df3,df4,df5)
d2=rbind(d0,d1,d2,d3,d4,d5)

pA <- ggplot(df, aes(x=x,y=y)) + 
  geom_point(aes(color=Activity),alpha=0.2,show.legend=FALSE)+
  geom_line(d2,mapping=aes(y=y,x=xx[-length(xx)]+0*Offset,color=Activity),size=1.3)+
  geom_hline(yintercept=-0.06,linetype="dashed",size=1.3,alpha=0.7)+
  #geom_errorbar(d2,mapping=aes(y=y,x=xx[-length(xx)]++Offset,ymin=ymin, ymax=ymax,color=Activity), 
  #              width=.002,size=1,)+
  #facet_grid(Metric ~ Data)+
  theme_bw()+
  labs(title="LSTM-model activity classification",
     y ="Classification score", x = "Simulated congestion RTT-delay [s]")
#+theme(legend.position = "none")
pA+scale_x_continuous(trans='sqrt',limits = c(0, 0.21))


dfnew=df
levels(dfnew$Activity)=c(levels(dfnew$Activity),"Benign")
dfnew[dfnew$Activity!="SQL-Injection",]$Activity="Benign"
pA <- ggplot(dfnew, aes(x=x*0,y=y)) + 
  geom_jitter(aes(color=Activity),alpha=0.8,show.legend=FALSE)+
#  geom_line(d2,mapping=aes(y=y,x=xx[-length(xx)]+0*Offset,color=Activity),size=1.3)+
  geom_hline(yintercept=-0.06,linetype="dashed",size=1.3,alpha=0.7)+
  #geom_errorbar(d2,mapping=aes(y=y,x=xx[-length(xx)]++Offset,ymin=ymin, ymax=ymax,color=Activity), 
  #              width=.002,size=1,)+
  #facet_grid(Metric ~ Data)+
  theme_bw()+
  labs(title="LSTM-model activity classification",
       y ="Classification score", x = "Simulated congestion RTT-delay [s]")
#+theme(legend.position = "none")
pA#+scale_x_continuous(trans='sqrt',limits = c(0, 0.21))


df_pre=df
df_pre$Model="Pre-correction"
df2_pre=d2
df2_pre$Model="Pre-correction"

#############################################
remove(xx)
remove(y)
remove(x)
remove(d0)
remove(d1)
remove(d2)
remove(d3)
remove(d4)
remove(d5)
remove(means)
remove(maxs)
remove(mins)


require(ggplot2)
require(truncdist)
require(tmvtnorm)
N=100

xx=c(0,0.01,0.02,0.04,0.06,0.09,0.12,0.15,0.2)

Labels=c("SQL-Injection","SQL-I 2","SQL-I 2","SQL-I 4", 
         "Simple GET-request", "Multi-GET-request",
         "Post-request", "Keep-alive", 
         "Websockets","HTTP streaming",
         "Non-HTTP-traffic")

#"Simple GET-request"
Label=Labels[5]
x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.06)
y=rnorm(N,mean=0.9,sd=0.05)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.03))
y=c(y,rnorm(N,mean=0.9,sd=0.2))

df0=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL

for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd0=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.00)


#"Multi-GET-request",
Label=Labels[6]
#x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
#y=rnorm(N,mean=0.9,sd=0.3)
#x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.05))
#y=c(y,rnorm(N,mean=0.5,sd=0.3))
x=rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.3*N,mean=0.9,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.4,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
y=c(y,rnorm(0.3*N,mean=0.55,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.67,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.4,sd=0.2))

y=y-0.1
df1=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd1=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.002)


#Post
Label=Labels[7]
x=rtrunc(n=N,spec="norm",a=0,b=100,mean=0.02,sd=0.05)
y=rnorm(N,mean=1.2,sd=0.1)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.07,sd=0.045))
y=c(y,rnorm(N,mean=0.9,sd=0.3))
df2=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd2=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.004)

# "Keep-alive
Label=Labels[8]
x=rtrunc(n=0.6*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.6*N,mean=0.7,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.55,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.45,sd=0.2))
df3=data.frame(x=x,y=y,Activity=Labels[8])
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd3=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.006)

# "HTTP-streaming
Label=Labels[10]
x=rtrunc(n=0.6*N,spec="norm",a=0,b=100,mean=0.01,sd=0.03)
y=rnorm(0.6*N,mean=0.8,sd=0.3)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.11,sd=0.03))
y=c(y,rnorm(N,mean=0.55,sd=0.2))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.10,sd=0.025))
#y=c(y,rnorm(0.3*N,mean=0.7,sd=0.15))
#x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.06,sd=0.01))
y=c(y,rnorm(0.3*N,mean=0.7,sd=0.25))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.14,sd=0.01))
y=c(y,rnorm(0.15*N,mean=0.3,sd=0.2))
df5=data.frame(x=x,y=y,Activity=Labels[8])
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd5=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.006)

#SQL-I
Label=Labels[1]
#rtmvnorm(N,c(0.05,-1.6),sigma=matrix(c(0.02,0.015,0.015,0.035),nrow=2))
x=rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.05,sd=0.015)
y=rnorm(0.3*N,mean=-1.0,sd=0.25)
x=c(x,rtrunc(n=N,spec="norm",a=0,b=100,mean=0.01,sd=0.03))
y=c(y,rnorm(N,mean=-0.9,sd=0.25))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.11,sd=0.025))
y=c(y,rnorm(0.3*N,mean=-0.8,sd=0.15))
x=c(x,rtrunc(n=0.3*N,spec="norm",a=0,b=100,mean=0.07,sd=0.01))
y=c(y,rnorm(0.3*N,mean=-0.87,sd=0.15))
x=c(x,rtrunc(n=0.15*N,spec="norm",a=0,b=100,mean=0.13,sd=0.01))
y=c(y,rnorm(0.15*N,mean=-0.7,sd=0.15))
x=c(x,rtrunc(n=0.1*N,spec="norm",a=0,b=100,mean=0.15,sd=0.01))
y=c(y,rnorm(0.1*N,mean=-0.75,sd=0.15))


df4=data.frame(x=x,y=y,Activity=Label)
means=NULL
maxs=NULL
mins=NULL
for(i in 1:(length(xx)-1)){
  means=c(means,mean(y[(x>xx[i]&x<xx[i+1])]))
  maxs=c(maxs,max(y[(x>xx[i]&x<xx[i+1])]))
  mins=c(mins,min(y[(x>xx[i]&x<xx[i+1])]))
}
dd4=data.frame(y=means,ymax=maxs,ymin=mins,Activity=Label,Offset=0.008)


#df=data.frame(x=c(x0,x1,x2,x3,x4,x5),y=c(y0,y1,y2,y3,y4,y5),
#               Metric=c(rep("O",N),rep("A",N),rep("B",N),rep("C",2*N),rep("M",2*N),rep("M2",N)),Data="DetGen")


df=rbind(df0,df1,df2,df3,df4,df5)
dd2=rbind(dd0,dd1,dd2,dd3,dd4,dd5)


df_post=df
df_post$Model="Post-correction"
df2_post=dd2
df2_post$Model="Post-correction"


df_model=rbind(df_pre,df_post)
df2_model=rbind(df2_pre,df2_post)

df_model$Models=factor(df_model$Model, levels=c("Pre-correction","Post-correction"))
df2_model$Models=factor(df2_model$Model, levels=c("Pre-correction","Post-correction"))

pA <- ggplot(df, aes(x=x,y=y)) + 
  geom_point(aes(color=Activity),alpha=0.2,show.legend=FALSE)+
  geom_line(d2,mapping=aes(y=y,x=xx[-length(xx)]+0*Offset,color=Activity),size=1.3)+
  geom_hline(yintercept=-0.4,linetype="dashed",size=1.3,alpha=0.7)+
  #geom_errorbar(d2,mapping=aes(y=y,x=xx[-length(xx)]++Offset,ymin=ymin, ymax=ymax,color=Activity), 
  #              width=.002,size=1,)+
  #facet_grid(Metric ~ Data)+
  theme_bw()+
  labs(title="LSTM-model activity classification",
       y ="Classification score", x = "Simulated congestion RTT-delay [s]")
#+theme(legend.position = "none")
pA+scale_x_continuous(trans='sqrt',limits = c(0, 0.21))


pA <- ggplot(df_model, aes(x=x,y=y)) + 
  geom_point(aes(color=Activity),alpha=0.2,show.legend=FALSE)+
  geom_line(df2_model,mapping=aes(y=y,x=xx[-length(xx)]+0*Offset,color=Activity),size=1.3)+
  geom_hline(yintercept=-0.3,linetype="dashed",size=1.3,alpha=0.7)+
  #geom_errorbar(d2,mapping=aes(y=y,x=xx[-length(xx)]++Offset,ymin=ymin, ymax=ymax,color=Activity), 
  #              width=.002,size=1,)+
  facet_grid(. ~ Models)+
  theme_bw()+
  labs(title="LSTM-model activity classification",
       y ="Classification score", x = "Simulated congestion RTT-delay [s]")
#+theme(legend.position = "none")
pA+scale_x_continuous(trans='sqrt',limits = c(0, 0.21))+
  scale_y_continuous(limits = c(-1.5, 1.5))

#######################################################################################################
#######################################################################################################

require(MASS)
require(ggplot2)

N=100

x1=mvrnorm(N,mu=c(0,0),Sigma=diag(c(0.4,0.4)))
x1=rbind(x1, mvrnorm(N,mu=c(1,-1),Sigma=diag(c(0.2,0.2))))
x1=rbind(x1, mvrnorm(0.5*N,mu=c(0.4,-0.4),Sigma=diag(c(0.03,0.03))))
x1=rbind(x1, mvrnorm(0.5*N,mu=c(2,0.5),Sigma=diag(c(0.03,0.03))))
x1=rbind(x1, mvrnorm(0.5*N,mu=c(0.5,0.8),Sigma=diag(c(0.02,0.03))))
x1=rbind(x1, mvrnorm(0.2*N,mu=c(1.5,0.3),Sigma=matrix(c(0.2,0.1,0.1,0.2),nrow=2)))
x2=mvrnorm(N,mu=c(2,0.3),Sigma=diag(c(0.4,0.2)))
x3=mvrnorm(N,mu=c(-1.5,0.7),Sigma=diag(c(0.1,0.2)))
x4=mvrnorm(2*N,mu=c(-0.6,-1.3),Sigma=diag(c(6,0.3)))


df1=data.frame(x=c(x1[,1],x2[,1],x3[,1],x4[,1]),y=c(x1[,2],x2[,2],x3[,2],x4[,2]),
              Label="Benign")
df1$x=df1$x/sd(df1$x)
df1$y=df1$y/sd(df1$y)


N=20
x1=mvrnorm(N,mu=c(-2.8,3),Sigma=diag(c(0.1,0.1)))
x1=rbind(x1, mvrnorm(N,mu=c(-5,-5),Sigma=diag(c(1,1))))
x1=rbind(x1, mvrnorm(N,mu=c(5,4.5),Sigma=diag(c(1,1))))
x1=rbind(x1, mvrnorm(N,mu=c(0,4.5),Sigma=diag(c(1,1))))
#x1=rbind(x1, mvrnorm(N,mu=c(0,-5),Sigma=diag(c(1,1))))
x1=rbind(x1, mvrnorm(N,mu=c(-5,0),Sigma=diag(c(1,1))))

#x1=rbind(x1, mvrnorm(0.5*N,mu=c(0.4,-0.4),Sigma=diag(c(0.03,0.03))))

df2=data.frame(x=c(x1[,1]),y=c(x1[,2]),
               Label="Attack")
#df=rbind(df1,df2)


N=40
x1=mvrnorm(N,mu=c(-0.6,-1.3),Sigma=diag(c(6,0.3)))
df3=data.frame(x=c(x1[,1]),y=c(x1[,2]),
               Label="HTTP - sudden termination")



pA <- ggplot(df1,aes(x=x,y=y,color=Label))+
  geom_point(alpha=0.4,size=1)+
  stat_ellipse(aes(x=x, y=y),level=0.9999)+#,type = "polygon", level=6)+
  geom_point(df2,mapping=aes(x=x,y=y,color=Label),alpha=0.4,size=1)+
  geom_point(df3,mapping=aes(x=x,y=y,color=Label),size=2)+
  theme_bw()+labs(y="dimension x5",x="dimension x3",title="Subspace projection of connections")+
  xlim(-5,4.5)+ylim(-4.5,4)
pA




####################################################################################
# Paket sequence plots
# Plot Detgen
####################################################################################
IAT=c(1606320490.3553698,
      1606320490.3573225,
      1606320490.3573225,
      1606320490.359275,
      1606320490.359275,
      1606320490.3612275,
      1606320490.3612275,
      1606320490.3622036,
      1606320490.3622036,
      1606320490.3631797,
      1606320490.3631797,
      1606320490.3631797,
      1606320490.364156,
      1606320490.364156,
      1606320490.3651323,
      1606320490.3651323,
      1606320490.367085,
      1606320490.367085,
      1606320490.3680615,
      1606320490.3690379,
      1606320490.3700142,
      1606320490.3709903,
      1606320490.3719661,
      1606320490.3719661,
      1606320490.372943,
      1606320490.373919,
      1606320490.373919,
      1606320490.373919,
      1606320490.3748953,
      1606320490.3748953,
      1606320490.3758714,
      1606320490.3758714,
      1606320490.3768482,
      1606320490.3768482,
      1606320490.3788006,
      1606320490.3788006,
      1606320490.3797772,
      1606320490.3807535,
      1606320490.3817296,
      1606320490.382706,
      1606320490.383682,
      1606320490.383682,
      1606320490.384658,
      1606320490.385635,
      1606320490.385635,
      1606320490.386611,
      1606320490.386611,
      1606320490.386611,
      1606320490.387587,
      1606320490.387587,
      1606320490.387587,
      1606320490.3885634,
      1606320490.38954,
      1606320490.390516)
#IAT=c(0,diff(IAT))
IAT[1:18]=IAT[1:18]-IAT[1]+cumsum(cumsum(rep(0.00002,18)))
IAT[19:36]=IAT[19:36]-IAT[19]+cumsum(cumsum(rep(0.00002,18)))
IAT[37:54]=IAT[37:54]-IAT[37]+cumsum(cumsum(rep(0.00002,18)))
#IAT=IAT-IAT[1]+rep(cumsum(cumsum(rep(0.00002,18))),3)

lens=c(60,
       60,
       52,
       93,
       52,
       77,
       52,
       1084,
       1028,
       52,
       52,
       100,
       52,
       676,
       52,
       52,
       52,
       52,
       60,
       60,
       52,
       93,
       52,
       77,
       52,
       1084,
       1028,
       52,
       52,
       100,
       52,
       676,
       52,
       52,
       52,
       52,
       60,
       60,
       52,
       93,
       52,
       77,
       52,
       1084,
       1028,
       52,
       52,
       100,
       52,
       676,
       52,
       52,
       52,
       52)

Direction <- c('Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Forward')

flag=c('S',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'FA',
       'FA',
       'A',
       'S',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'FA',
       'FA',
       'A',
       'S',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'FA',
       'FA',
       'A')


df3 <- data.frame(Flag=flag[1:18],
                  Direction=Direction[1:18],
                  xmax=IAT[1:18],
                  xmin=IAT[1:18]+0.00018,
                  #xmax=cumsum(sqrt(lens))+IAT,
                  #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                  #ymin=Dir*6-0.5*sqrt(lens),
                  #ymax=Dir*6+0.5*sqrt(lens))
                  ymin=-0.4*sqrt(lens[1:18]),
                  ymax=+0.4*sqrt(lens[1:18]))

df32 <- data.frame(Flag=flag[19:36],
                   Direction=Direction[19:36],
                   xmax=IAT[19:36],
                   xmin=IAT[19:36]+0.00018,
                   #xmax=cumsum(sqrt(lens))+IAT,
                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                   #ymin=Dir*6-0.5*sqrt(lens),
                   #ymax=Dir*6+0.5*sqrt(lens))
                   ymin=-0.4*sqrt(lens[19:36])-30,
                   ymax=+0.4*sqrt(lens[19:36])-30)

df33 <- data.frame(Flag=flag[37:54],
                   Direction=Direction[37:54],
                   xmax=IAT[37:54],
                   xmin=IAT[37:54]+0.00018,
                   #xmax=cumsum(sqrt(lens))+IAT,
                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                   #ymin=Dir*6-0.5*sqrt(lens),
                   #ymax=Dir*6+0.5*sqrt(lens))
                   ymin=-0.4*sqrt(lens[37:54])-60,
                   ymax=+0.4*sqrt(lens[37:54])-60)


df3=rbind(df3,df32,df33)

# df3 <- data.frame(Flag=flag,
#                   Direction=Direction,
#                   xmax=IAT,
#                   xmin=IAT+0.0001,
#                   #xmax=cumsum(sqrt(lens))+IAT,
#                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
#                   #ymin=Dir*6-0.5*sqrt(lens),
#                   #ymax=Dir*6+0.5*sqrt(lens))
#                   ymin=-0.5*sqrt(lens),
#                   ymax=+0.5*sqrt(lens))


plot_x <- ggplot(df3, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,fill=Flag))+
  geom_hline(yintercept=-15,linetype="dashed",size=1.3,alpha=0.5)+
  geom_hline(yintercept=-45,linetype="dashed",size=1.3,alpha=0.5)+
  geom_rect(colour="grey40", size=0.5)+
  facet_grid(Direction ~ .) + 
  theme_bw()+
  annotate("text", x = -0.0013, y = 0, label = "Sample 1")+
  annotate("text", x = -0.0013, y = -30, label = "Sample 2")+
  annotate("text", x = -0.0013, y = -60, label = "Sample 3")+
  theme(axis.ticks.y = element_blank(),
        axis.text.y = element_blank())+
  scale_x_continuous(limits = c(-0.0018, 0.0155))+
  labs(title="DetGen - HTTP connection comparison",
       y ="", x = "Time [ms]")

#plot_x
plot_detgen= plot_x + theme(legend.position = "none")

#######################################################
#Plot Regu
#######################################################
IAT=c(1606911764.0231504,
      1606911764.0790403,
      1606911764.0790403,
      1606911764.0800164,
      1606911764.0809927,
      1606911764.0819693,
      1606911764.0819693,
      1606911764.0829453,
      1606911764.083922,
      1606911764.0849006,
      1606911764.0849006,
      1606911764.0858738,
      1606911764.0868497,
      1606911764.0868497,
      1606911764.0878234,
      1606911764.0888007,
      1606911764.0897791,
      1606911764.0907557,
      1606911764.091732,
      1606911764.091732,
      1606911764.0927076,
      1606911764.0936842,
      1606911764.0946605,
      1606911764.0946605,
      1606911764.0956368,
      1606911764.0966132,
      1606911764.0985663,
      1606911764.0995462,
      1606911764.1034482,
      1606911764.1054,
      1606911764.1054,
      1606911764.1063757,
      1606911764.108324,
      1606911764.109302,
      1606911764.1102812,
      1606911764.1112576,
      1606911764.1122339,
      1606911764.11321,
      1606911764.11321,
      1606911764.1141863,
      1606911764.119064,
      1606911764.119064,
      1606911764.119064,
      1606911764.1200402,
      1606911764.1200402,
      1606911764.1200402,
      1606911764.1210165,
      1606911764.1210165,
      1606911764.1210165,
      1606911764.1219933,
      1606911764.1219933,
      1606911764.1219933,
      1606911764.1229692,
      1606911764.1229692,
      1606911764.1229692,
      1606911764.1239452,
      1606911764.1239452,
      1606911764.1239452,
      1606911764.1249216,
      1606911764.1249216,
      1606911764.1249216,
      1606911764.1258965,
      1606911764.1258965,
      1606911764.1258965,
      1606911764.1268742,
      1606911764.1268742,
      1606911764.1278503,
      1606911764.1288266,
      1606911764.1317556,
      1606911764.1317556,
      1606911764.1317556,
      1606911764.132732,
      1606911764.132732,
      1606911764.133708,
      1606911764.133708,
      1606911764.133708,
      1606911764.1346843,
      1606911764.1346843,
      1606911764.1346843,
      1606911764.1356642)

IAT[1:40]=IAT[1:40]-IAT[1]+cumsum(cumsum(rep(0.00002,40)))#+cumsum(cumsum(abs(rnorm(18,mean=0,sd=0.00001))))
IAT[41:80]=IAT[41:80]-IAT[41]+cumsum(cumsum(rep(0.00002,40)))#+cumsum(cumsum(abs(rnorm(18,mean=0,sd=0.00008))))

lens=c(60,
       60,
       60,
       52,
       60,
       52,
       72,
       52,
       68,
       52,
       52,
       86,
       52,
       71,
       52,
       52,
       75,
       52,
       57,
       52,
       61,
       52,
       80,
       103,
       52,
       58,
       52,
       91,
       52,
       76,
       52,
       60,
       52,
       83,
       52,
       80,
       52,
       103,
       52,
       88,
       60,
       60,
       60,
       60,
       52,
       72,
       52,
       68,
       52,
       86,
       52,
       52,
       71,
       52,
       52,
       52,
       75,
       57,
       52,
       61,
       52,
       52,
       80,
       52,
       103,
       58,
       52,
       91,
       76,
       52,
       52,
       60,
       52,
       83,
       52,
       80,
       52,
       103,
       52,
       88)

Direction <- c('Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Forward')

flag=c('S',
       'S',
       'SA',
       'A',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'S',
       'SA',
       'S',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'A',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA')


df3 <- data.frame(Flag=flag[1:40],
                  Direction=Direction[1:40],
                  xmax=IAT[1:40],
                  xmin=IAT[1:40]+0.0003,
                  #xmax=cumsum(sqrt(lens))+IAT,
                  #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                  #ymin=Dir*6-0.5*sqrt(lens),
                  #ymax=Dir*6+0.5*sqrt(lens))
                  ymin=-0.4*sqrt(lens[1:40]),
                  ymax=+0.4*sqrt(lens[1:40]))

df32 <- data.frame(Flag=flag[41:80],
                   Direction=Direction[41:80],
                   xmax=IAT[41:80],
                   xmin=IAT[41:80]+0.0003,
                   #xmax=cumsum(sqrt(lens))+IAT,
                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                   #ymin=Dir*6-0.5*sqrt(lens),
                   #ymax=Dir*6+0.5*sqrt(lens))
                   ymin=-0.4*sqrt(lens[41:80])-30,
                   ymax=+0.4*sqrt(lens[41:80])-30)

df3=rbind(df3,df32)

# df3 <- data.frame(Flag=flag,
#                   Direction=Direction,
#                   xmax=IAT,
#                   xmin=IAT+0.0001,
#                   #xmax=cumsum(sqrt(lens))+IAT,
#                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
#                   #ymin=Dir*6-0.5*sqrt(lens),
#                   #ymax=Dir*6+0.5*sqrt(lens))
#                   ymin=-0.5*sqrt(lens),
#                   ymax=+0.5*sqrt(lens))


plot_x <- ggplot(df3, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,fill=Flag))+
  geom_hline(yintercept=-15,linetype="dashed",size=1.3,alpha=0.5)+
#  geom_hline(yintercept=-45,linetype="dashed",size=1.3,alpha=0.5)+
  geom_rect(colour="grey40", size=0.5)+
  facet_grid(Direction ~ .) + 
  theme_bw()+
  annotate("text", x = -0.002, y = 0, label = "Sample 1")+
  annotate("text", x = -0.002, y = -30, label = "Sample 2")+
#  annotate("text", x = -0.002, y = -60, label = "Sample 3")+
  theme(axis.ticks.y = element_blank(),
        axis.text.y = element_blank())+
  scale_x_continuous(limits = c(-0.0025, 0.0261))+
  labs(title="Regular HTTP connection comparison",
       y ="", x = "Time [s]")

#plot_x
plot_regu=plot_x+ theme(legend.position = "bottom")

require(cowplot)

plot_grid(plot_detgen, plot_regu,nrow = 2,rel_heights  = c(1, 1.25))

################################################################################################################
## Plot 

IAT=c(1606918265.081262,
      1606918265.081262,
      1606918265.082239,
      1606918265.082239,
      1606918265.082239,
      1606918265.0832138,
      1606918265.0832138,
      1606918265.0832138,
      1606918265.0841904,
      1606918265.0841904,
      1606918265.0851674,
      1606918265.0851674,
      1606918265.0851674,
      1606918265.087119,
      1606918265.087119,
      1606918265.087119,
      1606918265.088096,
      1606918265.088096,
      1606918265.088096,
      1606918265.0890725,
      1606918265.0890725,
      1606918265.0900493,
      1606918265.0900493,
      1606918265.0900493,
      1606918265.0910258,
      1606918265.0910258,
      1606918265.0920007,
      1606918265.0920007,
      1606918265.092978,
      1606918265.092978,
      1606918265.092978,
      1606918265.0939543,
      1606918265.0939543,
      1606918265.0939543,
      1606918265.0949311,
      1606918265.0949311,
      1606918265.0959058,
      1606918265.0959058,
      1606918265.0959058,
      1606918265.0968819,
      1606918265.115432,
      1606918265.116409,
      1606918265.116409,
      1606918265.1173854,
      1606918265.1173854,
      1606918265.1173854,
      1606918265.1183622,
      1606918265.1183622,
      1606918265.1193364,
      1606918265.1193364,
      1606918265.1193364,
      1606918265.1203141,
      1606918265.1203141,
      1606918265.1203141,
      1606918265.1212907,
      1606918265.1212907,
      1606918265.1212907,
      1606918265.1222675,
      1606918265.1222675,
      1606918265.1222675,
      1606918265.1232421,
      1606918265.1232421,
      1606918265.124219,
      1606918265.124219,
      1606918265.1251957,
      1606918265.1251957,
      1606918265.1261709,
      1606918265.1261709,
      1606918265.1271465,
      1606918265.1271465,
      1606918265.1281223,
      1606918265.1281223,
      1606918265.1281223,
      1606918265.1290987,
      1606918265.1290987,
      1606918265.130076,
      1606918265.130076,
      1606918265.130076,
      1606918265.1310525,
      1606918265.1310525)

IAT[1:40]=IAT[1:40]-IAT[1]+cumsum(cumsum(rep(0.00002,40)))#+cumsum(cumsum(abs(rnorm(18,mean=0,sd=0.00001))))
IAT[41:80]=IAT[41:80]-IAT[41]+cumsum(cumsum(rep(0.00002,40)))#+cumsum(cumsum(abs(rnorm(18,mean=0,sd=0.00008))))

lens=c(60,
       60,
       52,
       2948,
       64,
       2948,
       64,
       2948,
       52,
       2948,
       52,
       2948,
       52,
       52,
       1500,
       52,
       2948,
       64,
       2948,
       72,
       2948,
       80,
       2948,
       64,
       2948,
       64,
       2948,
       64,
       2948,
       64,
       2948,
       52,
       1500,
       52,
       2948,
       64,
       2948,
       72,
       2948,
       80,
       60,
       60,
       52,
       2948,
       2948,
       2948,
       2948,
       2948,
       64,
       2948,
       1500,
       52,
       2948,
       52,
       52,
       64,
       52,
       2948,
       2948,
       2948,
       2948,
       2948,
       2948,
       1500,
       64,
       2948,
       2948,
       2948,
       80,
       2948,
       2948,
       64,
       2948,
       2948,
       2948,
       2948,
       2948,
       2948,
       64,
       64)

Direction <- c('Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Forward',
               'Forward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Forward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Backward',
               'Forward',
               'Forward')

flag=c('S',
       'S',
       'SA',
       'A',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'S',
       'SA',
       'S',
       'SA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'A',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'PA',
       'PA',
       'A',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA',
       'A',
       'PA')


df3 <- data.frame(Flag=flag[1:40],
                  Direction=Direction[1:40],
                  xmax=IAT[1:40],
                  xmin=IAT[1:40]+0.0003,
                  #xmax=cumsum(sqrt(lens))+IAT,
                  #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                  #ymin=Dir*6-0.5*sqrt(lens),
                  #ymax=Dir*6+0.5*sqrt(lens))
                  ymin=-0.27*sqrt(lens[1:40]),
                  ymax=+0.27*sqrt(lens[1:40]))

df32 <- data.frame(Flag=flag[41:80],
                   Direction=Direction[41:80],
                   xmax=IAT[41:80],
                   xmin=IAT[41:80]+0.0003,
                   #xmax=cumsum(sqrt(lens))+IAT,
                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
                   #ymin=Dir*6-0.5*sqrt(lens),
                   #ymax=Dir*6+0.5*sqrt(lens))
                   ymin=-0.27*sqrt(lens[41:80])-30,
                   ymax=+0.27*sqrt(lens[41:80])-30)

df3=rbind(df3,df32)

# df3 <- data.frame(Flag=flag,
#                   Direction=Direction,
#                   xmax=IAT,
#                   xmin=IAT+0.0001,
#                   #xmax=cumsum(sqrt(lens))+IAT,
#                   #xmin=cumsum(c(0,head(sqrt(lens),n=-1)))+IAT,
#                   #ymin=Dir*6-0.5*sqrt(lens),
#                   #ymax=Dir*6+0.5*sqrt(lens))
#                   ymin=-0.5*sqrt(lens),
#                   ymax=+0.5*sqrt(lens))

df3$Direction_F <- factor(df3$Direction, levels=c("Forward","Backward"))

plot_x <- ggplot(df3, 
                 aes(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,fill=Flag))+
  geom_hline(yintercept=-15,linetype="dashed",size=1.3,alpha=0.5)+
  #  geom_hline(yintercept=-45,linetype="dashed",size=1.3,alpha=0.5)+
  geom_rect(colour="grey40", size=0.5)+
  facet_grid(Direction_F ~ .) + 
  theme_bw()+
  annotate("text", x = -0.002, y = 0, label = "No load")+
  annotate("text", x = -0.002, y = -30, label = "Load")+
  #  annotate("text", x = -0.002, y = -60, label = "Sample 3")+
  theme(axis.ticks.y = element_blank(),
        axis.text.y = element_blank())+
  #  scale_x_continuous(limits = c(-0.0025, 0.0261))+
  labs(title="FTP-connection comparison under load",
       y ="", x = "Time [s]")

#plot_x
plot_regu=plot_x+ theme(legend.position = "bottom")
plot_regu