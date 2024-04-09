import glob
import json
import os
import pickle

import cv2
import numpy as np
import pandas as pd


def trans_to_single_glh(img, feature_num=225):
    """
    It is used to extract the grayscale histogram of the image and intercept the grayscale range
    of 0-225 as a one-dimensional vector output.

    Args:
        img: Input image.
        feature_num: The number of gray values (features) for each gray histogram. The value of a
         grayscale histogram without threshold restriction is 256, and that of a grayscale histogram
          with threshold restriction is 225. The default value is 225.

    Returns:
        A one-dimensional vector of a grayscale histogram with grayscale values in the range 0-225.
    """

    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist = hist[:feature_num, ]
    return hist.ravel()


def trans_to_merged_glh(img, feature_num=225):
    """
    It is used to extract the gray histogram of the three-channel image (each channel stores an
    AuNPs gray image), and intercepts the range of gray value 0-225 as a one-dimensional vector,
    and finally splits the three one-dimensional vectors into a one-dimensional vector according
    to the order of "AuNPs1, AuNPs2, AuNPs3".

    Args:
        img: Input three channel picture.
        feature_num: The number of gray values (features) for each gray histogram. The value of a
         grayscale histogram without threshold restriction is 256, and that of a grayscale histogram
          with threshold restriction is 225. The default value is 225.

    Returns:
        A one-dimensional vector composed of three one-dimensional vectors.
    """

    hist_list = []
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [256], [0, 255])
        hist_new = hist[:feature_num, ]
        hist_list.append(hist_new.ravel().astype(np.uint16))
    return np.hstack(hist_list)


def read_img(path, model_type, concentration="all", feature_num=225):
    """
    read images from path, return the histogram of the images and the labels

    Args:
        path: the path of folder that contains the images
        model_type: The form of data accepted by the model. It can be "Single" or "Merged".
        concentration: the concentration of the images, default is "all"
        feature_num: The number of gray values (features) for each gray histogram. The value of a
          grayscale histogram without threshold restriction is 256, and that of a grayscale histogram
          with threshold restriction is 225. The default value is 225.

    Returns:
        images: a ndarray of the histogram of the images
        labels: a ndarray of the labels of the images
    """
    images = []
    labels = []
    if model_type == "Single":
        trans = trans_to_single_glh
    else:
        trans = trans_to_merged_glh
    if concentration == "all":
        organisms = [os.path.join(path, x) for x in os.listdir(path)]
        concentration = ""
    else:
        organisms = [os.path.join(path, x) for x in os.listdir(path) if x != "xBlank"]
    for index, organism in enumerate(organisms):
        for file in glob.glob(f'{organism}/*{concentration}*.tif'):
            img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (256, 256))
            images.append(trans(img, feature_num))
            labels.append(index)
    return np.array(images), np.array(labels)


def save_model(model, path):
    """
    This function saves the model to the specified path through the dump() function of the pickle package.

    Args:
        model: The model that needs to be saved.
        path: The path to save the model.
    """
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def load_model(model_dir):
    """
    This function loads the model saved in the specified path through the load() function of
    the pickle package.

    Args:
        model_dir: The path to save the model.

    Returns:
        The model is extracted from the specified path.
    """

    with open(model_dir, 'rb') as file:
        model = pickle.load(file)
    return model


def load_param(param_dir):
    """
    This function loads the model parameters saved in the specified path through the load() function of
    the json package.

    Args:
        param_dir: The path to save the model parameters.

    Returns:
        The model parameters are extracted from the specified path.
    """
    with open(param_dir, "r") as f:
        params = json.load(f)
    return params


def create_table(table_path, column_names=None):
    """
    Create an empty Excel table to store model evaluation parameters.

    Args:
        table_path: The path to the created table. The cross_val_score() function are evaluated for
            accuracy by default.
        column_names: The column name of the table.
    """
    if os.path.exists(table_path):
        print(f"{table_path} already exists.")
        return
    if column_names is None:
        column_names = ["number_of_pictures", "diameter", "concentration", "Accuracy_score",
                        "Recall", "F1_score", "Precision_score"] + [f"Score{i}" for i in range(1, 31)]
    df = pd.DataFrame(columns=column_names)
    df.to_excel(table_path, sheet_name="Sheet1", index=False)


def insert_into_table(new_data, table_path, column_names=None, sheet="Sheet1"):
    """
    Insert evaluation parameters into the table.

    Args:
        new_data: The model evaluation parameters that need to be inserted are a fixed format list.
        table_path: The path to the inserted table.
        column_names: The column name of the table, if the table does not exist, it will be column name of new table.
        sheet: The inserted Sheet. Sheet1 is inserted by default.
    """
    if not os.path.exists(table_path):
        create_table(table_path, column_names)
    df = pd.read_excel(table_path, sheet_name=sheet, header=0, index_col=None)
    df.loc[len(df)] = new_data
    df.to_excel(table_path, sheet, index=False)
