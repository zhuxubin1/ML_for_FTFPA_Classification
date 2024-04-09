# Script name: Figure5.R
# Purpose: The script is used to generate a plot of the evaluation results of the
#           multiple classification models in Figure 5, including F1 score bars for
#           the hierarchical classification model and the Merged dataset trained model.
# Author: Zhu Xubin
# Date Created: 2024-02-17


# Load dependencies ----------------------

require(ggplot2)
require(tidyverse)
require(dplyr)
require(stringi)
source("toolbox.R")

# Import Data ----------------------

load("RData/Figure5.RData")

# Generation of subplots ------------------------------

F1_Hierarchical_barplot(F1_Hierarchical_data)
