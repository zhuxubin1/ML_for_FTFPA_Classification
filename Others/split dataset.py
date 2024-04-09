"""
This script is used to split the dataset into two parts, the train set and the test set.
"""
import glob
import os
import random
import shutil


def split(files, test_path, train_path, ratio):
    """
    split the files into two folders.

    Args:
        files: list, the files to be split.
        test_path: str, the folder to store the test set.
        train_path: str, the folder to store the train set.
        ratio: float, the ratio of the test set.
    """
    random.shuffle(files)
    num = int(len(files) * ratio)
    # copy to test folder
    for file in files[:num]:
        print(files.index(file))
        new_path = os.path.join(test_path, os.path.basename(file))
        shutil.copy(file, new_path)
    # copy to train folder
    for file in files[num:]:
        print(files.index(file))
        new_path = os.path.join(train_path, os.path.basename(file))
        shutil.copy(file, new_path)


if __name__ == '__main__':
    concentrations = ('10^4', '10^5', '10^6')
    diameter = ('5nm', '13nm', '60nm')

    root = "../Data/image_RF(imageJ)"
    train_folder = "d:/process2/split/train"
    test_folder = "d:/process2/split/test"

    folders = os.listdir(root)
    for folder in folders:
        sub_folder = os.path.join(root, folder)
        test_sub_folder = os.path.join(test_folder, folder)
        train_sub_folder = os.path.join(train_folder, folder)
        os.makedirs(test_sub_folder, exist_ok=True)
        os.makedirs(train_sub_folder, exist_ok=True)

        if folder == "Blank":
            for d in diameter:
                files = glob.glob(f"{sub_folder}/*{d}*.tif")
                split(files, test_sub_folder, train_sub_folder, 0.2)

        else:
            for c in concentrations:
                for d in diameter:
                    files = glob.glob(f"{sub_folder}/*{d}*{c}*.tif")
                    split(files, test_sub_folder, train_sub_folder, 0.2)
