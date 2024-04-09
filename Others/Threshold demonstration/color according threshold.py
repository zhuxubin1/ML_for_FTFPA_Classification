"""
This script is used to color the image according to the gray level threshold and draw the histogram.
"""
import cv2
import matplotlib.pyplot as plt

for concentration in ["10^4", "10^5", "10^6"]:
    file = f"data/E.coli_13nm_{concentration}.tif"
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    color_mask = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    color_mask[img < 225] = (39, 127, 255)
    color_mask[img >= 225] = (255, 0, 0)
    output = cv2.addWeighted(color_mask, 0.5, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), 0.75, 0)
    cv2.imwrite(f"color_mask_{concentration}.png", output)

    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    fig, ax = plt.subplots(figsize=(8, 4))
    hist_color = ["#ff7f27"] * 225 + ["#0000ff"] * 31
    ax.bar(range(256), hist.ravel(), width=1, color=hist_color)
    plt.axvline(x=225, color='black', linestyle="--")
    ax.set_xticks(ax.get_xticks().tolist() + [225])
    ax.set_xlim([0, 255.5])
    ax.set_xlabel('Gray Level')
    ax.set_ylabel('Frequency')
    plt.savefig(f"hist_{concentration}.png", dpi=600)
    plt.close()
