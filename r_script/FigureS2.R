# Script name: FigureS1.R
# Purpose: Used to generate representational images required by Figure S2.
# Author: Zhu Xubin
# Date Created: 2024-02-18


# Load dependencies ----------------------

require(ggplot2)
require(readxl)
require(dplyr)
require(ggnewscale)
source("toolbox.R")

# Import Data ----------------------

load("RData/FigureS2.RData")

# Generation of subplots ------------------------------

## 1.Grain size comparison histogram ----------------------

size_comparison_histogram(df)
zeta_comparison_histogram(df)
wavelength_comparison_histogram(df)
