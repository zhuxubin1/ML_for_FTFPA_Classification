"""
This script is used to find the peak value for every row in the file, and then calculate
the mean value and the 95% confidence interval.
"""
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import find_peaks


def findNearMid(arr, mid):
    """find the value in arr which is nearest to mid."""
    if len(arr) == 0:
        return -1
    return arr[np.argmin(np.abs(arr - mid))]


def findAllPeaks(file):
    """find all peaks for every row in the Excel file."""
    df = pd.read_excel(file, header=None)
    # determine the peak value corresponding to the average data
    mean = df.mean(axis=0)
    pf = np.polyfit(np.arange(len(mean)), mean, 9)
    pf_val = np.polyval(pf, np.arange(len(mean)))
    peaks, _ = find_peaks(pf_val)

    filtered_peaks = peaks[np.where(peaks < 270)]
    filtered_peaks = filtered_peaks[np.where(filtered_peaks > 30)]
    if filtered_peaks.size != 1:
        if filtered_peaks.size > 1:
            filtered_peaks = np.array([peaks[0]])
        elif filtered_peaks.size == 0:
            plt.plot(mean)
            plt.show()
            filtered_peaks = np.array([float(input("input the peak value: "))])
    new_peaks, _ = find_peaks(mean)
    new_peaks = findNearMid(new_peaks, filtered_peaks[0])

    # determine the peak value for every single row
    single_peaks = []
    for i, row in df.iterrows():
        r = np.array(row)
        single_peak, _ = find_peaks(r)
        single_peak = single_peak[np.where(single_peak < 270)]
        single_peak = single_peak[np.where(single_peak > 30)]
        single_peak = findNearMid(single_peak, new_peaks)

        if single_peak == -1:
            single_peak = round(new_peaks)
        single_peaks.append(single_peak)
    return np.array(single_peaks)


if __name__ == '__main__':
    root = "./wave_length_data"
    output = "result.csv"
    f = open(output, "w", encoding="utf-8")
    f.write("filename,mean,low,high,halfLength\n")
    for file in os.listdir(root):
        final_peaks = findAllPeaks(os.path.join(root, file))
        mean = final_peaks.mean()
        low = np.percentile(final_peaks, 2.5)
        high = np.percentile(final_peaks, 97.5)
        f.write(f"{file.removesuffix('.xlsx')},{round(mean, 3)},"
                f"{round(low, 3)},{round(high, 3)},{round((high - low) / 2, 3)}\n")
    f.close()
