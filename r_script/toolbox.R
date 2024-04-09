# Script name: toolbox.R
# Purpose of script: Stores the body of a custom function.
# Author: Zhu Xubin
# Date Created: 2024-02-15


# Import Data ----------------------

load("RData/Universal_variable.RData")

# Figure 1 ------------------------------


table_add_avg_sd <- function(data, data_type) {
  # This function is used to calculate the mean and standard deviation
  # for data.
  #  
  # Args:   
  #   data: A table containing AuNPs raw particle size or zeta potential
  #         data.
  #   data_type: Type of input data. "size" corresponds to AuNPs particle
  #         size data. "zeta" corresponds to AuNPs zeta potential data.
  # 
  # Returns:  
  #   Data table with mean and standard deviation.
  
  data$Label <- factor(data$Label, levels=c("AuNPs1","AuNPs2","AuNPs3"))
  if (data_type == "size") {
    data <- data %>%
      mutate(Avg = rowMeans(data[, 2:11], na.rm = TRUE),
             Sd = apply(data[, 2:11], 1, sd, na.rm = TRUE))
    data[,2:13] <- round(data[, 2:13], 3)
  }
  if (data_type == "zeta"){
    data <- data %>%
      mutate(Avg = rowMeans(data[, 2:4]),
             Sd = apply(data[, 2:4], 1, sd))
    data[,2:6] <- round(data[, 2:6], 3)
  }
  return(data)
}


AuNPs_size_histgram <- function(data, AuNPs_type, interval, color) {
  
  
  data_long <- data %>%  
    pivot_longer(  
      cols = -Label,
      names_to = "Size_type",
      values_to = "Size"
    ) %>% drop_na()
  
  data_filtered <- data_long %>%
    filter(Label == AuNPs_type)
  
  if (AuNPs_type == "AuNPs1") {
    xlim_min <- 2
    xlim_max <- 8
  }
  if (AuNPs_type == "AuNPs2") {
    xlim_min <- 5
    xlim_max <- 30
  }
  if (AuNPs_type == "AuNPs3") {
    xlim_min <- 40
    xlim_max <- 55
  }
  
  scale <- max(table(cut(data_filtered$Size,
                         seq(interval/2, max(data_filtered$Size) + interval + interval / 2, interval))))
  
  p <- ggplot(data_filtered, aes(x = Size)) +
    geom_histogram(binwidth = interval, position = "dodge", fill = color) +
    geom_density(aes(y = ..scaled.. * scale), color = "grey", adjust = 3,
                 size = 2) +
    labs(x = "Length (nm)", y = "Frequency") +
    scale_y_continuous(expand = c(0, 0), limits = c(0, scale * 1.2)) +
    xlim(xlim_min, xlim_max) +
    theme_minimal() +
    theme(text = element_text(family = 'sans', face = "bold"),
          panel.border = element_rect(colour = "black",
                                      fill = "NA", size = 1.5),
          panel.grid = element_blank(),
          axis.title.y = element_text(size = 15),
          axis.text = element_text(size = 13))
  ggsave(sprintf("plot/F1/F1_AuNPs_size_histgram_%s.png", AuNPs_type), p,
         units = 'cm', width = 8, height = 8, dpi = 1200)
}


AuNPs_wave_plot <- function(data, color, label, y_lim){
  # This function is used to generate UV-Vis spectral waveform of
  # AuNPs. The waveform data is derived from the mean curve of the
  # data set and smoothed by a generalized additive model (GAM).
  #  
  # Args:   
  #   data: The mean curve of AuNPs UV-Vis spectral waveform data.
  #   color: Corresponding color.
  #   label: AuNPs label.
  #   y_lim: The y-axis limit.
  
  ggplot(data, aes(x = wavelength, y = AVG)) +
    geom_smooth(method = "gam",se = FALSE, color = color) +
    labs(x = "Wavelength(nm)", y = "Absorbance(a.u.)", title = " ") +  
    scale_y_continuous(labels = function(labels){sprintf("%.2f", labels)},
                       expand = c(0, y_lim)) +
    theme_minimal() +
    theme(text = element_text(family = 'sans'),
          panel.border = element_rect(colour = "black",
                                      fill = "NA", size = 1.5),
          panel.grid = element_blank(),
          axis.title = element_text(face = 'bold',size = 15),
          axis.text = element_text(face = 'bold', size = 13))
  
  image_name <- sprintf("plot/F1/F1_curve_plot_%s_1.png", label)
  ggsave(image_name, units = 'cm', width = 7, height = 9, dpi = 1200)
}


AuNPs_zeta_plot <- function(data){
  # This function is used to generate a Zeta potential bar chart
  # for AuNPs.
  #  
  # Args:   
  #   data: Data table with mean and standard deviation.

  p <- ggplot(data, aes(x = Label, y = Avg, fill = Label)) +
    geom_bar(stat = "identity", width = .8) +  
    scale_fill_manual(values = c("AuNPs1" = "#452a3d","AuNPs2" = "#a07673",
                                 "AuNPs3" = "#eed5b7")) +  
    geom_errorbar(aes(ymin = Avg - Sd, ymax = Avg + Sd),
                  width = .1, position = position_dodge(.9)) +    
    theme_minimal() + 
    theme(text = element_text(family = 'sans'),
          legend.position = "none",
          panel.border = element_rect(colour = "black",
                                      fill = "NA", size = 1.5),
          panel.grid = element_blank(),
          axis.title.y = element_text(face = 'bold',size = 15),
          axis.text = element_text(face = 'bold', size = 13)) + 
    labs(title = "", x = "", y = "Zeta potential(mV)") +
    scale_y_continuous(limits = c(-45, 0),
                       breaks = seq(-40, 0, by = 10),
                       expand = c(0, 0)) +
    geom_text(aes(label = Avg), vjust = c(4, 3.5, 2), size = 6)
  ggsave("plot/F1/F1_Zeta_plot.png", p, units = 'cm',
         width = 8, height = 12, dpi = 1200)
}



# Figure 3 ------------------------------


Roc_curve <- function(ROC_1, ROC_3, d_color, s_color, s, c, abbr = ''){
  # This function is used to generate ROC curves using Single
  # data and Merged data under the same condition, and to attach
  # a shaded area of ci=0.95 to each ROC curve. And save the image
  # in png format.
  #  
  # Args:   
  #   ROC_1: ROC curve data for training the model with Single data
  #         under specified conditions. Save it as a list, with two
  #         columns, situation and probability.
  #   ROC_3: ROC curve data for training the model with Merged data
  #         under specified conditions. Save it as a list, with two
  #         columns, situation and probability.
  #   d_color: ROC curve color for the target sample, which is a
  #         model trained with Merged data.
  #   s_color: The color of the ROC curve confidence interval for
  #         the target sample, which is a model trained with Merged
  #         data.
  #   s: Microbial species corresponding to mapping data.
  #   c: Microbial concentration corresponding to mapping data.
  #   abbr: Microbial abbreviations corresponding to mapping data. 
  
  if (s == 'xBlank') {
    color_1 <- "#E28829"
    color_2 <- "#FFE0B7"
  }
  else {
    color_1 <- "#5b5b5b"
    color_2 <- "#bbbbbb"
  }
  
  roc2_1 <- roc(ROC_1$situation, ROC_1$probability, levels=c(0,1), direction=">")
  roc2_3 <- roc(ROC_3$situation, ROC_3$probability, levels=c(0,1), direction=">")
  
  auc2_1 <- auc(roc2_1)[1]
  auc2_3 <- auc(roc2_3)[1]
  auc2_text_1 <- sprintf("AUC(S): %.2f", round(auc2_1, 4))
  auc2_text_3 <- sprintf("AUC(M): %.2f", round(auc2_3, 4))
  
  ci_1 <- ci(roc2_1)
  ci_3 <- ci(roc2_3)
  
  roc_list <- list(roc2_1, roc2_3)
  ci.list <- lapply(roc_list, ci.se, specificities = seq(0, 1, l = 25))
  dat.ci.list <- lapply(ci.list, function(ciobj) 
    data.frame(x = as.numeric(rownames(ciobj)),
               lower = ciobj[, 1],
               upper = ciobj[, 3]))
  
  p <- ggroc(roc_list, size = 1.5) +
    geom_segment(aes(x = 1, y = 0, xend = 0, yend = 1), colour = 'grey', 
                 linetype = 'dashed') + 
    scale_color_manual(values = c(color_1, d_color)) +
    annotate("text", x = 0.3, y = 0.05, label = auc2_text_1, size = 7.5) + 
    annotate("text", x = 0.3, y = 0.17, label = auc2_text_3, size = 7.5) + 
    theme_bw() + 
    theme(text = element_text(family = "sans"),
          panel.grid = element_blank(),
          axis.title = element_text(face = "bold", size = 15),   
          axis.text = element_text(face = "bold", size = 14),   
          plot.title = element_text(face = "bold", size = 17),
          legend.position = "none") +
    labs(title = abbr,x = "FPR", y = "TPR")
  p1 <- p + geom_ribbon(data = dat.ci.list[[1]], 
                        aes(x = x, ymin = lower, ymax = upper),
                        fill = color_2, alpha = 0.5, inherit.aes = F) +
    geom_ribbon(data = dat.ci.list[[2]], 
                aes(x = x, ymin = lower, ymax = upper),
                fill = s_color, alpha = 0.5, inherit.aes = F)
  
  image_name = sprintf("plot/F3/F3_ROC_%s_%s.png", s, c)
  ggsave(filename = image_name , p1 , width = 4, height = 4,
         units = "in", dpi = 1200)
}


AUROC_AUPR_errorbar <- function(df, plot_type, data_type) {
  # This function is used to generate AUROC and AUPR error bar
  # plots for cross-validated models. Divided into two groups
  # of images based on using Single data or Merged data. The
  # image is finally output in png format.
  #  
  # Args:   
  #   df: AUROC or AUPR data after 30 fold cross-validation.
  #   plot_type: Types of error bar graphs, including AUROC and AUPR.
  #   data_type: Type of graph data, including Single and Merged.

  errorbar_color <- c("#FE8600", "#FEB705", "#219EBC", "#034C75")
  background_color <- case_when(data_type == "Single" ~ c("#EFE4B0", "#FFFFFF"),
                                data_type == "Merged" ~ c("#C8BFE7", "#FFFFFF"))
  
  
  df <- df %>% filter(target != "xBlank")
  
  N <- 30
  end <- 5 + N - 1 
  df$avgValue <- rowMeans(df[, 5:end])
  df$sd <- apply(df[, 5:end], 1, sd)
  df$se <- df$sd / sqrt(N)
  conf.interval = 0.95
  ciMult <- qt(conf.interval/2 + .5, 29)
  df$ci <- df$se * ciMult
  df$concentration <- factor(df$concentration, 
                             levels = c("10^4", "10^5", "10^6", "all"))
  
  bar_data <- data.frame(x = seq(2.5, 37.5, by = 4),
                         color = c(rep(c("A", "B"), 4), "A"))
  
  ggplot(df, aes(x = 1:nrow(df), y = avgValue)) +
    geom_bar(data = bar_data, aes(x = x, y = 1, fill = color),
             stat = "identity", width = 4, 
             show.legend = FALSE, alpha = 0.3) +
    scale_fill_manual(values = background_color) +
    
    new_scale_color() + 
    geom_point(size = 2.5, aes(col = concentration)) +
    scale_color_manual(values = errorbar_color, 
                       labels = expression(10^4, 10^5, 10^6, "all")) +
    geom_errorbar(aes(ymin = ifelse(avgValue - ci < 0, 0, avgValue - ci), 
                      ymax = ifelse(avgValue + ci > 1, 1, avgValue + ci),
                      col = concentration),
                  width = 0.4, size = 1.2, position = position_dodge(0.9)) +
    scale_color_manual(values = errorbar_color,
                       labels = expression(10^4, 10^5, 10^6, "all")) +
    scale_y_continuous(breaks = seq(0, 1, by = 0.2), limits = c(0, 1),
                       expand = c(0, 0)) +
    scale_x_continuous(breaks = seq(2.5, 37.5, by = 4), labels = abbr) + 
  
    geom_hline(yintercept = 1, linetype = "dashed") +
    labs(title = plot_type, x = "", y = "Area Under Curve") +
    theme_pubr() + 
    labs(color = "Concentration(CFU/mL)") +
    
    theme(text = element_text(family = "sans"),
          axis.text = element_text(face = "bold", size = 17, vjust = 1),
          plot.title = element_text(hjust = 0.5, size = 20, face = "bold"),
          axis.title.y = element_text(face = "bold", size = 20),
          legend.position = 'none')
  
  plot_dir <- sprintf("plot/F3/F3_%s_%s.png", plot_type, data_type)
  ggsave(plot_dir, units = 'in', width = 8, height = 5, dpi = 1200)
}


F1_barplot <- function(df, s, c, abbr = '') {
  # This function is used to generate a bar chart of the F1 score
  # of the model under specified conditions and save it in png format.
  # This bar chart is used to compare the effects of Single and Merged
  # data sets on the model's predictive power under specified conditions.
  #  
  # Args:   
  #   df: F1 score of the model and the corresponding concentration and
  #       number of images (1 is Single, 3 is Merged) information.
  #   s: Abbreviation of species name corresponding to data.
  #   c: The data correspond to microbial concentrations.
  #   abbr: Microbial abbreviations corresponding to mapping data. 
  
  if (s == 'xBlank') {
    fill_color <- c("#8FB4D8", "#FFE0B7")
  }
  else {
    fill_color <- c("#8bb2d4", "#bbbbbb")
  }
  p <- ggplot(df, aes(x = number_of_pictures, y = F1_score, 
                      fill = number_of_pictures)) +
    geom_bar(stat = "identity", width = 0.5) +
    labs(x = "", y = "F1 Score", legend = "") +
    geom_text(aes(label = sprintf("%.3f", F1_score)),
              vjust = -1, position = position_dodge(width = 0.88), size = 7) +
    theme_bw() +
    theme(text = element_text(family = 'sans'),
          axis.text = element_text(face = "bold", size = 14),
          axis.title = element_text(face = "bold", size = 15),
          legend.position = 'none',
          panel.grid = element_blank()) +
    scale_y_continuous(limits = c(0, 1.2), breaks = seq(0, 1, by = 0.2),
                       expand = c(0, 0)) +
    scale_fill_manual(values = fill_color)
  
  image_name <- sprintf("plot/F3/F3_Dichotomies_%s_%s.png", s, c)
  ggsave(image_name, p, units = 'in', height = 4, width = 3.5, dpi = 1200)
}



# Figure 4 ------------------------------


F1_multi_barplot <- function(df, model_type) {
  # This function is used to generate F1 score barplots for models
  # under different model types (PCA+LDA tandem dimension reduction
  # model/random forest model), different data types (Single/Merged),
  # and different microbial concentrations. The resulting image is
  # saved in png format.
  #  
  # Args:   
  #   df: F1 score of the model and the corresponding concentration and
  #       number of images (1 is Single, 3 is Merged) information.
  #   model_type: The type of model, namely PCA+LDA tandem dimension
  #               reduction model (PCA+LDA) or Random forest model (RF).
  
  if (model_type == "PCA+LDA") {
    color_bar <- c("#BCE9FF", "#8ABFDA", "#5797B6", "#167094")
    }
  if (model_type == "RF") {
    color_bar <- c("#ffdbc1", "#ffbf8a", "#ffa252", "#FB8502")
    }
  
  p <- ggplot(df, mapping = aes(x = number_of_pictures, y = F1_score,
                             fill = concentration)) +
    geom_bar(stat = "identity", position = position_dodge(0.85)) +
    geom_text(aes(label =  sprintf("%.3f", F1_score)), 
              vjust = -1, position = position_dodge(width = 0.88)) +
    labs(x = "", y = "F1 Score",
         fill = "Concentration(CFU/mL)") +
    scale_x_discrete(labels = c("Single", "Merged")) +
    scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, by = 0.2),
                       expand = c(0, 0)) +
    scale_fill_manual(values = color_bar,
                      label = expression(10^4, 10^5, 10^6, "all")) +
    theme(text = element_text(family = "sans"),
          legend.text = element_text(face = "bold", size = 14),
          legend.title = element_text(face = "bold", size = 14),
          legend.position = "top",
          axis.text = element_text(face = "bold", size = 14),   
          axis.title.y = element_text(face = "bold", size = 15),
          panel.border = element_blank(),
          panel.background = element_blank(),
          axis.line = element_line(colour = "black"))
  
  image_name <- sprintf("plot/F4/F4_f1_barplot_%s.png", model_type)
  ggsave(image_name, p, units = "in", height = 4, width = 6, dpi = 1200)
}



# Figure 5 ------------------------------


F1_Hierarchical_barplot <- function(data) {
  # This function is used to generate an F1 score comparison bar for
  # hierarchical classification and Merged data. A model containing a
  # combination of model types (PCA+LDA tandem dimension reduction
  # model/random forest model) and data types (Merged/Hierarchical).
  # The resulting image is saved in png format.
  #  
  # Args:   
  #   data: A dataframe containing model type (PCA+LDA tandem dimension
  #   Reduction Model (PCA+LDA)/ Random Forest Model (RF)), data
  #   type (Merged/Hierarchical), microbial concentration, and F1
  #   score.
  
  color = c("#136784", "#269EBC", "#FB8502", "#FFB702")
  group_level <- c("PCA+LDA, Merged", "PCA+LDA, Hierarchical",
                   "RF, Merged", "RF, Hierarchical")
  
  p <- ggplot(data, mapping = aes(x = concentration, y = F1,
                                  fill = group)) +
    geom_bar(stat = "identity", position = position_dodge(0.9)) +
    geom_text(aes(label =  sprintf("%.3f", F1), fontface = "bold"), 
              size = 4.5,
              vjust = -1, position = position_dodge(width = 0.9)) +
    labs(x = "Concentration(CFU/mL)", y = "F1 Score",
         fill = "Model Type") +
    scale_x_discrete(labels = expression(10^4, 10^5, 10^6, "all")) +
    scale_fill_manual(values = color) +
    scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, by = 0.2),
                       expand = c(0, 0)) +
  
    theme(text = element_text(family = 'sans'),
          legend.title = element_text(face = 'bold',size = 13),
          legend.text = element_text(face = 'bold', size = 13),
          legend.position = "bottom",
          axis.text.y = element_text(face = "bold", size = 18), 
          axis.text.x = element_text(face = "bold", size = 20),
          axis.title = element_text(face = "bold", size = 19),
          axis.line = element_line(colour = "black"),
          panel.border = element_blank(),
          panel.background = element_blank())
    
    
  ggsave("plot/F5/F5_Hierarchical_barplot.png", p, units = "in",
         height = 6, width = 10, dpi = 1200)
}



# Figure S2 ------------------------------

require(ggplot2)
set_theme <- theme(
  text = element_text(face = "bold", family = 'sans'),
  legend.title = element_blank(),
  axis.text = element_text(size = 14),
  axis.title.y = element_text(size = 15),
  legend.text = element_text(size = 10),
  panel.grid = element_blank(),
  strip.text.x = element_text(size = 10)
)


size_comparison_histogram <- function(df) {
  # This function is used to generate the particle size histogram of
  # AuNPs complexes after interaction with different concentrations of
  # microorganisms.
  #  
  # Args:   
  #   df: Data table with particle size, zeta potential, and maximum
  #       absorption peak.

  p <- ggplot(df, aes(x = Concentration, y = Size, fill = Species)) +
    facet_wrap("~ AuNPs_Type", labeller = label_parsed) +
    labs(x = '', y = 'hydrated particle size (nm)') +
    geom_bar(stat = "identity", position = position_dodge(0.85)) +
    scale_x_discrete(labels = expression(10^4, 10^5, 10^6)) +
    scale_fill_manual(values = color_scale) +
    scale_y_continuous(expand = c(0, 0), limits = c(0, 10000)) +
    theme_bw() +
    set_theme
  ggsave("plot/FS2/FS2_Size_plot.png", p, units = "in", width = 10,
         height = 5, dpi = 1200)
}


zeta_comparison_histogram <- function(df) {
  # This function is used to generate zeta potential histogram of
  # AuNPs complex after interaction with different concentrations
  # of microorganisms.The zeta potential corresponding to AuNPs 
  # FTFPA is shaded in gray.
  #  
  # Args:   
  #   df: Data table with particle size, zeta potential, and maximum
  #       absorption peak.
  
  rect_data <- data.frame(
    mean = c(-22.933, -35.367, -9.413),
    sd = c(3.814, 3.202, 0.466),
    AuNPs_Type = unique(df$AuNPs_Type)
  )
  
  p <- ggplot(df) +
    facet_wrap(~AuNPs_Type, labeller = label_parsed) +
    labs(x = '', y = 'Zeta Potential (mV)') +
    scale_x_discrete(labels = parse(text = unique(df$Concentration))) +
    # draw shaded areas.
    geom_rect(data = rect_data,
              aes(xmin = -Inf, xmax = Inf, ymin = mean - sd, 
                  ymax = mean + sd, fill = AuNPs_Type,
                  alpha = 0.2),
              show.legend = F) +
    scale_fill_manual(values = c(rep("grey", 3))) +
    # draw bar chart.
    new_scale("fill") +
    geom_bar(aes(x = Concentration, y = Zeta_potential, fill = Species),
             stat = "identity", position = position_dodge(0.85)) +
    geom_hline(yintercept = 0, linetype = "dashed") +
    scale_fill_manual(values = color_scale) +
    theme_bw() +
    set_theme
  p
  ggsave("plot/FS2/FS2_Zeta_plot.png", p, units = "in", width = 10,
         height = 5, dpi = 1200)
}


wavelength_comparison_histogram <- function(df) {
  # This function is used to generate a histogram of the maximum
  # absorption wavelength of AuNPs complex after interaction with
  # different concentrations of microorganisms. Error bar with
  # wavelength peak standard deviation. The maximum absorption
  # wavelength corresponding to AuNPs FTFPA is shaded in gray.
  #  
  # Args:   
  #   df: Data table with particle size, zeta potential, and maximum
  #       absorption peak.
  
  rect_data <- data.frame(
    mean = c(520, 531, 565),
    sd = c(1, 1, 1),
    AuNPs_Type = unique(df$AuNPs_Type)
  )
  
  p <- ggplot(df) +
    facet_wrap("~ AuNPs_Type", labeller = label_parsed) +
    labs(x = '', y = 'Maximum absorption wavelength (nm)') +
    scale_x_discrete(labels = parse(text = unique(df$Concentration))) +
    # Draw shaded areas.
    geom_rect(data = rect_data,
              aes(xmin = -Inf, xmax = Inf, ymin = mean - sd, 
                  ymax = mean + sd, fill = AuNPs_Type,
                  alpha = 0.2),
              show.legend = F) +
    scale_fill_manual(values = c(rep("grey", 3))) +
    # Draw error bar and bar chart.
    new_scale("fill") +
    geom_errorbar(aes(x = Concentration, y = Wavelength_avg,
                      fill = Species, 
                      ymin = Wavelength_avg - Wavelength_sd,
                      ymax = Wavelength_avg + Wavelength_sd),
                      width = 0.35,
                      position = position_dodge(0.85)) +
    geom_bar(aes(x = Concentration, y = Wavelength_avg, fill = Species),
             stat = "identity", position = position_dodge(0.85)) +
    scale_fill_manual(values = color_scale) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.01), add = c(-500, 0))) +
    theme_bw() +
    set_theme
  ggsave("plot/FS2/FS2_Wavelength_plot.png", p, units = "in", width = 10,
         height = 5, dpi = 1200)
}



# Figure S5 ------------------------------


bubble_plot <- function(data, data_type){
  # This function is used to plot bubble plots for the binary
  # classification models Precision and Recall. And output in
  # png format.
  #  
  # Args:   
  #   data: Data used to generate bubble maps.
  #   data_type: Type of data. Including Single and Merged.
  
  p <- ggplot(data, aes(x = rep(1:9, each = 4), y = rep(c(1, 2, 3, 4), 9))) +
    geom_point(aes(size = Precision_score, color = Recall)) +
    geom_text(aes(label = sprintf("%.3f", Recall)), vjust = 2.8) +
    geom_text(aes(label = sprintf("%.3f", Precision_score)), vjust = 4.8) +
    scale_x_continuous(breaks = seq(1, 9, by = 1), labels = abbr) +
    scale_color_gradient(name = "Recall",
                         low = "lightblue", high = "darkblue",
                         limits = c(0.5, 1),
                         breaks = c(0.50, 0.75, 1.00)) +
    scale_size_continuous(name = "Precision",
                          range = c(2, 10),
                          limits = c(0.5, 1.0),
                          breaks = seq(from = 0.5, to = 1, by = 0.1)) +
    scale_y_continuous(breaks = seq(1, 4, by = 1),
                       limits = c(0.4, 4.2),
                       label = expression(10^4, 10^5, 10^6, "all")) +
    labs(title = data_type, y = "Concentration(CFU/mL)") +
    theme_bw() +
    theme(text = element_text(family = "sans"),
          title = element_text(face = "bold", size = 20),
          axis.title.x = element_blank(),
          axis.text = element_text(face = "bold", size = 14),
          axis.title.y = element_text(face = "bold", size = 15),
          legend.title = element_text(face = "bold", size = 14),
          panel.grid.major = element_line(size = 1),
          panel.grid.minor = element_blank())
  
  plot_name <- sprintf("plot/FS5/FS5_Bubble_Plot_%s.png", data_type)
  ggsave(plot_name, p, units = 'in', width = 10, height = 5, dpi = 1200)
}



# Figure S6 ------------------------------


GLH_heatmap <- function(data) {
  # This function is used to draw the heat map form of a grayscale
  # histogram, returning a heat map without labels and color bars.
  #  
  # Args:   
  #   data: Grayscale histogram data used to draw heat maps.
  # 
  # Returns:  
  #   A ggplot class data containing a heat map without labels and
  #   color bars.
  
  bk <- seq(from = 0, to = 0.66, length.out = 101)
  colors <- colorRampPalette(colors = c("#FFEA9B", "#E92A1F"))(length(bk) - 1)
  p <- pheatmap(data,
                color = colors,
                breaks = bk,
                cluster_rows = F, cluster_cols = F,
                border = F,
                border_color = NA,
                show_colnames = F, show_rownames = F, legend = F)
  return(p)
}


upper_label <- function() {
  # This function is used to plot data annotations at the top of 
  # the grayscale histogram, including AuNPs types and microbial
  # concentrations corresponding to the data.
  #
  # Returns:  
  #   A ggplot class data containing data annotations at the top
  #   of the grayscale histogram.
  
  # Draws data corresponding to the AuNPs type comment box.
  data_top <- data.frame(
    xmin = c(0, 3, 6),
    xmax = c(3, 6, 9),
    ymin = rep(0.5, 3),
    ymax = rep(1, 3),
    text = c("AuNPs1", "AuNPs2", "AuNPs3")
  )
  
  # Draws data corresponding to the microbial concentration comment box.
  data_bottom <- data.frame(
    xmin = 0:8,
    xmax = 1:9,
    ymin = rep(0, 9),
    ymax = rep(0.5, 9),
    text = rep(c("10^4", "10^5", "10^6"), 3)
  )
  
  data_line <- data.frame(
    xstart = 0.1 + (0:2) * 3,
    xend = 2.9 + (0:2) * 3
  )
  
  rectangle <- ggplot() +
    # Draw the comment box for the AuNPs type.
    geom_rect(data = data_bottom, 
              aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), 
              fill = "white", color = "white", linewidth = 2) +
    geom_text(data = data_bottom,
              aes(x = (xmin + xmax) / 2, y = (ymin + ymax) / 2, label = text), 
              parse = TRUE, size = 6) +
    
    # Draw the comment box for the microbial concentration.
    geom_rect(data = data_top, 
              aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), 
              fill = "white", color = "white", linewidth = 2) +
    geom_text(data = data_top, 
              aes(x = (xmin + xmax) / 2, y = (ymin + ymax) / 2, label = text), 
              parse = TRUE, size = 8) +
    geom_segment(data = data_line, 
                 aes(x = xstart, xend = xend, y = 0.5, yend = 0.5),
                 size = 1.5, color = "black") +
    scale_x_continuous(expand = c(0, 0)) +
    scale_y_continuous(expand = c(0, 0)) +
    theme_void() 

  return (rectangle)
}


left_label <- function() {
  # This function is used to plot annotated information about
  # microbial species on the left side of the grayscale histogram
  # heat map.
  # 
  # Returns:  
  #   A ggplot class data containing annotated information about
  #   microbial species on the left side of the grayscale histogram
  #   heat map.
  
  s <- c("", abbr, "Control")
  data <- data.frame(
    xmin = rep(0, 11),
    xmax = rep(2, 11),
    ymin = c(1.5 + (9:0) * 3, 0),
    ymax = c(33.5, 1.5 + (9:0) * 3), s)
  label_p <- ggplot(data) +
    geom_rect(aes(xmin = xmin, xmax = xmax,
                  ymin = ymin, ymax = ymax), fill = "white") +
    geom_text(aes(x = 1.8, y = (ymin + ymax) / 2, label = s),
              size = 8, hjust = 1) +
    scale_x_continuous(expand = c(0, 0)) +
    scale_y_continuous(expand = c(0, 0)) +
    theme_void()
  return (label_p)
}


# Figure S7-S8 ------------------------------


main_plot <- function(df, LDA, label, color){
  # This function is used to generate a scatter plot based on
  # a tandem dimension reduction model of PCA and LDA and
  # displays LD1 and LD2. The resulting image will return the
  # upper level function used to concatenate the final image.
  #  
  # Args:   
  #   df: A dataframe containing the label (organized 0-9),
  #       the horizontal and vertical coordinates of the scatter,
  #       and the data type label (containing the data type and
  #`      microbial concentration).
  #   LDA: The proportion of data contained in the LD1 and LD2 
  #         directions.
  #   label: Data labels vary according to data types.
  #   color: Drawing color, different data types correspond to
  #           different drawing colors.
  # 
  # Returns:  
  #   A ggplot class data containing a plotted scatter plot and
  #   a confidence ellipse with a level = 0.9.
  
  p_main <- ggplot(data = df, aes(x, y, col = label)) + 
    geom_point(size = 1.5) +
    labs(x = sprintf("LD1(%.1f%%)", LDA[1]),
         y = sprintf("LD2(%.1f%%)", LDA[2])) +
    scale_color_manual(name = NULL,
                       labels = label,
                       values = color) +
    theme_bw() +
    theme(text = element_text(family = 'sans'),
          panel.grid = element_blank(),
          axis.text = element_text(face = "bold", size = 30),
          axis.title = element_text(face = "bold", size = 30),
          panel.border = element_rect(color = "black", fill = NA, size = 2))
  
  p_main <- p_main + stat_ellipse(data = df, geom = "polygon", level = 0.9,
                                  linetype = 1, size = 0.8, aes(fill = label),
                                  alpha = 0.1, show.legend = F) +
    scale_fill_manual(values = color)+
    theme(legend.position = "none")
  return(p_main)
}


side_view <- function(df, color, axis_type){
  # This function is used to plot the axial density distribution
  # of scatter plots. The horizontal and vertical axes of the LDA
  # scatter plot are plotted separately. Finally, the density plot
  # is returned to the upper level function and combined with the
  # LDA scatter plot.
  #  
  # Args:   
  #   df: A dataframe containing the label (organized 0-9),
  #       the horizontal and vertical coordinates of the scatter,
  #       and the data type label (containing the data type and
  #`      microbial concentration).
  #   color: Drawing color, different data types correspond to
  #           different drawing colors.
  #   axis_type: The axis of the density map. 1 is the horizontal
  #               axis, 2 is the vertical axis.
  # 
  # Returns:  
  #   The generated ggplot object.
  
  df_1 <- df[, c(1, axis_type + 1)]
  colnames(df_1) <- c("label", "x")
  
  p_side <- ggplot(data = df_1, aes(x = x, fill = label, alpha = 0.1)) +
    geom_density(colour = "white") +
    scale_color_manual(values = color) +
    scale_fill_manual(values = color) +
    theme_pubr() +
    theme(axis.text = element_blank(),
          axis.title = element_blank(),
          axis.ticks = element_blank(),
          axis.line = element_blank(),
          legend.position = "none")
  if (axis_type == 1){
    p_side <- p_side + theme(plot.margin = margin(0, -0.1, 0, 1, 'in'))
  }
  
  if (axis_type == 2){
    p_side <- p_side + coord_flip() +
      theme(plot.margin = margin(-0.1, 0, 0.7, 0, "in"))
  }
  return(p_side)
}


scatter_plot <- function(df, LDA, t, c) {
  # This function is used to draw an LDA scatter plot and an axial
  # density plot, combine them, and finally output them in png format.
  #  
  # Args:   
  #   df: A dataframe containing the label (organized 0-9),
  #       the horizontal and vertical coordinates of the scatter,
  #       and the data type label (containing the data type and
  #`      microbial concentration).
  #   LDA: The proportion of data contained in the LD1 and LD2 
  #         directions.
  #   t: Type of model, including single\merged\order\Bacillales\Enterobacteriales.
  #   c: The concentration corresponding to the data.
  
  load("RData/FigureS7-8_variable.RData")
  
  lda_value <- c(LDA[, 3] * 100, LDA[, 4] * 100)

  if (t == "single" || t == "merged") {
    label <- abbr
    if (c == "all") {
      label = c(abbr, "Control")
    }
    color <- LDA_color
  }
  if (t == "order") {
    label <- order_label
    color <- order_color
  }
  if (t == "Bacillales") {
    label <- Bacillales_label
    color <- Bacillales_color
  }
  if (t == "Enterobacteriales") {
    label <- Enterobacteriales_label
    color <- Enterobacteriales_color
  }
  
  p_main <- main_plot(df, lda_value, label, color)
  p_x <- side_view(df, color, 1)
  p_y <- side_view(df, color, 2)
  
  p <- grid.arrange(p_x, p_main, p_y, ncol = 2, nrow = 2,
                    layout_matrix = rbind(c(1, NA), c(2, 3)),
                    heights = c(0.5, 4), widths = c(4, 0.5))
  
  imagename = sprintf("plot/FS7-8/FS7-8_%s_%s.png", t, c)
  ggsave(imagename, p, units = "in", height = 6, width = 7.5, dpi = 1200)
}


