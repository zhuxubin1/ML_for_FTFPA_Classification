import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def confusionPainting(y_test, y_pred, labels, cmap, rotation=0,
                      text_size=None, tick_fontsize=None, label_fontsize=None,
                      output=None):
    """
    Calculate and draw the heat map of the confusion matrix, and save the heat map to the
    specified path.

    Args:
        y_test: Real label of data.
        y_pred: The label of the data predicted by the model.
        labels: Abbreviations for individual microbes in the data set. Used as a label when drawing
         a heat map of the confusion matrix.
        cmap: The color palette of the heat map.
        rotation: The rotation Angle of the horizontal axis label in the heat map, the default is 0
        text_size: The font size of the text in the heat map, the default is None.
        output: A path to save the confusion matrix heat map.
    """
    plt.rc('font', family='Arial')
    size = (3.2 * len(labels), 2.4 * len(labels))
    fig, ax = plt.subplots(figsize=size)
    cm_test = confusion_matrix(y_test, y_pred)
    print(f"cm_test.shape: {cm_test.shape}")
    cm_test = cm_test / cm_test.sum(axis=1)[:, np.newaxis]
    cm_test = np.round(cm_test, decimals=2)

    disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=labels)
    if text_size is None:
        text_size = 42 + 1.5 * len(labels)
    if tick_fontsize is None:
        tick_fontsize = 27 + 1.5 * len(labels)
    if label_fontsize is None:
        label_fontsize = 33 + 2 * len(labels)
    disp_test.plot(ax=ax, cmap=cmap, colorbar=False, text_kw={"size": text_size},
                   im_kw={"vmin": 0, "vmax": 1})
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()
    if rotation != 0:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotation, ha='right')
    else:
        plt.setp(ax.xaxis.get_majorticklabels(), ha='center')
    ax.set_xticklabels(labels, fontsize=tick_fontsize, fontweight='bold')
    ax.set_yticklabels(labels, fontsize=tick_fontsize, fontweight='bold')
    ax.set_xlabel("Predicted labels", fontsize=label_fontsize)
    ax.set_ylabel("True labels", fontsize=label_fontsize)
    if output is not None:
        plt.savefig(output, dpi=600, bbox_inches='tight')
    plt.close()


def scatter(y_true, X, output):
    """
    Save the scatter plot data to a csv file, the format is: y_true, X[:, 0], X[:, 1]

    Args:
        y_true: true labels
        X: features
        output: output file path
    """
    df = pd.DataFrame(np.column_stack((y_true, X[:, 0], X[:, 1])))
    df.to_csv(output, index=False, header=False)
