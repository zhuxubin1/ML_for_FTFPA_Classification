import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.display import scatter, confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import read_img, insert_into_table, load_model
from Utils.names import *

ROOT = f"{FILE_ROOT}/Data"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
SCATTER = "./scatter"
VARIANCE = "./variance"
IDENTIFIER = "order_merged"

if __name__ == "__main__":
    for order in ["Bacillales", "Enterobacteriales"]:
        for concentration in ["10^4", "10^6", "10^5", "all"]:
            # read images and labels from files
            X_train, y_train = read_img(f"{ROOT}/split_in_{order}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/split_in_{order}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/split_in_{order}/train")
            if concentration != "all":
                labels.remove("xBlank")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print("X_train:", X_train.shape, "\n" + "X_test:", X_test.shape)

            best_model = load_model(f"{MODEL}/{IDENTIFIER}_{order}_{concentration}.pkl")

            # confusion matrix
            y_pred = best_model.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds,
                              output=f"{IMAGE}/{IDENTIFIER}_{order}_{concentration}.png")

            # # LDA scatter
            # X = np.concatenate((X_train, X_test))
            # y = np.concatenate((y_train, y_test))
            # X = best_model.transform(X)
            # scatter(y, X, output=f"{SCATTER}/{IDENTIFIER}_{order}_{concentration}.csv")
            #
            # # LDA variance
            # with open(f"{VARIANCE}/{IDENTIFIER}_{order}.txt", "a") as f:
            #     v = best_model.named_steps["lda"].explained_variance_ratio_
            #     f.write(f"{IDENTIFIER}_{order}_{concentration}\t{v[0]}\t{v[1]}\n")
            #
            # # model metrics
            # Accuracy, Recall, F1_score, Precision = model_metrics(y_test, y_pred)
            # cv = StratifiedKFold(n_splits=30)
            # scores = cross_val_score(best_model, X_test, y_test, scoring='accuracy', n_jobs=-1, cv=cv)
            # data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision] + list(scores)
            # insert_into_table(data, f"{TABLE}/{IDENTIFIER}_{order}_Accuracy.xlsx")
