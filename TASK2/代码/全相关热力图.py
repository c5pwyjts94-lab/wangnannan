import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# 读取数据
# ==========================
file_path = "TASK2\heart_failure_preprocessed_dataset.csv"
df = pd.read_csv(file_path)

# ==========================
# Pearson相关系数矩阵
# ==========================
corr_matrix = df.corr(numeric_only=True)

# ==========================
# 绘图
# ==========================
plt.rcParams["font.family"] = "Times New Roman"

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(
    corr_matrix,
    annot=True,           # 显示数值
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    square=True,
    linewidths=0.5,
    linecolor="white",
    annot_kws={
        "size": 7
    },
    cbar_kws={
        "shrink": 0.8
    }
)

# ==========================
# 美化
# ==========================
plt.xticks(
    rotation=45,
    ha='right',
    fontsize=8
)

plt.yticks(
    rotation=0,
    fontsize=8
)

plt.title(
    "Pearson Correlation Heatmap",
    fontsize=14,
    pad=15
)

plt.tight_layout()

# ==========================
# 保存SVG
# ==========================
plt.savefig(
    "Correlation_Heatmap.svg",
    format="svg",
    bbox_inches="tight"
)

plt.show()