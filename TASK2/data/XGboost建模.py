import pandas as pd
import numpy as np
import shap

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve
)

import matplotlib.pyplot as plt
import seaborn as sns
train = pd.read_csv(r"TASK2\data\train_standardized.csv")
test = pd.read_csv(r"TASK2\data\test_standardized.csv")
print(train.shape)
print(test.shape)
X_train = train.drop("DEATH_EVENT", axis=1)
y_train = train["DEATH_EVENT"]

X_test = test.drop("DEATH_EVENT", axis=1)
y_test = test["DEATH_EVENT"]
print(X_train.shape)
print(X_test.shape)
xgb_model = XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',

    n_estimators=200,

    max_depth=3,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42
)
xgb_model.fit(X_train, y_train)
explainer = shap.TreeExplainer(xgb_model)
y_prob = xgb_model.predict_proba(X_test)[:,1]
y_pred = (y_prob >= 0.5).astype(int)
acc = accuracy_score(y_test,y_pred)
pre = precision_score(y_test,y_pred)
rec = recall_score(y_test,y_pred)
f1 = f1_score(y_test,y_pred)
auc = roc_auc_score(y_test,y_prob)
print("Accuracy =",acc)
print("Precision =",pre)
print("Recall =",rec)
print("F1 =",f1)
print("AUC =",auc)
fpr,tpr,_ = roc_curve(y_test,y_prob)

plt.figure(figsize=(6,6))

plt.plot(
    fpr,
    tpr,
    linewidth=2,
    label=f"AUC={auc:.3f}"
)

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve of XGBoost")

plt.legend()

plt.tight_layout()

plt.savefig(
    r"TASK2\picture-task2\ROC_XGBoost.png",
    format="png",
    bbox_inches="tight"
)

plt.show()
cm = confusion_matrix(y_test,y_pred)

plt.figure(figsize=(5,4))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues'
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.title("Confusion Matrix")

plt.tight_layout()

plt.savefig(
    r"TASK2\picture-task2\ConfusionMatrix_XGBoost.png",
    format="png",
    dpi=300,                    
    bbox_inches="tight"         
)

plt.show()
from xgboost import plot_importance

plt.figure(figsize=(8,6))

plot_importance(
    xgb_model,
    max_num_features=11,
    height=0.6
)

plt.title("Feature Importance")

plt.tight_layout()

plt.savefig(
    r"TASK2\picture-task2\FeatureImportance_XGBoost.png",
    format="png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': xgb_model.feature_importances_
})

importance = importance.sort_values(
    by='Importance',
    ascending=False
)

print(importance.head(3))
shap_values = explainer.shap_values(X_test)
print(shap_values.shape)
plt.figure()

shap.summary_plot(
    shap_values,
    X_test,
    show=False
)

plt.tight_layout()

plt.savefig(
    r"TASK2\picture-task2\SHAP_Summary.png",
    format="png",
    bbox_inches="tight"
)

plt.show()
plt.figure()

shap.summary_plot(
    shap_values,
    X_test,
    plot_type="bar",
    show=False
)

plt.tight_layout()

plt.savefig(
    r"TASK2\picture-task2\SHAP_Bar.png",
    format="png",
    bbox_inches="tight"
)

plt.show()
# ==========================================
# 新增：构建 1 个新患者示例并预测死亡概率
# ==========================================
print("\n" + "="*40)
print("--- 新患者预测示例 ---")

# 1. 构造新患者数据
# 获取模型训练时的所有特征列名
feature_columns = X_train.columns

# 随机生成一个新患者的标准化特征数据 (假设数值在 -1.5 到 1.5 之间)
# 实际业务中，这里应填入真实患者数据，并使用与训练集相同的 Scaler 进行 transform 标准化
np.random.seed(100) 
new_patient_data = {col: [np.random.uniform(-1.5, 1.5)] for col in feature_columns}
new_patient_df = pd.DataFrame(new_patient_data)

print("新患者的特征数据 (标准化后):")
# 转置打印以便于观察
print(new_patient_df.T.rename(columns={0: "Feature Value"}))

# 2. 预测死亡概率
# predict_proba 返回的是 [预测为0的概率, 预测为1的概率]，我们取索引 1 即死亡(DEATH_EVENT=1)的概率
new_patient_prob = xgb_model.predict_proba(new_patient_df)[:, 1][0]

# 3. 根据阈值 (0.5) 得出最终分类结果
new_patient_pred = int(new_patient_prob >= 0.5)

print("\n--- 预测结果 ---")
print(f"该新患者的预测死亡概率为: {new_patient_prob:.4f} ({new_patient_prob * 100:.2f}%)")
if new_patient_pred == 1:
    print("模型最终预测类别: 1 (高风险 / 预测死亡)")
else:
    print("模型最终预测类别: 0 (低风险 / 预测存活)")
print("="*40 + "\n")
