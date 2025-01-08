import numpy as np
import matplotlib.pyplot as plt
import csv
import argparse
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Set argument
parser = argparse.ArgumentParser(description='Draw ROC curve from multiple CSV files')
parser.add_argument('--draw', type=str, nargs='+', default=['cora'], help='Names of datasets (CSV files without extension) to draw')
args = parser.parse_args()

# 绘制所有ROC曲线
plt.figure(figsize=(8, 6))  # 设置图形大小

save_name = ""
# 遍历传入的多个数据集
for dataset_name in args.draw:
    fpr = []
    tpr = []
    roc_auc = 0
    save_name+=dataset_name+"_"
    # 读取CSV文件中的数据
    try:
        with open(f'draw_data/{dataset_name}_CoLA.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过标题行
            for row in reader:
                if row[0] == 'AUC':
                    roc_auc = float(row[1])
                else:
                    fpr.append(float(row[0]))
                    tpr.append(float(row[1]))

        fpr = np.array(fpr)
        tpr = np.array(tpr)

        # 绘制ROC曲线
        plt.plot(fpr, tpr, marker='o', markersize=0.5, linestyle='-', label=f'{dataset_name} ROC curve (AUC = {roc_auc:.4f})')

    except FileNotFoundError:
        print(f"Warning: File 'draw_data/{dataset_name}_CoLA.csv' not found, skipping this dataset.")
        continue

# 设置图形的x轴和y轴范围
plt.xlim(0, 1)
plt.ylim(0, 1.05)

# 添加标题和标签
plt.title('ROC Curves for Multiple Datasets')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

# 添加图例
plt.legend(loc='lower right')

# 保存图形为图片文件
plt.savefig(f'draw_images/{save_name}.png', dpi=300, bbox_inches='tight')

# 显示图形
plt.show()
