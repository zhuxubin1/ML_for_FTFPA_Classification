# Script name: FigureS5.R
# Purpose: The script is used to generate the results of the binary model evaluation
#           in Figure S5. Includes model P-R bubble charts using Single data sets and
#           Merged data sets.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(dplyr)
require(readxl)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS5.RData")

# Generation of subplots ------------------------------

## 1.bubble plot ----------------------

bubble_plot(bubble_Single, "Single")
bubble_plot(bubble_Merged, "Merged")
