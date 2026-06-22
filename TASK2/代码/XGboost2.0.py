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
train = pd.read_csv(r"D:\医疗大模型挑战作业\TASK2\train_standardized.csv")
test = pd.read_csv(r"D:\医疗大模型挑战作业\TASK2\test_standardized.csv")
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