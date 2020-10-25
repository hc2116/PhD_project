
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

dat <- structure(list(Year = c(2013L, 2013L, 2013L, 2013L, 2013L, 2014L, 2014L, 2014L, 2014L, 2014L), 
                      Category = structure(c(1L, 2L, 3L,4L, 5L, 1L, 2L, 3L, 4L, 5L), 
                                           .Label = c("Beverages", "Condiments","Confections", "Dairy Products", "Seafood"), class = "factor"), 
                      TotalSales = c(102074.29, 55277.56, 36415.75, 30337.39, 53019.98, 81338.06, 55948.82, 44478.36, 84412.36, 65544.19), 
                      AverageCount = c(22190.06, 14173.73, 12138.58, 24400, 27905.25, 35400, 19981.72, 24710,32466, 14565.37)), 
                 .Names = c("Year", "Category", "TotalSales","AverageCount"), 
                 class = "data.frame", row.names = c(NA, -10L))

library(reshape2)
dat_l <- melt(dat, id.vars = c("Year", "Category"))

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
x1 <- 1-abs(rnorm(N,sd=0.02))
x2 <- 1-abs(rnorm(N,sd=0.01))
x3 <- 1-abs(rnorm(N,sd=0.04))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",N),rep("flow",N),rep("seq",N)))
df2=data.frame(ymin=c(quantile(x1,0.1),quantile(x2,0.1),quantile(x3,0.1)),
               ymax=c(quantile(x1,0.9),quantile(x2,0.9),quantile(x3,0.9)),
               y=c(median(x1),median(x2),median(x3)),
               Metric=c("conn","flow","seq"))

dfA=df
dfB=df
dfA$Set="A"
dfB$Set="B"

df2A=df2
df2B=df2
df2A$Set="A"
df2B$Set="B"

df=rbind(dfA,dfB)
df2=rbind(df2A,df2B)

pA <- ggplot(df, aes(x=Metric, y=x)) + 
  #geom_dotplot(binaxis='y', stackdir='center', aes(colour=Metric,fill=Metric),
  #             dotsize =0.3,binwidth=0.01,stackratio = .3)
  geom_point(aes(color=Metric),alpha=0.8)+
  facet_grid(. ~ Set)+
  geom_errorbar(df2,mapping=aes(y=y,x=Metric,ymin=ymin, ymax=ymax), 
                width=.2,size=1,)+
  theme_bw()+  labs(y="%",x="")+
  geom_point(df2,mapping=aes(y=y,x=Metric,color=Metric),fill="white",shape = 21,size=4,show.legend=FALSE)


plot_grid(pA, pA,pA,pA, labels = c('A', 'B', 'C','D'), ncol = 4)

pA <- ggplot(df, aes(x=Metric, y=x)) + 
  geom_dotplot(binaxis='y', stackdir='center')+
stat_summary(fun.data = "mean_se", colour = "red", size = 1)+
  theme_bw()+  labs(y="%",x="")
  #labs(title="HTTP",y="Similarity (% of overall)")

# B
x1 <- 1-abs(rnorm(30,sd=0.02))
x2 <- 1-abs(rnorm(30,sd=0.1))
x3 <- 1-abs(rnorm(30,sd=0.04))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",30),rep("flow",30),rep("seq",30)))
pB <- ggplot(df, aes(x=Metric, y=x)) + 
  geom_dotplot(binaxis='y', stackdir='center')+
  stat_summary(fun.data = "mean_se", colour = "red", size = 1)+
  theme_bw()+labs(y="%",x="")

# C
x1 <- 1-abs(rnorm(30,sd=0.02))
x2 <- 1-abs(rnorm(30,sd=0.00001))
x3 <- 1-abs(rnorm(30,sd=0.04))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",30),rep("flow",30),rep("seq",30)))
pC <- ggplot(df, aes(x=Metric, y=x)) + 
  geom_dotplot(binaxis='y', stackdir='center')+
  stat_summary(fun.data = "mean_se", colour = "red", size = 1)+
  theme_bw()+labs(y="%",x="")

# D
x1 <- 1-abs(rnorm(30,sd=0.05))
x2 <- 1-abs(rnorm(30,sd=0.1))
x3 <- 1-abs(rnorm(30,sd=0.1))
df=data.frame(x=c(x1,x2,x3),
              Metric=c(rep("conn",30),rep("flow",30),rep("seq",30)))
pD <- ggplot(df, aes(x=Metric, y=x)) + 
  geom_dotplot(binaxis='y', stackdir='center')+
  stat_summary(fun.data = "mean_se", colour = "red", size = 1)+
  theme_bw()+labs(y="%")


plot_grid(pA, pB,pC,pD, labels = c('A', 'B', 'C','D'), ncol = 1)
