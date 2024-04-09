# Script name: FigureS7-8.R
# Purpose: Used to generate representational images required by Figure 76 and S8.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(ggpubr)
require(gridExtra)
require(stringi)
require(ggfortify)
source("toolbox.R")

# Import Data ----------------------

load("RData/Universal_variable.RData")
load("RData/FigureS7-8.RData")

# Generation of subplots ------------------------------

## 1.LDA scatter ----------------------

for (i in 1:length(scatter)) {
  data_name <- scatter[[i]]$name
  data_name_list <- strsplit(data_name, '_')
  t <- data_name_list[[1]][2]
  c <- data_name_list[[1]][3]
  
  scatter_plot(as.data.frame(scatter[[i]]), LDA[i, ], t, c)
}
