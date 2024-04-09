import numpy as np
from matplotlib import pyplot as plt
from sklearn.pipeline import Pipeline

from Utils.display import confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import load_model, read_img, insert_into_table
from Utils.names import *

ROOT = "../../../Data/three_channel_combine"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
IDENTIFIER = "order_merged"

orders = ["Bacillales", "Enterobacteriales", "E.faecalis", "S.cerevisiae", "xBlank"]

order_to_species = {
    "Bacillales": ["B.licheniformis", "L.monocytogenes", "S.aureus"] + ["xBlank"],
    "Enterobacteriales": ["E.cloacae", "E.coli", "S.enterica", "S.marcescens", ] + ["xBlank"],
    "Lactobacillales": ["E.faecalis"] + ["xBlank"],
    "Saccharomycetales": ["S.cerevisiae"] + ["xBlank"],
    "xBlank": ["xBlank"]
}


class CustomPipeline(Pipeline):
    index_to_order = np.vectorize(lambda x: orders[x])
    index_to_Bacillales = np.vectorize(lambda x: order_to_species["Bacillales"][x])
    index_to_Enterobacteriales = np.vectorize(lambda x: order_to_species["Enterobacteriales"][x])

    def predict(self, X, **predict_params):
        y_pred = self.named_steps["order"].predict(X)
        y_pred = self.index_to_order(y_pred)

        index_B = np.where(y_pred == "Bacillales")
        y_pred_B = self.named_steps["Bacillales"].predict(X[index_B])
        y_pred_B = self.index_to_Bacillales(y_pred_B)
        y_pred[index_B] = y_pred_B

        index_E = np.where(y_pred == "Enterobacteriales")
        y_pred_E = self.named_steps["Enterobacteriales"].predict(X_test[index_E])
        y_pred_E = self.index_to_Enterobacteriales(y_pred_E)
        y_pred[index_E] = y_pred_E

        return y_pred


if __name__ == "__main__":
    for concentration in ["10^4", "10^5", "10^6", "all"]:
        # read images and labels from files
        X_test, y_test = read_img(f"{ROOT}/test", "Merged", concentration=concentration)
        print("X_test:", X_test.shape)
        labels = ORGANISMS if concentration != "all" else ORGANISMS_WITH_BLANK
        labels = [name_to_abbr.get(x, x) for x in labels]

        index_to_truelabel = np.vectorize(lambda x: ORGANISMS_WITH_BLANK[x])
        y_test = index_to_truelabel(y_test)

        # load model
        model_order = load_model(f"{MODEL}/{IDENTIFIER}_{concentration}.pkl")
        model_Bacillales = load_model(f"{MODEL}/{IDENTIFIER}_Bacillales_{concentration}.pkl")
        model_Enterobacteriales = load_model(f"{MODEL}/{IDENTIFIER}_Enterobacteriales_{concentration}.pkl")

        pipeline = CustomPipeline([
            ("order", model_order),
            ("Bacillales", model_Bacillales),
            ("Enterobacteriales", model_Enterobacteriales)
        ])

        # confusion matrix
        y_pred = pipeline.predict(X_test)
        confusionPainting(y_test, y_pred, labels, plt.cm.Reds, output=f"{IMAGE}/{IDENTIFIER}_{concentration}.png")

        # # model metrics
        # Accuracy, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
        # insert_into_table([concentration, Accuracy, Recall, F1_score, Precision_score],
        #                   f"{TABLE}/{IDENTIFIER}_Accuracy.xlsx",
        #                   column_names=["concentration", "Accuracy", "Recall", "F1", "Precision"])
