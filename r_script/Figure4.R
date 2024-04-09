# Script name: Figure4.R
# Purpose: The script is used to generate a plot of the evaluation results of the
#           multiple classification models in Figure 4, including F1 score bars
#           using PCA+LDA tandem dimensionality reduction algorithm and random
#           forest algorithm.
# Author: Zhu Xubin
# Date Created: 2024-02-17


# Load dependencies ----------------------

require(ggplot2)
require(tidyverse)
require(dplyr)
require(stringi)
source("toolbox.R")

# Import Data ----------------------

load("RData/Figure4.RData")

# Generation of subplots ------------------------------

## 1.Multi-classification bar chart ----------------------

F1_multi_barplot(F1_multi_PCA, "PCA+LDA")
F1_multi_barplot(F1_multi_RF, "RF")
  

