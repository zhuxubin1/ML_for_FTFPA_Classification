"""
This script is used to merge three pictures into one picture. The three pictures are corresponding to three different
diameters of nanoparticles.
"""
import glob
import os

import cv2


def combine(file_lists, output_folder, concentration, batch):
    """
    Combine three pictures into one picture, and then save it into the output folder.

    Args:
        file_lists: list containing three lists of file paths, each list contains the file paths of the same diameter of
                    pictures.
        output_folder: the folder to save the merged pictures.
        concentration: the concentration of the images.
        batch: the batch number of the images.
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    num = len(file_lists[0])
    for n in range(num):
        pics = []
        for file_list in file_lists:
            img = cv2.imread(file_list[n], cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (256, 256))
            pics.append(img)
        combination = cv2.merge(pics)
        cv2.imwrite(f"{output_folder}/{concentration}_{n + batch * num}.tif", combination)


if __name__ == '__main__':
    input_root = "../Data/split"
    output_root = "../Data/three_channel_combine/"
    concentrations = ('10^4', '10^5', '10^6')
    diameters = ('5nm', '13nm', '60nm')

    for dataset in ("train", "test"):
        if not os.path.exists(output_root):
            os.mkdir(output_root)
        input_root = os.path.join(input_root, dataset)
        output_root = os.path.join(output_root, dataset)
        typenames = os.listdir(input_root)
        for typename in typenames:
            print(typename)
            input_folder = os.path.join(input_root, typename)
            output_folder = os.path.join(output_root, typename)

            if typename == "Blank":
                d_5 = glob.glob(f"{input_folder}/*5nm*.tif")
                d_13 = glob.glob(f"{input_folder}/*13nm*.tif")
                d_60 = glob.glob(f"{input_folder}/*60nm*.tif")
                interval = len(d_5) // 3
                for i in range(3):
                    # combine, and then change the order of d_13 and d_60
                    combine((d_5, d_13, d_60), output_folder, "blank", i)
                    d_13 = d_13[interval:] + d_13[:interval]
                    d_60 = d_60[2 * interval:] + d_60[:2 * interval]

            else:
                for c in concentrations:
                    d_5 = glob.glob(f"{input_folder}/*5nm*{c}*.tif")
                    d_13 = glob.glob(f"{input_folder}/*13nm*{c}*.tif")
                    d_60 = glob.glob(f"{input_folder}/*60nm*{c}*.tif")
                    interval = len(d_5) // 3
                    for i in range(3):
                        combine((d_5, d_13, d_60), output_folder, c, i)
                        d_13 = d_13[interval:] + d_13[:interval]
                        d_60 = d_60[2 * interval:] + d_60[:2 * interval]
