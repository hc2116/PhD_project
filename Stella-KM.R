
require(ggplot2)

DSS1 <- c(1,1)
DSS2 <- c(0,130)
DSS3 <- c("DSS","DSS")

RFF1 <- c(16/16,16/16,15/16,15/16,14/16,14/16)
RFF2 <- c(0,4,4,40,40,130)
RFF3 <- rep("RFF",6)

RS1 <- c(16/16,16/16,15/16,15/16,14/16,14/16)
RS2 <- c(0,1,1,122,122,130)
RS3 <- rep("RS",6)

df <- data.frame(x = c(DSS1,RFF1,RS1),y = c(DSS2,RFF2,RS2),z = c(DSS3,RFF3,RS3))

g <- ggplot(df, aes(x=y,y=x,linetype=z,color=z))+
  geom_line()+
  theme_bw()+
  theme(legend.title = element_blank())+
  labs(x="Time (months)",y="Probability",title="Kaplan-Meier")+
  ylim(0.8,1)+theme(legend.position=c(0.1, 0.3))+
  scale_x_continuous(breaks = seq(0,130,10)) 
g  

gg_color_hue <- function(n) {
  hues = seq(15, 375, length = n + 1)
  hcl(h = hues, l = 65, c = 100)[1:n]
}


n = 4
hues = gg_color_hue(n)
g <- ggplot(df[df$z=="DSS",], aes(x=y,y=x,linetype=z,color=hues[2]))+
  geom_line(color=hues[1])+
  theme_bw()+
  theme(legend.title = element_blank())+
  labs(x="Time (months)",y="Probability",title="Kaplan-Meier, DSS")+
  ylim(0.8,1)+theme(legend.position="none")+
  scale_x_continuous(breaks = seq(0,130,10))
g  

g <- ggplot(df[df$z=="RFF",], aes(x=y,y=x,linetype=z))+
  geom_line(color=hues[2])+
  theme_bw()+
  theme(legend.title = element_blank())+
  labs(x="Time (months)",y="Probability",title="Kaplan-Meier, RFF")+
  ylim(0.8,1)+theme(legend.position="none")+
  scale_x_continuous(breaks = seq(0,130,10))
g  


g <- ggplot(df[df$z=="RS",], aes(x=y,y=x,linetype=z,color=hues[3]))+
  geom_line(color=hues[3])+
  theme_bw()+
  theme(legend.title = element_blank())+
  labs(x="Time (months)",y="Probability",title="Kaplan-Meier, RS")+
  ylim(0.8,1)+theme(legend.position="none")+
  scale_x_continuous(breaks = seq(0,130,10))
g  

