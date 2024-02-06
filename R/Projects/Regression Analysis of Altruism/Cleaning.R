#install.packages("ggfortify")
#install.packages("jtools")
#install.packages("interactions")

library(interactions)
library(jtools) 
library(tidyverse)
library(ggplot2) 
library(dplyr)
library(tidyr)
library(stringr)
library(readxl)
library(stargazer)
library(ggfortify)


#Business: 65-4=61, Med: 66-8=58

#added specialization to business students (so far not used in analysis becase only med students were analyzed for subgroups)
df1 <- as.data.frame(read.csv("Provider_Altruism_Medical.csv", sep= ";"))
df2 <- as.data.frame(read.csv("Provider_Altruism_Business.csv", sep= ";"))
View(df1)
View(df2)


#incomplete answers
df1 <- as.data.frame(df1[-c(1:8, 64, 67),]) #64 both ib and med
df2 <- as.data.frame(df2[-c(18,19),])



#df1 <- as.data.frame(df1[-c(1),])
df2 <- as.data.frame(df2[-c(1),])




df <- rbind(df1, df2)
View(df)

summary(df)
#numeric transform
df <- df %>% 
  mutate_at(c(11:39), as.numeric) #Q10-Q25

df <- df %>% 
  mutate_at(c(41:47), as.numeric) #Q28-Q25

summary(df)


#create means/sums 
df$past_alt <- rowSums(df[ , c(15:29)], na.rm=TRUE)   #Q18 past altruism

df$prof_alt <- rowMeans(df[ , c(31:36)], na.rm=TRUE)  #Q21 professional altruism

df$stat_form <- rowMeans(df[ , c(43:47)], na.rm=TRUE)   #Q29 status formation

#exp
df$past_alt1 <- rowMeans(df[ , c(15:29)], na.rm=TRUE)
df$prof_alt1 <- rowSums(df[ , c(31:36)], na.rm=TRUE)  #Q21 professional altruism
df$stat_form1 <- rowSums(df[ , c(43:47)], na.rm=TRUE)   #Q29 status formation

df

colnames(df)
View(df)

#salary Q - recoding dummy var
df$salary <- ifelse(is.na(df$Q22_1_TEXT)==TRUE, 0, 1) #if NA coded as 0, if number, coded as 1
df$stud <- ifelse(df$Q23  == '1', 0, 1) #if medical - coded as 0,if business(all SBE) - 1

df$salary



#men women dummy
df$gender <- ifelse(df$Q28  == '1', 0, 1) #0 man 1 woman
df$gender
is.double(df$gender)

table(df[df$stud == 0, 'gender'])
table(df[df$stud == 1, 'gender'])



#how altruistic they view themselves dummy

df$below_av <- ifelse(df$Q19 == '1', 1, 0)
df$average <- ifelse(df$Q19 == '2', 1, 0)

df$below_av1 <- ifelse(df$Q19 == '1', 1, 0)
df$above_av1 <- ifelse(df$Q19 == '3', 1, 0)



table(df[df$stud == 0, 'Q19'])
table(df[df$stud == 1, 'Q19'])

h<-ggplot(df, aes(x=Q19, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")
h

#regression for robustness


#master dummy Q24 (1=bachelor, 2=master)
table(df[df$stud == 0, 'Q24'])
table(df[df$stud == 1, 'Q24'])

ggplot(df, aes(x=Q24, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")


#year of study Q25

table(df[df$stud == 0, 'Q25'])
table(df[df$stud == 1, 'Q25'])

ggplot(df, aes(x=Q25, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")





#business with ebe etc dummy

df$stud <- ifelse(df$Q23  == '1', 0, 1) #if medical - coded as 0,if business(all SBE) - 1
df$stud1 <- ifelse(df$stud  == '0', "med", "sbe")
df$med <- ifelse(df$stud  == '0', 1, NA)
df$bus <- ifelse(df$stud  == '1', 1, NA)

table(df$Q23_3_TEXT)

View(df)

#descriptive stats
summary(df)

#DG
mean(df[df$Q23 == 1, 'Q15_1'],na.rm=TRUE) #you 1=med, 2 =business
mean(df[df$Q23 == 2, 'Q15_1'],na.rm=TRUE)

mean(df[df$stud == 0, 'Q15_1'],na.rm=TRUE) #you 0=med, 1=SBE
mean(df[df$stud == 1, 'Q15_1'],na.rm=TRUE)

mean(df[df$Q23 == 1, 'Q15_2'],na.rm=TRUE) #charity 1=med, 2 =business
mean(df[df$Q23 == 2, 'Q15_2'],na.rm=TRUE)

mean(df[df$stud == 0, 'Q15_2'],na.rm=TRUE) #charity 0=med, 1=SBE
mean(df[df$stud == 1, 'Q15_2'],na.rm=TRUE)

median(df[df$stud == 0, 'Q15_2'],na.rm=TRUE) #charity 0=med, 1=SBE
median(df[df$stud == 1, 'Q15_2'],na.rm=TRUE)

summary(df[df$stud == 1, 'Q15_2'])
sd(df[df$stud == 1, 'Q15_2'])

t.test (Q15_2 ~ stud, var.equal=TRUE, data = df)


#i might need to dif colsfor the 2 stud groups to plot
p <- ggplot(df, aes(x=stud1, y=Q15_2, color=stud1)) + 
  geom_boxplot() +
  labs(title="Allocation of Money to Charity",x="Student Group", y = "Eur")
p

u <- ggplot(df, aes(x=stud1, y=prof_alt, color=stud1)) + 
  geom_boxplot() +
  labs(title="Professional Altruism",x="Student Group", y = "Mean Professional Altruism Scores")
u


p + geom_jitter(shape=16, position=position_jitter(0.2))


h1<-ggplot(df, aes(x=Q15_2, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")+
  labs(title="Allocation of Money to Charity",x="Eur", y = "Counts")

h1

ggplot(df, aes(x = prof_alt1, y = Q15_2)) +
  geom_point() +
  stat_smooth(method="lm")


h<-ggplot(df, aes(x=Q15_2, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")
h

ggplot(df, aes(x=past_alt, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")

past <- ggplot(df, aes(x=stud1, y=stat_form, color=stud1)) + 
  geom_boxplot() +
  labs(title="Status formation",x="Student Group", y = "Mean status formation scores")+
  geom_jitter(shape=16, position=position_jitter(0.2))
past

h2<-ggplot(df, aes(x=stat_form, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")+
  labs(title="Status Formation",x="Mean status formation scores", y = "Counts")

h2

#past
mean(df[df$Q23 == 1, 'past_alt'],na.rm=TRUE) # 1=med, 2=business
mean(df[df$Q23 == 2, 'past_alt'],na.rm=TRUE)

mean(df[df$stud == 0, 'past_alt'],na.rm=TRUE) # 0=med, 1=SBE
mean(df[df$stud == 1, 'past_alt'],na.rm=TRUE)

sd(df[df$stud == 0, 'past_alt'])


t.test (Q15_2 ~ stud1, var.equal=TRUE, data = df)
t.test (past_alt ~ stud1, var.equal=TRUE, data = df)
t.test (prof_alt ~ stud1, var.equal=TRUE, data = df)

#prof
mean(df[df$Q23 == 1, 'prof_alt'],na.rm=TRUE) # 1=med, 2=business
mean(df[df$Q23 == 2, 'prof_alt'],na.rm=TRUE)


mean(df[df$stud == 0, 'prof_alt'],na.rm=TRUE) # 0=med, 1=SBE
mean(df[df$stud == 1, 'prof_alt'],na.rm=TRUE)

sd(df[df$stud == 0, 'prof_alt'])


#status
mean(df[df$Q23 == 1, 'stat_form'],na.rm=TRUE) # 1=med, 2=business
mean(df[df$Q23 == 2, 'stat_form'],na.rm=TRUE)

mean(df[df$stud == 0, 'stat_form'],na.rm=TRUE) # 0=med, 1=SBE
mean(df[df$stud == 1, 'stat_form'],na.rm=TRUE)

summary(df[df$stud == 1, 'stat_form'])
sd(df[df$stud == 1, 'stat_form'])

#salary
mean(df[df$Q23 == 1, 'Q22_1_TEXT'],na.rm=TRUE) # 1=med, 2=business
mean(df[df$Q23 == 2, 'Q22_1_TEXT'],na.rm=TRUE)


mean(df[df$stud == 0, 'Q22_1_TEXT'],na.rm=TRUE) # 0=med, 1=SBE
mean(df[df$stud == 1, 'Q22_1_TEXT'],na.rm=TRUE)

df$salary

length(df[df$stud == 0, 'salary'],na.rm=TRUE) # 0=med, 1=SBE
count(df[df$stud == 1, 'salary'],na.rm=TRUE)

ggplot(df, aes(x=salary, color=stud1)) +
  geom_histogram(fill="white", position="dodge", binwidth=1)+
  theme(legend.position="top")



##graphs, mean comparisons, distributions,missing vals

#REGRESSIONS
#just student charity
model <- lm(Q15_2 ~ stud1,
             data = df)
summary(model)

#student past altruism and prof altruism

modelI <- lm(past_alt ~ stud1,
             data = df)

modelII <- lm(prof_alt ~ stud1,
              data = df)

summary(modelI)
summary(modelII)

stargazer(model, modelI,modelII, type="html",title="Three dimensions of Altruism based on Study Program",
          dep.var.labels=c("Experimental Altruism", "Past Altruism", "Professional Altruism"),
          covariate.labels=c("Study Group"),ci=TRUE, ci.level=0.95, out="models_RQ1.htm")
autoplot(model)
autoplot(modelI)
autoplot(modelII)


#internal validity - does past altruism predict DG altruism? (Q15_2 charity)
model_int <- lm(Q15_2 ~ past_alt,
                 data = df)
summary(model_int)

model_ints <- lm(Q15_2 ~ past_alt+stud1,
                 data = df)
summary(model_ints)


model_intII <- lm(past_alt ~ prof_alt,
                  data = df)
summary(model_intII)

model_intIII <- lm(Q15_2~ past_alt + prof_alt,
                  data = df)
summary(model_intIII)


model_intIaa <- lm(Q15_2 ~ past_alt,
                   data = df)
summary(model_intIaa)

model_intI <- lm(Q15_2 ~  past_alt+ prof_alt  + stud1,
                 data = df)
summary(model_intI)

model_intIa <- lm(Q15_2 ~ past_alt + prof_alt,
                 data = df)
summary(model_intIa)

model_intIi <- lm(Q15_2 ~  past_alt+ prof_alt*stud1,
                 data = df)
model_intIii <- lm(Q15_2 ~  past_alt*stud1,
                  data = df)

summary(model_intI)


model_intIIaa <- lm(past_alt ~ prof_alt,
                   data = df)

model_intIIaai <- lm(past_alt ~ prof_alt*stud1,
                    data = df)
summary(model_intIIaa)

stargazer(model_intIaa,model_intIa,model_intIi, model_intIii, model_intIIaa,model_intIIaai, type="html",title="The Connection of Experimental Altruism to Past Altruism and Professional Altruism",
          dep.var.labels=c("Experimental Altruism", "Past Altruism"),
          covariate.labels=c("Past Altruism", "Professional Altruism","Student Group","Interaction var: student group and professional altruism", "Interaction var: student group and past altruism"),ci=TRUE, ci.level=0.95, out="models_RQ2.htm")
autoplot(model_intIaa)
autoplot(model_intIa)
autoplot(model_intIIaa)


stargazer(model_intIaa,model_intIa, model_intIIaa, model_intIIaai , type="html",title="The Connection of Experimental Altruism to Past Altruism and Professional Altruism",
          dep.var.labels=c("Experimental Altruism", "Past Altruism"),
          covariate.labels=c("Past Altruism", "Professional Altruism"),ci=TRUE, ci.level=0.95, out="models_RQ2i.htm")

#collinearity

model_int1 <- lm(Q15_2 ~ gender + Q25 + past_alt +stat_form + salary,
                 data = df)
summary(model_int1)

model_int11 <- lm(Q15_2 ~ gender + Q25 + past_alt +stat_form ,
                 data = df)
summary(model_int11)

##past altruism collinearity
model_int111 <- lm(past_alt ~ stat_form,
                  data = df)
summary(model_int111)


model_int1 <- lm(Q15_2 ~ stat_form1*past_alt,
                 data = df)
summary(model_int1)

model_int1 <- lm(Q15_2 ~ stat_form1*past_alt,
             data = df)
summary(model_int1)

model <- lm(Q15_2 ~ stud1*Q25,  #Q25 year of study
                 data = df)

summary(model)

model_int1 <- lm(Q15_2 ~ stat_form1*past_alt,
                 data = df)
summary(model_int1)

#how they view themselves
models <- lm(past_alt ~ below_av1 + above_av1,
             data = df)
summary(models)

modelsi <- lm(Q15_2 ~ below_av1 + above_av1,
             data = df)
summary(modelsi)


stargazer(models,type="html",title="Past Altruism",
          dep.var.labels=c("Past Altruism"),
          covariate.labels=c("below average dummy", "above average dummy"),ci=TRUE, ci.level=0.95, out="models_below.htm")


#year and status formation
modelo <- lm(stat_form ~ Q25, #Q25 year
               data = df)
summary(modelo)


#DG MODELLING
modeldg <- lm(Q15_2 ~ past_alt+stat_form + prof_alt + stud1, #salary not sign, Q22 salary n# not sign
              data = df)
modeldg1 <- lm(Q15_2 ~ past_alt+stat_form+gender, #salary not sign, Q22 salary n# not sign
              data = df)

modelDG <- lm(Q15_2 ~ past_alt*stat_form+gender, #salary not sign, Q22 salary n# not sign
             data = df)

modelDG2 <- lm(Q15_2 ~ past_alt*stat_form+gender+salary, #salary not sign, Q22 salary n# not sign
              data = df)
modelDG3 <- lm(Q15_2 ~ past_alt*stat_form+gender+Q25, #Q25 year 
                 data = df)
modelDG4 <- lm(Q15_2 ~ prof_alt*stud1 +past_alt*stat_form+gender, #Q25 year 
               data = df)
modelDG5 <- lm(Q15_2 ~ past_alt*stud1 +past_alt*stat_form+gender, #Q25 year 
               data = df)

modelDG3mb <- lm(Q15_2 ~ past_alt*stat_form+gender+Q25*Q24, #Q25 year Q24 master bachelor
               data = df)

summary(modelDG3mb)

summary(modeldg)
summary(modeldg1)
summary(modelDG)
summary(modelDG2)
summary(modelDG3)
summary(modelDG4)

stargazer(modeldg,modeldg1, modelDG, modelDG2,modelDG3,type="html",title="Experimental Altruism",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Past Altruism", "Status formation","Gender","Salary Indication","year of study", "Interaction variable: Status formation and Past Altruism"),ci=TRUE, ci.level=0.95, out="models_RQ3.htm")

stargazer(modeldg,modeldg1, modelDG, modelDG2,modelDG3mb,type="html",title="Experimental Altruism",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Past Altruism", "Status formation","Gender","Salary Indication","year of study","Bachelor/Master program" ,"Interaction variable: Status formation and Past Altruism", "Interaction variable: Year of study and Bachelor/Master program"),ci=TRUE, ci.level=0.95, out="models_RQ3i.htm")

stargazer(modeldg,modeldg1, modelDG, modelDG2,modelDG3,type="html",title="Experimental Altruism",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Past Altruism", "Status formation","Professional Altruism", "Study group", "Gender","Salary Indication","year of study", "Interaction variable: Status formation and Past Altruism"),ci=TRUE, ci.level=0.95, out="models_RQ3stud.htm")

stargazer(modeldg,modeldg1, modelDG, modelDG2,modelDG3,modelDG4,modelDG5,type="html",title="Experimental Altruism",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Past Altruism", "Status formation","Professional Altruism", "Study group", "Gender","Salary Indication","year of study", "Interaction var: professional altruism and study group", "Interaction var: past altruism and study group", "Interaction var: past altruism and status formation"),ci=TRUE, ci.level=0.95, out="models_RQ3studpast.htm")


autoplot(modelDG)

#interaction plot
summ(modelDG) 
interact_plot(modelDG, pred = past_alt, modx = stat_form, centered = "none",x.label = "Past Altruism", y.label = "Allocations of money to charity (eur)",
              main.title = "Interaction Plot",  legend.main = "Status-and-identity formation",
              colors = "seagreen") 
#interact_plot(modelDG, pred = stat_form, modx = past_alt, centered = "none")


par(interaction.plot(
  x.factor = df$stat_form,
  trace.factor = df$past_alt,
  response = df$Q15_2,
  fun = median,
  ylab = "Weight loss after six weeks",
  xlab = "Diet type",
  trace.label = "Gender",
  col = c("#0198f9", "#f95801"),
  lyt = 1,
  lwd = 3
))




library(tidyverse)
library(broom)

model.diag.metrics <- augment(modelDG)
model.diag.metrics <- model.diag.metrics %>%
  mutate(index = 1:nrow(model.diag.metrics)) %>%
  select(index, everything(), -.se.fit, -.sigma)
# Inspect the data
head(model.diag.metrics, 4)
View(model.diag.metrics %>%
  top_n(5, wt = .cooksd))


#Past alt


modelpast <- lm(past_alt ~ stud+stat_form+average+below_av,
               data = df)
summary(modelpast)


#t-test

#Q19 i consider myself... alt person
#Q28 gender
mean(df[df$Q28 == 1, 'prof_alt'],na.rm=TRUE) #you 1=man, 2=woman
mean(df[df$Q28 == 2, 'prof_alt'],na.rm=TRUE)




#SUBGROUPS


#subgroups based on Specialization




n_distinct(df[df$stud == 0, 'Specialty'])
n_distinct(df[df$stud == 1, 'Specialty'])

mean(table(df[df$stud == 0, 'Specialty']))
mean(table(df[df$stud == 1, 'Specialty']))


#altruism for grouped?
past <- ggplot(df, aes(x=stud1, y=stat_form, color=stud1)) + 
  geom_boxplot() +
  labs(title="Status formation",x="Student Group", y = "Mean status formation scores")+
  geom_jitter(shape=16, position=position_jitter(0.2))
past


res <- model.matrix(~Specialty, data = df)
head(res[, -1])


library(car)
model2 <- lm(Q15_2 ~ Specialty,
             data = df)
Anova(model2)
summary(model2)
#http://www.sthda.com/english/articles/40-regression-analysis/163-regression-with-categorical-variables-dummy-coding-essentials-in-r/ 


install.packages("fastDummies")
library(fastDummies)
spec_dummies <- as.data.frame(dummy_cols(df$Specialty))
spec_dummies
names(spec_dummies)


model_int <- glm(Q15_2 ~ results,
                 data = df)
summary(model_int)


#grouped specialties
#surgery, diagnostics, psychiatry, anethesiology and internal, internal med, pediatry
df$Specialty
df$medSpecialty <- ifelse(df$stud == 0, df$Specialty, NA)
df$medSpecialty


df$idk <- ifelse(df$medSpecialty == 'idk', 1, 0)
df$surg <- ifelse(df$medSpecialty == "Surgery"| df$medSpecialty == "Surgery "| df$medSpecialty == "Ob/gyn"| df$medSpecialty == "urology", 1, 0)
df$internal <- ifelse(df$medSpecialty == "Neurology" |df$medSpecialty== "Geriatrics" |df$medSpecialty=="Immunology" |df$medSpecialty== "Internal Medicine" |df$medSpecialty=="Cardiology", 1,0)
df$psych <- ifelse(df$medSpecialty == "Neuropsychiatry " |df$medSpecialty=="Psychiatry", 1,0)
df$ped <- ifelse(df$medSpecialty == 'pediatrics', 1, 0)
df$GP <- ifelse(df$medSpecialty == 'GP' |df$medSpecialty== "Sports arts", 1, 0)
df$an_int <- ifelse(df$medSpecialty == 'Anesthesiology' |df$medSpecialty=="Intensive care" |df$medSpecialty== "Intensivist" |df$medSpecialty=="Pediatric intensive care ", 1, 0)
df$int <- ifelse(df$medSpecialty=="Intensive care" |df$medSpecialty== "Intensivist" |df$medSpecialty=="Pediatric intensive care ", 1, 0)
#diagnostics - pathology left


modelspec1 <- lm(Q15_2 ~ idk + surg + internal + psych + ped
                 + GP ,
                 data = df)
summary(modelspec1)


#specialties 3 gorups
df$surg1 <- ifelse(df$surg == 1,1,0)
df$nonsurg <- ifelse(df$internal ==1 | df$psych==1 | df$ped ==1 | df$GP ==1 |df$int==1, 1,0)
df$sup <- ifelse(df$an_int == 1 | df$int==1 | df$medSpecialty=="Pathology" | df$medSpecialty=="Oncology",1,0)
#left idk


table(df$sup)



table(df$nonsurg)
table(df[df$stud == 0, 'sup'])

modelspec2 <- lm(Q15_2 ~  surg1 + nonsurg +sup
  ,data=df)

summary(modelspec2)

stargazer(modelspec2,type="html",title="Experimental Altruism based on Preferred Medical Specialties",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Surgical Specialties", "Non-surgical Specialties","Supportive Specialties"),ci=TRUE, ci.level=0.95, out="models_RQsub.htm")

modelll <- lm(Q15_2 ~  prof_alt
                 ,data=df)

summary(modelll)

#business students grouped 
df$Specialty
df$sbeSpecialty <- ifelse(df$stud == 1, df$Specialty, NA)
df$sbeSpecialty

df$scontrol <- ifelse(df$sbeSpecialty == 'controlling'|df$sbeSpecialty == 'strategy'|df$sbeSpecialty == 'supplychain', 1, 0)
df$secon <- ifelse(df$sbeSpecialty == 'econ', 1, 0)
df$seme <- ifelse(df$sbeSpecialty == 'emerging'|df$sbeSpecialty == 'sustfinance'|df$sbeSpecialty == 'entre', 1, 0)
df$sfinance <- ifelse(df$sbeSpecialty == 'finance', 1, 0)
df$sIB <- ifelse(df$sbeSpecialty == 'IB', 1, 0)
df$sinfo <- ifelse(df$sbeSpecialty == 'info'|df$sbeSpecialty == 'marketing'|df$sbeSpecialty == 'HR', 1, 0)

modelsbe <- lm(Q15_2 ~ scontrol + secon +seme+sfinance+sIB+sinfo,
               data = df)
summary(modelsbe)

stargazer(modelsbe,type="html",title="Experimental Altruism based on Business-related Specialties",
          dep.var.labels=c("Experimental Altruism"),
          covariate.labels=c("Controlling+", "Economics","Emerging+", "Finance", "International Business","Marketing+"),ci=TRUE, ci.level=0.95, out="models_SBESpec.htm")



#subsetting df for med students only
df_med <- df[ which(df$stud=='0'), ]
View(df_med)


modeldgm <- lm(Q15_2 ~ past_alt, #salary not sign, Q22 salary n# not sign
              data = df_med)
modeldg1m <- lm(Q15_2 ~ past_alt+stat_form+gender, #salary not sign, Q22 salary n# not sign
               data = df_med)

modelDGm <- lm(Q15_2 ~ past_alt*stat_form+gender, #salary not sign, Q22 salary n# not sign
              data = df_med)

modelDG2m <- lm(Q15_2 ~ past_alt*stat_form+gender+salary, #salary not sign, Q22 salary n# not sign
               data = df_med)

modelDG3m <- lm(Q15_2 ~ past_alt*stat_form+gender+Q25, #Q25 year
               data = df_med)

summary(modelDG3m)
