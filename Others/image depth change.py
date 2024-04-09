"""
This script is used to convert 16-bit depth images in the input folder to 8-bit depth images
 and save them in the output folder.
"""
import numpy as np
import cv2
import os


def bit_depth_change(inputFolder, outputFolder):
    for dirs, folders, files in os.walk(inputFolder):
        for filename in files:
            origin = os.path.join(dirs, filename)
            # origin: .../bacteria\\Saccharomyces\\13nm\\4\\batch1\\untitled000.tif
            img_16 = cv2.imread(origin, -1)
            MAX, MIN = np.max(img_16), np.min(img_16)
            img_16 = (img_16 - MIN) / (MAX - MIN) * 255
            img_8 = img_16.astype(np.uint8)

            species = origin.split("\\")[1]
            sub_folder = os.path.join(outputFolder, species)
            if not os.path.exists(sub_folder):
                os.mkdir(sub_folder)

            output = origin.split('bacteria\\')[-1].replace("\\", "_").replace("untitled", "")
            output = os.path.join(sub_folder, output)
            cv2.imwrite(output, img_8)


if __name__ == '__main__':
    inputFolder = "bacteria16"
    outputFolder = "bacteria8"
    bit_depth_change(inputFolder, outputFolder)
