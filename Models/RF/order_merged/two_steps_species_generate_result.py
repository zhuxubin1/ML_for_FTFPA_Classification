import os
import sys

import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import read_img, insert_into_table, load_model
from Utils.names import *

ROOT = f"{FILE_ROOT}/Data"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
IDENTIFIER = "order_merged"

if __name__ == "__main__":
    for order in ["Enterobacteriales", "Bacillales"]:
        for concentration in ["10^4", "10^5", "10^6", "all"]:
            # read images and labels from filesv
            X_train, y_train = read_img(f"{ROOT}/split_in_{order}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/split_in_{order}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/split_in_{order}/train")
            if concentration != "all":
                labels.remove("xBlank")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print(X_train.shape)
            print(y_test.shape)

            model_rf = load_model(f"{MODEL}/{IDENTIFIER}_{order}_{concentration}.pkl")

            # confusion matrix
            y_pred = model_rf.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds, text_size=40,
                              output=f"{IMAGE}/{IDENTIFIER}_{order}_{concentration}.png")

            # # model metrics
            # accuracy = accuracy_score(y_test, y_pred)
            # cv = StratifiedKFold(n_splits=30)
            # scores = cross_val_score(model_rf, X_test, y_test, scoring='accuracy', n_jobs=10, cv=cv)
            # Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
            # data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision_score] + list(scores)
            # insert_into_table(data, f"{TABLE}/accuracy.xlsx")
