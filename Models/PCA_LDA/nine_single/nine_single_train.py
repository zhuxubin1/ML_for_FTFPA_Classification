import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.display import confusionPainting, scatter
from Utils.evaluate import model_metrics
from Utils.io import save_model, read_img, insert_into_table, load_param
from Utils.names import *

ROOT = f"{FILE_ROOT}/Data/split"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
SCATTER = "./scatter"
VARIANCE = "./variance"
IDENTIFIER = "nine_single"

if __name__ == "__main__":
    for concentration in ["10^4", "10^5", "10^6", "all"]:
        # read images and labels from files
        X_train, y_train = read_img(f"{ROOT}/train", "Single", concentration=concentration)
        X_test, y_test = read_img(f"{ROOT}/test", "Single", concentration=concentration)
        labels = os.listdir(f"{ROOT}/train")
        if concentration != "all":
            labels.remove("xBlank")
        labels = [name_to_abbr.get(x, x) for x in labels]
        print("X_train:", X_train.shape, "\n" + "X_test:", X_test.shape)

        # model training
        pca = load_param(f"{MODEL}/{IDENTIFIER}_{concentration}_pca.json")
        lda = load_param(f"{MODEL}/{IDENTIFIER}_{concentration}_lda.json")
        pipeline = Pipeline([
            ('pca', KernelPCA(**pca)),
            ('lda', LinearDiscriminantAnalysis(**lda))
        ])
        pipeline.fit(X_train, y_train)
        save_model(pipeline, f"{MODEL}/{IDENTIFIER}_{concentration}.pkl")

        # confusion matrix
        y_pred = pipeline.predict(X_test)
        confusionPainting(y_pred, y_test, labels, plt.cm.Reds, output=f"{IMAGE}/{IDENTIFIER}_{concentration}.png")

        # LDA scatter
        X = np.concatenate((X_train, X_test))
        y = np.concatenate((y_train, y_test))
        X = pipeline.transform(X)
        scatter(y, X, output=f"{SCATTER}/{IDENTIFIER}_{concentration}.csv")

        # LDA variance
        with open(f"{VARIANCE}/{IDENTIFIER}.txt", "a") as f:
            v = pipeline.named_steps["lda"].explained_variance_ratio_
            f.write(f"{IDENTIFIER}_{concentration}\t{v[0]}\t{v[1]}\n")

        # model metrics
        Accuracy_score, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
        cv = StratifiedKFold(n_splits=30)
        scores = cross_val_score(pipeline, X_test, y_test, scoring='accuracy', n_jobs=-1, cv=cv)
        data = [3, 3, concentration, Accuracy_score, Recall, F1_score, Precision_score] + list(scores)
        insert_into_table(data, f"{TABLE}/{IDENTIFIER}_Accuracy.xlsx")
