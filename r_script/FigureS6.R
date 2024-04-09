# Script name: FigureS6.R
# Purpose: Used to draw spectral heat maps.
# Author: Zhu Xubin
# Date Created: 2024-03-16


# Load dependencies ----------------------

require(ggplot2)
require(readxl)
require(dplyr)
require(pheatmap)
require(gridExtra)
source("toolbox.R")

# Import Data ----------------------

load("RData/figureS6.RData")

# Generation of subplots ------------------------------

## 1.Spectral heat map ----------------------

p_list <- list()
for (index in 1:90) {
  p <- GLH_heatmap(df_list[[index]])
  p_list[[index]] <- p$gtable
}
heights <- c(rep(2, 9), 1)
merged_p <- grid.arrange(grobs = p_list, nrow = 10,
                         padding = 0, heights = heights)

## 2.Upper legend  ----------------------

upper_legend <- upper_label()
upper_legend_p <- grid.arrange(grobs = list(upper_legend, merged_p),
                               nrow = 2, padding = 0, heights = c(2.5, 15))

## 3.Left legend  ----------------------

left_legend <- left_label()
upper_left_legend_p <- grid.arrange(grobs = list(left_legend, upper_legend_p),
                                    ncol = 2, widths = c(2.5, 15))

## 4.Save the figure  ----------------------

ggsave("plot/FS6/FigureS6.png", upper_left_legend_p, width = 10, height = 10,
       units = "in", dpi = 1200)

