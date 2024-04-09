# Script name: Figure3.R
# Purpose: Used to generate representational images required by Figure3.
# Author: Zhu Xubin
# Date Created: 2024-02-15


# Load dependencies ----------------------

require(stringi)
require(ggplot2)
require(ROCR)
require(pROC)
require(dplyr)
require(ggpubr)
require(readxl)
require(ggnewscale)
source("toolbox.R")

# Import Data ----------------------

load("RData/Universal_variable.RData")
load("RData/Figure3_ROC.RData")
load("RData/Figure3_errorbar.RData")
load("RData/Figure3_F1_barplot.RData")

# Generation of subplots ------------------------------

## 1.ROC curve ----------------------

d_color <- c('#44045a', '#413e85', '#30688d',
             '#1f928b', '#35b777', '#91d542',
             '#f8e620', '#FF8000', '#FE2E2E')
s_color <- c('#c1a4c8', '#b0a9d1', '#8bb2d4',
             '#79b9b3', '#8cb89d', '#a3b48d',
             '#f9eec4', '#cea68c', '#d6a198')


Roc_curve(save_ROC[[1]]$ROC_1, save_ROC[[1]]$ROC_3, '#206AB1', '#8FB4D8', 'xBlank', "all")
for (i in 2:37) {
  k <- case_when(i <= 10 & i >= 2 ~ 0,
                 i <= 19 & i >= 11 ~ 1,
                 i <= 28 & i >= 20 ~ 2,
                 i <= 37 & i >= 29 ~ 3)
  j <- i - 9 * k - 1
  s <- species[j]
  d_c <- d_color[j]
  s_c <- s_color[j]
  a <- abbr[j]
  c <- case_when(i <= 10 & i >= 2 ~ '10^4',
                 i <= 19 & i >= 11 ~ '10^5',
                 i <= 28 & i >= 20 ~ '10^6',
                 i <= 37 & i >= 29 ~ 'all')
  
  Roc_curve(save_ROC[[i]]$ROC_1, save_ROC[[i]]$ROC_3, d_c, s_c, s, c, a)
}


## 2.AUROC & AUPR Error bar diagram ----------------------

AUROC_AUPR_errorbar(AUROC_data_Single, "AUROC", "Single")
AUROC_AUPR_errorbar(AUPR_data_Single, "AUPR", "Single")
AUROC_AUPR_errorbar(AUROC_data_Merged, "AUROC", "Merged")
AUROC_AUPR_errorbar(AUPR_data_Merged, "AUPR", "Merged")

## 3.F1 score bar plot ----------------------

F1_barplot(as.data.frame(save_F1_barplot[[1]]), 'xBlank', 'all')
for (i in 2:37) {
  k <- case_when(i <= 10 & i >= 2 ~ 0,
                 i <= 19 & i >= 11 ~ 1,
                 i <= 28 & i >= 20 ~ 2,
                 i <= 37 & i >= 29 ~ 3)
  j <- i - 9 * k - 1
  s <- species[j]
  a <- abbr[j]
  c <- case_when(i <= 10 & i >= 2 ~ '10^4',
                 i <= 19 & i >= 11 ~ '10^5',
                 i <= 28 & i >= 20 ~ '10^6',
                 i <= 37 & i >= 29 ~ 'all')
  F1_barplot(as.data.frame(save_F1_barplot[[i]]), s, c, a)
}
