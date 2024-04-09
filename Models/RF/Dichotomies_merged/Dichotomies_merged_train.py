import os
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.names import ORGANISMS, name_to_abbr

FILE_ROOT = os.path.abspath(__file__).split("Models")[0]
sys.path.append(FILE_ROOT)

from Utils.io import read_img, save_model, load_param, insert_into_table

ROOT = f"{FILE_ROOT}/Data/split_Dichotomies_merged"
IMAGE = "./image"
MODEL = "./model"
PARAMS = "./params"
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
            X_train, y_train = read_img(f"{ROOT}/{organism}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/{organism}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/{organism}/train")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print(X_train.shape)
            print(y_test.shape)

            # model training
            param = load_param(f"{PARAMS}/{IDENTIFIER}_{organism}_{concentration}.json")
            model = RandomForestClassifier(**param)
            model.fit(X_train, y_train)
            save_model(model, f"{MODEL}/{IDENTIFIER}_{organism}_{concentration}.pkl")

            # confusion matrix
            y_pred = model.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds,
                              output=f"{IMAGE}/{IDENTIFIER}_{organism}_{concentration}.png")

            # model metrics
            Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
            cv = StratifiedKFold(n_splits=30)
            scores = cross_val_score(model, X_test, y_test, scoring='accuracy', n_jobs=10, cv=cv)
            data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision_score] + list(scores)
            insert_into_table(data, f"{TABLE}/{organism}_accuracy.xlsx")
