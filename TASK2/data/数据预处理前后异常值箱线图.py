import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ===================== 路径配置（和你本地文件对应） =====================
RAW_CSV = r"TASK2\data\heart_failure_clinical_records_dataset.csv"
PRE_CSV = r"TASK2\data\heart_failure_preprocessed_dataset.csv"
FIG_DIR = r"TASK2\picture-task2"
Path(FIG_DIR).mkdir(exist_ok=True)

# 连续字段列表（原始英文，不做中文转换）
CONTINUOUS_COLS = [
    'age',
    'creatinine_phosphokinase',
    'ejection_fraction',
    'platelets',
    'serum_creatinine',
    'serum_sodium',
    'time'
]

# 读取原始数据 & 预处理后数据
df_raw = pd.read_csv(RAW_CSV)
df_pre = pd.read_csv(PRE_CSV)

# 只保留连续字段用于绘图
df_raw_plot = df_raw[CONTINUOUS_COLS]
df_pre_plot = df_pre[CONTINUOUS_COLS]

# 绘图全局设置：关闭中文渲染，纯英文环境，杜绝乱码
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# 创建画布，上下两张子图
plt.figure(figsize=(16, 10))

# 上图：原始数据箱线图
plt.subplot(2, 1, 1)
sns.boxplot(data=df_raw_plot, palette="Set2")
plt.title("Raw Data Boxplot (Before IQR Winsorization)", fontsize=14, weight="bold")
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.ylabel("Value", fontsize=12)

# 下图：缩尾处理后箱线图
plt.subplot(2, 1, 2)
sns.boxplot(data=df_pre_plot, palette="Set2")
plt.title("Processed Data Boxplot (After IQR Winsorization)", fontsize=14, weight="bold")
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.ylabel("Value", fontsize=12)

# 自动调整布局防止文字截断
plt.tight_layout()

# 保存高清图片
save_path = r"TASK2\picture-task2\boxplot_compare_before_after.png"
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"箱线图已保存至：{save_path}")
print("绘图完成，全部字段、标题均为英文，无中文乱码问题")