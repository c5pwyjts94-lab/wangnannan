import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)

import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# 1. 读取数据
# ==========================

train_df = pd.read_csv(r"TASK2\train_standardized.csv")
test_df = pd.read_csv(r"TASK2\test_standardized.csv")

# ==========================
# 2. 划分特征与标签
# ==========================

X_train = train_df.drop("DEATH_EVENT", axis=1)
y_train = train_df["DEATH_EVENT"]

X_test = test_df.drop("DEATH_EVENT", axis=1)
y_test = test_df["DEATH_EVENT"]

# ==========================
# 3. Grid Search
# ==========================

param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

grid = GridSearchCV(
    LogisticRegression(
        class_weight='balanced',
        max_iter=5000,
        random_state=42
    ),
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("=" * 50)
print("Best Parameters:")
print(grid.best_params_)
print("=" * 50)
# ==========================
# 4. 预测
# ==========================

y_pred = best_model.predict(X_test)

y_prob = best_model.predict_proba(X_test)[:, 1]
acc = accuracy_score(y_test, y_pred)
pre = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
print("\n")
print("=" * 50)
print("Logistic Regression Performance")
print("=" * 50)

print(f"Accuracy  : {acc:.4f}")
print(f"Precision : {pre:.4f}")
print(f"Recall    : {rec:.4f}")
print(f"F1-score  : {f1:.4f}")
print(f"AUC       : {auc:.4f}")