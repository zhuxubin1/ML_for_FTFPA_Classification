import os
import sys

from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, StratifiedKFold

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.names import name_to_abbr

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.io import read_img, save_model, load_param, insert_into_table

ROOT = f"{FILE_ROOT}/Data/"
IMAGE = "./image"
MODEL = "./model"
PARAMS = "./params"
TABLE = "./table"
IDENTIFIER = "order_merged"

if __name__ == "__main__":
    for order in ["Bacillales", "Enterobacteriales"]:
        for concentration in ["10^4", "10^5", "10^6", "all"]:
            # read images and labels from files
            X_train, y_train = read_img(f"{ROOT}/split_in_{order}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/split_in_{order}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/split_in_{order}/train")
            if concentration != "all":
                labels.remove("xBlank")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print(X_train.shape)
            print(y_test.shape)

            # model training
            param = load_param(f"{PARAMS}/{IDENTIFIER}_{order}_{concentration}.json")
            model = RandomForestClassifier(**param)
            model.fit(X_train, y_train)
            save_model(model, f"{MODEL}/{IDENTIFIER}_{order}_{concentration}.pkl")
            
            # confusion matrix
            y_pred = model.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds, text_size=40,
                              output=f"{IMAGE}/{IDENTIFIER}_{order}_{concentration}.png")

            # model metrics
            accuracy = accuracy_score(y_test, y_pred)
            cv = StratifiedKFold(n_splits=30)
            scores = cross_val_score(model, X_test, y_test, scoring='accuracy', n_jobs=10, cv=cv)
            Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
            data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision_score] + list(scores)
            insert_into_table(data, f"{TABLE}/accuracy.xlsx")
