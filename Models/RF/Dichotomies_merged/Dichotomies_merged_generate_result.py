import os
import sys

import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import read_img, insert_into_table, load_model
from Utils.names import *

ROOT = f"{FILE_ROOT}/Data/split_Dichotomies_merged"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
IDENTIFIER = "Dichotomies_merged"

if __name__ == "__main__":
    for organism in ORGANISMS:
        for concentration in ["10^4", "10^5", "10^6", "all"]:
            # read images and labels from files
            X_train, y_train = read_img(f"{ROOT}/{organism}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/{organism}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/{organism}/train")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print("X_train: ", X_train.shape)
            print("X_test: ", y_test.shape)

            model_rf = load_model(f"{MODEL}/{IDENTIFIER}_{organism}_{concentration}.pkl")

            # confusion matrix
            y_pred = model_rf.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds,
                              output=f"{IMAGE}/{IDENTIFIER}_{organism}_{concentration}.png")

            # # model metrics
            # Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
            # cv = StratifiedKFold(n_splits=30)
            # scores = cross_val_score(model_rf, X_test, y_test, scoring='accuracy', n_jobs=10, cv=cv)
            # data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision_score] + list(scores)
            # insert_into_table(data, f"{TABLE}/{organism}_accuracy.xlsx")
