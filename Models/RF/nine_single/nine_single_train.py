import os
import sys

from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.names import name_to_abbr

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.io import read_img, save_model, load_param, insert_into_table

ROOT = f"{FILE_ROOT}/Data/split"
IMAGE = "./image"
MODEL = "./model"
PARAMS = "./params"
TABLE = "./table"
IDENTIFIER = "nine_single"

if __name__ == "__main__":
    for concentration in ["10^4", "10^5", "10^6", "all"]:
        # read images and labels from files
        X_train, y_train = read_img(f"{ROOT}/train", "Single", concentration)
        X_test, y_test = read_img(f"{ROOT}/test", "Single", concentration)
        labels = os.listdir(f"{ROOT}/train")
        if concentration != "all":
            labels.remove("xBlank")
        labels = [name_to_abbr.get(x, x) for x in labels]
        print(X_train.shape)
        print(y_test.shape)

        # model training
        param = load_param(f"{PARAMS}/{IDENTIFIER}_{concentration}.json")
        model = RandomForestClassifier(**param)
        model.fit(X_train, y_train)
        save_model(model, f"{MODEL}/{IDENTIFIER}_{concentration}.pkl")

        # confusion matrix
        y_pred_rf = model.predict(X_test)
        confusionPainting(y_pred_rf, y_test, labels, plt.cm.Reds,
                          output=f"{IMAGE}/{IDENTIFIER}_{concentration}.png")

        # model metrics
        Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred_rf)
        cv = StratifiedKFold(n_splits=30)
        scores = cross_val_score(model, X_test, y_test, scoring='accuracy', n_jobs=10, cv=cv)
        data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision_score] + list(scores)
        insert_into_table(data, f"{TABLE}/accuracy.xlsx")
