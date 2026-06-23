# 医疗大模型挑战作业

## 一、项目简介

### TASK1：病例实体提取

**任务说明**：利用大语言模型（如 Claude/ChatGPT/Gemini）读取心力衰竭临床病例 PDF，进行医学命名实体抽取。

 **主要提交物**： 

* case_entities.json：大模型抽取的结构化实体 JSON 文件

* 源代码.py：包含API调用和prompt输出

* 源文件 依赖包说明

### TASK2：心衰死亡率预测

 **任务说明**：对心衰患者数据集进行 Logistic Regression 与 XGBoost 建模，对比基线性能，并引入 SHAP 进行可解释性分析。使用 LaTeX 在本地或 Overleaf 完成全英文小论文排版。 

**主要提交物**：

* data/:与模型有关的所有代码与数据表格
* picture-task2/：全套科研图表（含混淆矩阵、ROC 曲线对比图、SHAP 摘要图等）
* main.pdf：核心交付物，利用 main.tex 编译生成的英文学术型大作业研究报告
* main.tex:latex源代码

###  TASK3：医疗大模型新人快速上手指南

**任务说明**：将前期的学习踩坑经验与大模型协作心得进行沉淀，编写一份对后续新人友好的快速上手指南。

**主要提交物**：

*  医疗大模型新人快速上手指南.md & .pdf： Markdown 指南文件及 PDF 导出版本。

  ## 二.📂 仓库目录结构

```markdown

医疗大模型挑战作业/
├── AI_Chat_Records.md                     # AI 协作记录根目录（含各任务交互记录）
│   ├── TASK1相关的AI chat.md             # 任务一 AI 提示词与对话留痕
│   ├── TASK2相关的AI交互.md              # 任务二 AI 提示词与对话留痕
│   └── TASK3相关的AI交互.md              # 任务三 AI 提示词与对话留痕
│
├── TASK1/                                # 任务一：基于大语言模型的病例实体提取
│   ├── 源代码.py                         # API调用、Prompt构建与实体抽取主程序
│   ├── A case of portal vein...pdf       # 临床病例参考报告（英文PDF）
│   ├── case_entities.json                # 大模型抽取后的结构化实体结果
│   └── requirements.txt                  # 任务一运行环境依赖
│
├── TASK2/                                # 任务二：心衰患者死亡率预测建模
│   ├── data/                             # 数据集与核心建模代码
│   │   ├── heart_failure_clinical_records_dataset.csv      
│   │   ├── 数据预处理代码.py
│   │   ├── 全相关热力图.py
│   │   ├── 逻辑回归.py
│   │   ├── XGBoost建模.py
│   │   ├── ROC对比绘图.py
│   │   └── 其他分析脚本...
│   │
│   ├── picture-task2/                    # 模型评估与可视化结果
│   │   ├── 缺失值分布.png
│   │   ├── boxplot_compare_before_after.png
│   │   ├── correlationheatmap.png
│   │   ├── ConfusionMatrix_XGBoost.png
│   │   ├── ROC_Comparison.png
│   │   ├── SHAP_Bar.png
│   │   ├── SHAP_Summary.png
│   │   └── 其他图表结果...
│   │
│   ├── main.tex                          # 论文LaTeX源码
│   ├── main.pdf                          # 最终论文PDF
│   └── requirements.txt                  # 任务二运行环境依赖
│
├── TASK3/                                # 任务三：医疗大模型新人快速上手指南
│   ├── 医疗大模型新人快速上手指南.md      # Markdown版指南
│   └── 医疗大模型新人快速上手指南.pdf     # PDF版指南
│
└── README.md                             # 项目说明文档
```

## 三、TASK1运行说明

### 功能介绍

本任务用来运行指定论文，通过调用API与system prompt和user prompt的输出来进行医学实体json文件的输出，介绍病人症状与相应病理与解决方案

### 输入文件

`源代码.py`

### 输出文件

`case_entities.json`

### 运行方法

先下载requirement文件里的依赖包，运行源文件，在弹窗中输入API密钥等信息，最后可在同目录根下得到json文件的输出。

```bash
python 源代码.py
```

## 四、TASK2运行说明

### 任务概述

本任务以心力衰竭（Heart Failure）患者临床数据为研究对象，构建死亡风险预测模型，并对不同机器学习方法的预测性能进行比较分析。整个实验流程涵盖数据预处理、特征分析、模型训练、性能评估以及模型可解释性分析等环节，最终输出数据文件、可视化图表及模型评价结果。

本实验采用逻辑回归（Logistic Regression）作为基准模型，以XGBoost作为核心预测模型，并结合SHAP方法对模型预测结果进行解释分析。

###  步骤① 数据预处理

#### 输入文件

- 原始临床数据集（CSV格式）:`heart_failure_clinical_records_dataset.csv`

#### 主要处理内容

- 基于IQR（Interquartile Range）方法检测并处理异常值；
- 对各数值型变量进行数据质量检查；
- 生成清洗后的数据集文件；
- 输出数据清洗前后的可视化结果，包括：
  - 变量分布图；
  - 异常值处理效果对比图。

#### 输出结果

- 清洗后数据集；
- 数据预处理相关图表。

------

### 步骤② 变量相关性分析

为分析各临床特征之间的相关关系，计算变量相关系数矩阵并绘制热力图。

#### 主要内容

- 计算Pearson相关系数；
- 构建变量相关性热力图；
- 初步评估变量间相关程度及潜在多重共线性问题。

#### 输出结果

- `correlation_heatmap.png`

------

### 步骤③ 数据标准化与数据集划分

为了保证模型训练稳定性与实验结果可比性，对数据进行统一标准化处理，并划分训练集与测试集。

#### 主要内容

- 对全部连续变量执行Z-score标准化；
- 保持目标变量不参与标准化；
- 按固定比例划分训练集和测试集；
- 保存标准化后的训练数据与测试数据。

#### 输出结果

- 训练集（Train Set）
- 测试集（Test Set）

------

### 步骤④ 逻辑回归基准模型训练与评估

逻辑回归模型作为传统统计学习方法，用于建立基准预测模型。

#### 主要内容

- 基于训练集训练Logistic Regression模型；
- 在测试集上完成预测；
- 计算分类评价指标，包括：
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - ROC-AUC
- 输出模型分析图及结果文件。

#### 输出结果

- 逻辑回归预测结果；
- 模型评价指标；
- `analysis.png`

------

### 步骤⑤ 多模型ROC曲线对比分析

为比较不同模型的判别能力，对逻辑回归模型与XGBoost模型的ROC曲线进行统一绘制。

#### 主要内容

- 获取各模型预测概率；
- 计算ROC曲线及AUC值；
- 在同一画布中绘制ROC对比图；
- 直观比较不同模型的分类性能。

#### 输出结果

- 模型预测结果文件；
- ROC对比图。

------

### 步骤⑥ XGBoost模型构建与SHAP可解释性分析

XGBoost为本研究的核心预测模型，在完成模型训练后进一步开展模型解释分析。

#### （1）模型性能评估

主要输出内容包括：

- ROC曲线；
- Accuracy、Precision、Recall、F1-score、AUC等评价指标；
- 混淆矩阵（Confusion Matrix）；
- 分类结果分析报告。

#### 输出结果

- XGBoost ROC曲线；
- 混淆矩阵热力图；
- 分类评价指标结果。

------

#### （2）特征重要性分析

利用XGBoost内置特征重要性指标评估各变量对预测结果的贡献程度。

#### 输出结果

- Feature Importance图；
- 特征贡献排序结果。

------

#### （3）SHAP可解释性分析

采用SHAP（SHapley Additive Explanations）方法解释模型预测机制。

分析内容包括：

- 单样本特征影响分析；
- 全局特征贡献分析；
- 变量重要性排序解释。

#### 输出结果

- SHAP Summary Plot；
- SHAP Bar Plot；
- SHAP Value Scatter Plot。

### 实验输出文件汇总

####  数据文件

- 清洗后数据集；
- 标准化数据集；
- 训练集与测试集；
- Logistic Regression预测结果；
- XGBoost预测结果。

#### . 可视化结果

- 变量分布图；
- 异常值处理效果图。

- 相关性热力图。

- 模型分析图。

- ROC曲线对比图。

- ROC曲线；

- 混淆矩阵；

- 特征重要性图；

- SHAP Summary图；

- SHAP Bar图；

- SHAP散点图。

  ### 为保证实验流程正常执行及各阶段输出文件正确生成，必须严格按照以下顺序运行：

1. 数据预处理；
2. 变量相关性热力图绘制；
3. 数据标准化与训练测试集划分；
4. 逻辑回归模型训练与评估；
5. 多模型ROC曲线对比分析；
6. XGBoost模型构建与SHAP可解释性分析。

请勿调整上述执行顺序，否则可能导致数据依赖缺失或结果文件无法正常生成。

## 五、TASK3说明

### 指南内容

- 医疗大模型基础知识
- API调用方法
- Prompt工程入门
- 常见错误与排查
- Git与GitHub基础

## 六、项目输出成果

### TASK1输出

- case_entities.json

### TASK2输出

- ROC曲线
- 混淆矩阵
- SHAP解释图
- 特征重要性图
- LaTeX论文
- PDF论文

### TASK3输出

- Markdown指南
- PDF指南

## 七、注意事项

- API Key配置
- 网络要求
- 文件路径要求
- 随机种子固定
- 环境依赖版本说明

## 八、新人学习路线建议

1. 阅读TASK3指南
2. 运行TASK1理解医疗实体抽取
3. 运行TASK2学习机器学习建模流程
4. 阅读论文与代码
5. 尝试修改Prompt与模型参数进行实验

```
这个结构基本符合企业新人培训项目、科研项目和比赛项目的 README 标准格式。
```
