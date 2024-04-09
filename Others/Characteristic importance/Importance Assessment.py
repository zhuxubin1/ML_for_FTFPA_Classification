"""
This script uses the random forest model to show the importance of each feature
when using Single images as input data.
The results are saved as bar chart images and a csv file containing the sum of
the importance of the features 0-224 and features 225-255.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Utils.io import load_model, read_img

if __name__ == "__main__":
    ROOT = f"D:/new_data/test_1/image_RF_FJ_1_0125"
    sum_225 = []
    sum_256 = []

    for concentration in ['10^4', '10^5', '10^6', 'all']:
        X_train, y_train = read_img(f"{ROOT}/train", "Single", concentration, feature_num=256)
        X_test, y_test = read_img(f"{ROOT}/test", "Single", concentration, feature_num=256)

        model_rf = load_model(f"model/rf_{concentration}.pkl")
        model_rf.fit(X_train, y_train)

        importance = model_rf.feature_importances_
        sum_225.append(np.sum(importance[:225]))
        sum_256.append(np.sum(importance[225:]))

        sorted_index = importance.argsort()[::-1]
        colors = ['#F2BA02' if i < 225 else '#DAE3F4' for i in sorted_index]

        plt.rcParams['font.family'] = 'Arial'
        plt.figure(figsize=(3, 3))
        plt.barh(range(len(sorted_index[:40])), model_rf.feature_importances_[sorted_index[:40]], color=colors[:40])
        plt.xticks(fontsize=10)
        plt.yticks([], fontsize=10)
        plt.xlabel('Feature Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        legend_elements = [plt.Rectangle((0, 0), 1, 1, color='#F2BA02'),
                           plt.Rectangle((0, 0), 1, 1, color='#DAE3F4')]
        plt.legend(legend_elements, ['0-224', '224-255'], loc='upper right', fontsize=10)
        plt.tight_layout()
        plt.savefig(f"feature_importance_{concentration}.png", dpi=1200, bbox_inches='tight')
        plt.close()

    data = {'0-224': sum_225, '225-256': sum_256}
    df = pd.DataFrame(data)
    df.index = ['10^4', '10^5', '10^6', 'all']
    df.to_csv('feature_importance.csv')
