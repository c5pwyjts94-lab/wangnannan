# ===================== 1. 导入所需依赖库 =====================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 解决matplotlib中文显示乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False
# 设置可视化风格
sns.set_style('whitegrid')

# ===================== 2. 配置核心参数（可按需修改） =====================
# 数据集文件路径（请确保该文件在代码运行目录下，或修改为绝对路径）
DATA_PATH = 'TASK2\heart_failure_clinical_records_dataset.csv'
# 预处理后数据集保存路径
OUTPUT_CSV_PATH = 'heart_failure_preprocessed_dataset.csv'
OUTPUT_EXCEL_PATH = 'heart_failure_preprocessed_dataset.xlsx'
# 可视化图表保存文件夹
FIG_SAVE_DIR = 'preprocessing_visualization'
# 需要处理的连续型数值字段（完全匹配您的指定）
CONTINUOUS_COLS = [
    'age',
    'creatinine_phosphokinase',
    'ejection_fraction',
    'platelets',
    'serum_creatinine',
    'serum_sodium',
    'time'
]
# 分类字段（用于统计分析）
CATEGORICAL_COLS = [
    'anaemia',
    'diabetes',
    'high_blood_pressure',
    'sex',
    'smoking',
    'DEATH_EVENT'
]
# IQR法异常值识别系数（默认1.5，为行业通用标准）
IQR_FACTOR = 1.5

# ===================== 3. 加载数据集 & 基础校验 =====================
print('='*50)
print('1. 数据集加载与基础校验')
print('='*50)

# 检查文件是否存在
if not Path(DATA_PATH).exists():
    raise FileNotFoundError(f'未找到数据集文件，请检查路径是否正确：{DATA_PATH}')

# 加载数据
df = pd.read_csv(DATA_PATH)
# 备份原始数据，用于后续对比
df_original = df.copy()

print(f'数据集加载成功！')
print(f'数据总行数：{df.shape[0]} | 总字段数：{df.shape[1]}')
print(f'字段列表：{list(df.columns)}')
print('\n数据前5行预览：')
print(df.head())

# ===================== 4. 描述性统计分析 =====================
print('\n' + '='*50)
print('2. 完整描述性统计分析')
print('='*50)

# 4.1 数据基本信息
print('\n2.1 数据基本信息（字段类型、非空值数量）：')
df.info()

# 4.2 连续型字段描述性统计
print('\n2.2 连续型数值字段描述性统计：')
continuous_stats = df[CONTINUOUS_COLS].describe().round(4)
print(continuous_stats)

# 4.3 分类型字段分布统计
print('\n2.3 分类型字段分布统计（数量+占比）：')
for col in CATEGORICAL_COLS:
    print(f'\n--- {col} 字段分布 ---')
    count_dist = df[col].value_counts()
    ratio_dist = df[col].value_counts(normalize=True).round(4) * 100
    dist_df = pd.DataFrame({
        '数量': count_dist,
        '占比(%)': ratio_dist
    })
    print(dist_df)

# ===================== 5. 缺失值检查与处理 =====================
print('\n' + '='*50)
print('3. 缺失值检查结果')
print('='*50)

# 计算每个字段的缺失值数量和占比
missing_stats = pd.DataFrame({
    '缺失值数量': df.isnull().sum(),
    '缺失值占比(%)': (df.isnull().sum() / len(df) * 100).round(4)
})
print(missing_stats)

# 明确说明缺失值情况
total_missing = df.isnull().sum().sum()
if total_missing == 0:
    print('\n✅ 数据集无任何缺失值，无需进行缺失值填充/删除处理')
else:
    print(f'\n⚠️  数据集共存在 {total_missing} 个缺失值，可按需补充缺失值处理逻辑')

# ===================== 6. 基于IQR法的异常值识别 =====================
print('\n' + '='*50)
print('4. 基于IQR法的异常值识别结果')
print('='*50)

# 定义IQR异常值识别函数
def detect_outliers_iqr(data, factor=IQR_FACTOR):
    """
    基于IQR法识别异常值
    返回：异常值上下限字典、异常值标记DataFrame、各字段异常值统计
    """
    outlier_bounds = {}
    outlier_mask = pd.DataFrame()
    outlier_stats = []

    for col in CONTINUOUS_COLS:
        # 计算四分位数
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        # 计算异常值上下限
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        # 保存上下限
        outlier_bounds[col] = {
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            '下限': lower_bound,
            '上限': upper_bound
        }
        # 标记异常值
        col_outlier_mask = (data[col] < lower_bound) | (data[col] > upper_bound)
        outlier_mask[col] = col_outlier_mask
        # 统计异常值
        outlier_count = col_outlier_mask.sum()
        outlier_ratio = (outlier_count / len(data) * 100).round(4)
        outlier_stats.append({
            '字段名称': col,
            '异常值数量': outlier_count,
            '异常值占比(%)': outlier_ratio,
            '下限': round(lower_bound, 4),
            '上限': round(upper_bound, 4)
        })

    # 转换为DataFrame
    outlier_stats_df = pd.DataFrame(outlier_stats)
    # 计算每行是否存在异常值
    outlier_mask['行是否含异常值'] = outlier_mask.any(axis=1)
    total_outlier_rows = outlier_mask['行是否含异常值'].sum()
    total_outlier_ratio = (total_outlier_rows / len(data) * 100).round(4)

    return outlier_bounds, outlier_mask, outlier_stats_df, total_outlier_rows, total_outlier_ratio

# 执行异常值识别
outlier_bounds, outlier_mask, outlier_stats_df, total_outlier_rows, total_outlier_ratio = detect_outliers_iqr(df)

# 输出异常值统计结果
print('各字段异常值统计详情：')
print(outlier_stats_df)
print(f'\n数据集总异常值行数：{total_outlier_rows} 行，占比：{total_outlier_ratio}%')

# ===================== 7. 异常值缩尾处理（Winsorization） =====================
print('\n' + '='*50)
print('5. 异常值缩尾处理（Winsorization）执行结果')
print('='*50)

# 定义缩尾处理函数
def winsorize_data(data, outlier_bounds):
    """
    基于IQR上下限进行缩尾处理
    超出上下限的数值替换为对应的上下限
    """
    df_winsorized = data.copy()
    for col in CONTINUOUS_COLS:
        bounds = outlier_bounds[col]
        lower = bounds['下限']
        upper = bounds['上限']
        # 缩尾处理
        df_winsorized[col] = np.where(df_winsorized[col] < lower, lower, df_winsorized[col])
        df_winsorized[col] = np.where(df_winsorized[col] > upper, upper, df_winsorized[col])
        # 统计处理结果
        original_min = data[col].min()
        original_max = data[col].max()
        new_min = df_winsorized[col].min()
        new_max = df_winsorized[col].max()
        print(f'--- {col} 字段处理结果 ---')
        print(f'原始值范围：[{original_min:.4f}, {original_max:.4f}]')
        print(f'处理后范围：[{new_min:.4f}, {new_max:.4f}]')
        print(f'缩尾上下限：[{lower:.4f}, {upper:.4f}]\n')
    return df_winsorized

# 执行缩尾处理
df_preprocessed = winsorize_data(df, outlier_bounds)

# 输出处理后数据的描述性统计
print('✅ 缩尾处理完成！处理后连续字段描述性统计：')
print(df_preprocessed[CONTINUOUS_COLS].describe().round(4))

# ===================== 8. 生成可视化图表 =====================
print('\n' + '='*50)
print('6. 可视化图表生成中...')
print('='*50)

# 创建可视化保存文件夹
Path(FIG_SAVE_DIR).mkdir(exist_ok=True)

# 8.1 缺失值分布柱状图
print('生成缺失值分布图表...')
plt.figure(figsize=(12, 6))
sns.barplot(x=missing_stats.index, y='缺失值数量', data=missing_stats, palette='Reds_d')
plt.title('数据集各字段缺失值数量分布', fontsize=14, fontweight='bold')
plt.xlabel('字段名称', fontsize=12)
plt.ylabel('缺失值数量', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{FIG_SAVE_DIR}/缺失值分布.png', dpi=300, bbox_inches='tight')
plt.close()

# 8.2 异常值箱线图（处理前 vs 处理后对比）
print('生成异常值箱线图（处理前后对比）...')
# 处理前箱线图
plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
sns.boxplot(data=df_original[CONTINUOUS_COLS], palette='Set2')
plt.title('处理前连续字段异常值箱线图', fontsize=14, fontweight='bold')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
# 处理后箱线图
plt.subplot(2, 1, 2)
sns.boxplot(data=df_preprocessed[CONTINUOUS_COLS], palette='Set2')
plt.title('处理后连续字段异常值箱线图', fontsize=14, fontweight='bold')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(f'{FIG_SAVE_DIR}/异常值箱线图_前后对比.png', dpi=300, bbox_inches='tight')
plt.close()

# 8.3 字段分布直方图（处理前 vs 处理后对比）
print('生成字段分布直方图（处理前后对比）...')
# 计算子图行列数
n_cols = 3
n_rows = (len(CONTINUOUS_COLS) + n_cols - 1) // n_cols
plt.figure(figsize=(18, 5 * n_rows))

for i, col in enumerate(CONTINUOUS_COLS, 1):
    # 处理前分布
    plt.subplot(n_rows, n_cols * 2, i * 2 - 1)
    sns.histplot(df_original[col], kde=True, color='#1f77b4', bins=20)
    plt.title(f'处理前 {col} 分布', fontsize=12, fontweight='bold')
    plt.xlabel(col, fontsize=10)
    plt.ylabel('频数', fontsize=10)
    plt.tight_layout()
    # 处理后分布
    plt.subplot(n_rows, n_cols * 2, i * 2)
    sns.histplot(df_preprocessed[col], kde=True, color='#ff7f0e', bins=20)
    plt.title(f'处理后 {col} 分布', fontsize=12, fontweight='bold')
    plt.xlabel(col, fontsize=10)
    plt.ylabel('频数', fontsize=10)
    plt.tight_layout()

plt.savefig(f'{FIG_SAVE_DIR}/字段分布直方图_前后对比.png', dpi=300, bbox_inches='tight')
plt.close()

print(f'✅ 所有可视化图表已生成并保存至文件夹：{FIG_SAVE_DIR}')

# ===================== 9. 保存预处理后的最终数据集 =====================
print('\n' + '='*50)
print('7. 预处理后数据集保存')
print('='*50)

# 保存为CSV文件
df_preprocessed.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
# 保存为Excel文件
df_preprocessed.to_excel(OUTPUT_EXCEL_PATH, index=False)

print(f'✅ 预处理后的数据集已保存为CSV文件：{OUTPUT_CSV_PATH}')
print(f'✅ 预处理后的数据集已保存为Excel文件：{OUTPUT_EXCEL_PATH}')

# ===================== 10. 预处理总结 =====================
print('\n' + '='*50)
print('8. 数据预处理全流程总结')
print('='*50)
print(f'1. 数据集基础信息：{df.shape[0]}行 × {df.shape[1]}列')
print(f'2. 缺失值情况：无任何缺失值，无需缺失值处理')
print(f'3. 异常值识别：基于IQR法共识别出 {total_outlier_rows} 行含异常值的记录，占比 {total_outlier_ratio}%')
print(f'4. 异常值处理：对所有指定连续字段完成缩尾处理，超出IQR上下限的数值已替换为对应上下限')
print(f'5. 产物输出：已生成预处理后的数据集（CSV+Excel）、3类核心可视化图表')
print('='*50)
print('✅ 数据预处理全流程完成！')