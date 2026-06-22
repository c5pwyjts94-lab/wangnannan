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
# ==========================
# ==========================
# 8. OR分析
# ==========================

coef = best_model.coef_[0]

or_value = np.exp(coef)

or_df = pd.DataFrame({
    "Feature": X_train.columns,
    "Coefficient": coef,
    "Odds_Ratio": or_value
})

or_df = or_df.sort_values(
    by="Odds_Ratio",
    ascending=False
)

print("\nOdds Ratio Analysis")
print(or_df)

or_df.to_csv(
    "Logistic_OR_Table.csv",
    index=False,
    encoding="utf-8-sig"
)
plt.figure(figsize=(8,6))

sns.barplot(
    data=or_df,
    x="Odds_Ratio",
    y="Feature"
)

plt.axvline(
    1,
    linestyle="--",
    linewidth=1
)

plt.title("Odds Ratio of Risk Factors")

plt.tight_layout()

plt.savefig(
    "OR_Analysis.svg",
    format="svg",
    bbox_inches="tight"
)

plt.show()