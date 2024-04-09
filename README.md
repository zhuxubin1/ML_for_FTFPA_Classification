# Machine Learning for Microbe Identification

In this project, we tried to classify the threshold gray histogram of the freeze-thaw feature patterns of AuNPs and 9 microorganisms through machine learning methods (including the tandem dimensionality reduction model of PCA and LDA and the random forest model), so as to achieve effective identification of microorganisms in tasks such as binary classification, multi-classification and hierarchical classification.

## Table of Contents

- [Organization](#organization)
- [Software requirement](#software-requirement)
- [Running sample](#running-sample)
- [Expected Output](#expected-output)

## Organization

* _**Models**_ contains python scripts for training and testing the model.
* _**Data**_ contains the dataset for training and testing the model.
* _**Others**_ contains python scripts for image preprocessing.
* _**Utils**_ contains functions for data preprocessing and result visualization.
* _**r_script**_ contains R scripts for result visualization.

## Software requirement

  * R version: 4.2.3
  * A list of some required R packages version:
    * readxl 1.4.3
    * dplyr 1.0.10
    * stringi 1.7.8
    * ggplot2 3.3.6
    * ROCR 1.0.11
    * pROC 1.18.4
    * ggpubr 0.4.0
    * ggnewscale 0.4.9
    * tidyverse 1.3.2
    * gridExtra 2.3
    * ggfortify 0.4.16
    * openxlsx 4.2.5.2
    * forcats 0.5.2
    * stringr 1.5.0
    * purrr 0.3.4
    * readr 2.1.2
    * tidyr 1.2.1
    * tibble 3.1.8
  * Python version: 3.10
  * A list of some required Python library versions:
    * opencv-python~=4.8.1.78
    * numpy~=1.26.0
    * pandas~=2.1.1
    * matplotlib~=3.8.2
    * scikit-learn~=1.3.2
    * scipy~=1.11.3
    * pyqtgraph~=0.13.3
    * PyQt6~=6.5.2

## Running sample

### 1. Clone the repository.

```commandline
git clone https://github.com/zhuxubin1/machine_learning_for_microbe_identification
cd machine_learning_for_microbe_identification
```

### 2. Run xx_train.py to train the model and generate the result, or run xx_generate_result.py to generate the result directly.

```commandline
python Models/PCA_LDA/nine_merged/nine_merged_train.py
```
```commandline
python Models/PCA_LDA/nine_merged/nine_merged_generate_result.py
```

## Expected Output
- Pickle file of the trained model.
- Heatmap of the confusion matrix.
- Table of model performance in cross-validation.
- Table of two-dimensional LDA variance. (Only for PCA_LDA model)
- Table of two-dimensional data after PCA. (Only for PCA_LDA model)
