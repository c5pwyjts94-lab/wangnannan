import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    roc_curve,
    roc_auc_score
)
train = pd.read_csv(r"D:\医疗大模型挑战作业\TASK2\train_standardized.csv")
test = pd.read_csv(r"D:\医疗大模型挑战作业\TASK2\test_standardized.csv")

X_train = train.drop("DEATH_EVENT", axis=1)
y_train = train["DEATH_EVENT"]

X_test = test.drop("DEATH_EVENT", axis=1)
y_test = test["DEATH_EVENT"]
from sklearn.linear_model import LogisticRegression

log_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

log_model.fit(X_train,y_train)

prob_log = log_model.predict_proba(X_test)[:,1]
from xgboost import XGBClassifier

xgb_model = XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',

    max_depth=3,
    learning_rate=0.05,
    n_estimators=200,

    subsample=0.8,
    colsample_bytree=0.8,

    random_state=42
)

xgb_model.fit(X_train,y_train)

prob_xgb = xgb_model.predict_proba(X_test)[:,1]
# Logistic ROC

fpr_log, tpr_log, _ = roc_curve(
    y_test,
    prob_log
)

auc_log = roc_auc_score(
    y_test,
    prob_log
)

# XGBoost ROC

fpr_xgb, tpr_xgb, _ = roc_curve(
    y_test,
    prob_xgb
)

auc_xgb = roc_auc_score(
    y_test,
    prob_xgb
)

print(f"Logistic AUC = {auc_log:.4f}")
print(f"XGBoost AUC = {auc_xgb:.4f}")
plt.figure(figsize=(6,6))

# Logistic

plt.plot(
    fpr_log,
    tpr_log,
    linewidth=2.5,
    label=f'Logistic Regression (AUC={auc_log:.3f})'
)

# XGBoost

plt.plot(
    fpr_xgb,
    tpr_xgb,
    linewidth=2.5,
    label=f'XGBoost (AUC={auc_xgb:.3f})'
)

# 随机分类器

plt.plot(
    [0,1],
    [0,1],
    linestyle='--',
    color='gray',
    linewidth=1.5
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve Comparison")

plt.legend(loc="lower right")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    r"D:\医疗大模型挑战作业\TASK2\ROC_Comparison.svg",
    format="svg",
    bbox_inches="tight"
)

plt.show()