import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. 读取数据 (请确保文件名和路径正确)
file_path = r'TASK2\data\withouttimeheart_failure_preprocessed_dataset.csv'
df = pd.read_csv(file_path)

# 2. 分离特征 (X) 和目标变量 (y)
X = df.drop('DEATH_EVENT', axis=1)
y = df['DEATH_EVENT']

# 3. 划分训练集和测试集 (80%训练集, 20%测试集)
# 使用 stratify=y 确保训练集和测试集中的死亡/存活比例与原数据一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. 定义需要进行 Z-score 标准化的连续型特征
continuous_cols = [
    'age', 
    'creatinine_phosphokinase', 
    'ejection_fraction', 
    'platelets', 
    'serum_creatinine', 
    'serum_sodium'
]

# 5. 初始化 Z-score 标准化器
scaler = StandardScaler()

# 复制一份数据以防修改原数据
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

# 【关键步骤】：只在训练集上 fit_transform (计算训练集的均值和方差并进行转换)
X_train_scaled[continuous_cols] = scaler.fit_transform(X_train[continuous_cols])

# 在测试集上只进行 transform (使用训练集的均值和方差对测试集进行转换)
X_test_scaled[continuous_cols] = scaler.transform(X_test[continuous_cols])

# 6. 将标准化后的特征与目标变量重新合并
train_processed = pd.concat([X_train_scaled, y_train], axis=1)
test_processed = pd.concat([X_test_scaled, y_test], axis=1)

# 7. 导出为 CSV 文件
train_processed.to_csv(r'TASK2\data\train_standardized.csv', index=False)
test_processed.to_csv(r'TASK2\data\test_standardized.csv', index=False)

print("数据标准化完成！")
print(f"训练集已保存为: train_standardized.csv (共 {len(train_processed)} 条样本)")
print(f"测试集已保存为: test_standardized.csv (共 {len(test_processed)} 条样本)")
