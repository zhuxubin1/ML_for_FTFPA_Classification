import os
import sys

import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import insert_into_table, read_img, load_model
from Utils.names import *

ROOT = f"{FILE_ROOT}/Data/split_Dichotomies_merged/"
IMAGE = "./image"
MODEL = "./model"
TABLE = "./table"
IDENTIFIER = "Dichotomies_merged"

if __name__ == "__main__":
    for organism in ORGANISMS:
        if organism == "xBlank":
            concentrations = ["all"]
        else:
            concentrations = ["10^4", "10^5", "10^6", "all"]

        for concentration in concentrations:
            # read images and labels from files
            new_root = f"{ROOT}/{organism}"
            X_train, y_train = read_img(f"{new_root}/train", "Merged", concentration=concentration)
            X_test, y_test = read_img(f"{new_root}/test", "Merged", concentration=concentration)
            labels = os.listdir(f"{new_root}/train")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print("X_train:", X_train.shape, "\n" + "X_test:", X_test.shape)

            best_model = load_model(f"{MODEL}/{IDENTIFIER}_{organism}_{concentration}.pkl")

            # confusion matrix
            y_pred = best_model.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds, text_size=45, tick_fontsize=30, label_fontsize=36,
                              output=f"{IMAGE}/{IDENTIFIER}_{organism}_{concentration}.png")

            # model metrics
            Accuracy_score, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
            y_probs = best_model.predict_proba(X_test)[:, 1]
            AUROC = roc_auc_score(y_test, y_probs)
            AUPR = average_precision_score(y_test, y_probs)
            data = [organism, 3, 3, concentration, AUROC, AUPR, Accuracy_score, Recall, F1_score, Precision_score]
            column_names = ["target", "number_of_pictures", "diameter", "concentration", "AUROC", "AUPR",
                            "Accuracy_score", "Recall", "F1_score", "Precision_score"]
            insert_into_table(data, f"{TABLE}/{IDENTIFIER}_AUROC_AUPR.xlsx", column_names)

            # accuracy of cross validation
            cv = StratifiedKFold(n_splits=30)
            scores = cross_val_score(best_model, X_test, y_test, scoring='accuracy', n_jobs=-1, cv=cv,
                                     error_score='raise')
            data = [3, 3, concentration, Accuracy_score, Recall, F1_score, Precision_score] + list(scores)
            insert_into_table(data, f"{TABLE}/{IDENTIFIER}_{organism}_Accuracy.xlsx")

            # AUROC and AUPR of cross validation
            cv = StratifiedKFold(n_splits=30)
            auroc = list(cross_val_score(best_model, X_test, y_test, scoring='roc_auc', n_jobs=-1, cv=cv))
            aupr = list(cross_val_score(best_model, X_test, y_test, scoring='average_precision', n_jobs=-1, cv=cv))
            data_roc = [organism, 3, 3, concentration] + auroc
            data_pr = [organism, 3, 3, concentration] + aupr
            column_names = (["target", "number_of_pictures", "diameter", "concentration"] +
                            [f"Score{i}" for i in range(1, 31)])
            insert_into_table(data_roc, f"{TABLE}/{IDENTIFIER}_AUROC.xlsx", column_names)
            insert_into_table(data_pr, f"{TABLE}/{IDENTIFIER}_AUPR.xlsx", column_names)
