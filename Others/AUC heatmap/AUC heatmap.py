"""
This script is used to draw the heatmap of AUROC and AUPR of the single and merged dichotomies models.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Utils.names import *


def draw_heatmap(file, output_name):
    # ================= process the excel table =================
    df = pd.read_excel(file, sheet_name="Sheet1", header=0, index_col=None)
    # select the columns of target, concentration, AUROC, AUPR, and remove the last row "xBlank"
    df = df.iloc[:, [0, 3, 4, 5]]
    df = df.iloc[:-1, :]
    df = df.pivot_table(index=["target"], columns="concentration", values=["AUROC", "AUPR"])
    df.columns = ["_".join(x) for x in df.columns.ravel()]
    df = df.T
    df = df.reindex(["AUROC_10^4", "AUPR_10^4", "AUROC_10^5", "AUPR_10^5",
                     "AUROC_10^6", "AUPR_10^6", "AUROC_all", "AUPR_all"]).copy()

    # ================= draw the heatmap =================
    plt.rc('font', family='Arial')
    fig, ax1 = plt.subplots(figsize=(9, 6))
    img = ax1.imshow(df.values, cmap=plt.cm.coolwarm, vmin=0.5, vmax=1)
    ax1.set_xticks(range(df.shape[1]))
    xlabels = [name_to_abbr.get(name, name) for name in df.columns]
    ax1.set_xticklabels(xlabels, fontsize=13)
    ax1.set_yticks(range(df.shape[0]))
    ylabels = ["AUROC", "AUPR"] * 4
    ax1.set_yticklabels(ylabels, fontsize=13)

    # y-axis on the right
    ax2 = ax1.twinx()
    ax2.imshow(df.values, cmap=plt.cm.coolwarm, vmin=0.5, vmax=1)
    ax2.set_yticks(np.arange(0.5, df.shape[0], 2))
    ax2.set_yticklabels(["10$^4$", "10$^5$", "10$^6$", "all"], fontsize=20)
    ax2.tick_params(axis="y", which="both", length=0)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            ax2.text(j, i, round(df.iloc[i, j], 2), ha="center", va="center", color="black", fontsize=13)
    fig.colorbar(img, ax=ax1, pad=0.1)
    plt.savefig(output_name, bbox_inches="tight", dpi=1200)
    plt.close()


if __name__ == '__main__':
    # Single
    file_single = "Dichotomies_single_AUROC_AUPR.xlsx"
    output_name = "single_AUROC.png"
    draw_heatmap(file_single, output_name)
    # Merged
    file_merged = "Dichotomies_merged_AUROC_AUPR.xlsx"
    output_name = "merged_AUROC.png"
    draw_heatmap(file_merged, output_name)
