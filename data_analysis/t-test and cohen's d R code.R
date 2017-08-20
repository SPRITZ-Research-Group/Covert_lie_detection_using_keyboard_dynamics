# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  Merylin Monaro
# See GNU General Public Licence v.3 for more details.
#  NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

##load data (load the .txt file named "Data for descriptive statistical analysis - 40 subjects")

data<-read.delim(file.choose(),header=T)

str(data)

#mind condition 0=truthteller 1=liar

data$mind_condition <- as.factor(data$mind_condition)

##load packages

library(boot)
library (ggm)
library(ggplot2)
library(Hmisc)
library(polycor)
library(ltm)
library(pastecs)
library(WRS2)
library(ez)
library(BayesFactor)
library(effsize)
library(lsr)

#t-test, Bayes Factor and Cohen's d calculation

#### Errors

Model_errors<-t.test(errors~mind_condition, data=data, var.equal=FALSE, paired=FALSE)
Model_errors

t.test(errors ~ mind_condition, data = data, var.eq=FALSE)

tErrors<-t.test(data$errors[data$mind_condition=="1"],data$errors[data$mind_condition=="0"])
tErrors 

tErrorsBF<-ttestBF(data$errors[data$mind_condition=="1"],data$errors[data$mind_condition=="0"])
summary(tErrorsBF)

#or
bf = ttestBF(formula = errors ~ mind_condition, data = data)
bf

cohen.d(data$errors[data$mind_condition=="1"],data$errors[data$mind_condition=="0"])

#### Prompted-firstdigit

t.test(prompted.firstdigit ~ mind_condition, data = data, var.eq=FALSE)

bf = ttestBF(formula = prompted.firstdigit ~ mind_condition, data = data)
bf

cohen.d(data$prompted.firstdigit[data$mind_condition=="1"],data$prompted.firstdigit[data$mind_condition=="0"])

#### Prompted-firstdigit adjusted GULPEASE

t.test(Prompted.firstdigit_adjusted_GULPEASE ~ mind_condition, data = data, var.eq=FALSE)

bf = ttestBF(formula =Prompted.firstdigit_adjusted_GULPEASE ~ mind_condition, data = data)
bf

cohen.d(data$Prompted.firstdigit_adjusted_GULPEASE[data$mind_condition=="1"],data$Prompted.firstdigit_adjusted_GULPEASE[data$mind_condition=="0"])


#### Prompted-enter

t.test(prompted.enter ~ mind_condition, data = data, var.eq=FALSE)

bf = ttestBF(formula = prompted.enter ~ mind_condition, data = data)
bf

cohen.d(data$prompted.enter[data$mind_condition=="1"],data$prompted.enter[data$mind_condition=="0"])


