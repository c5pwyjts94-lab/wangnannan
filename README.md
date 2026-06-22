# 项目说明文档
# 一.项目介绍
本项目需要综合运用大模型 API、机器学习与 LaTeX，在对应目录完成以下交付：
1. TASK1/（医学实体抽取）
任务说明：利用大语言模型（如 Claude/ChatGPT/Gemini）读取心力衰竭临床病例 PDF，进行医学命名实体抽取。
主要提交物：
case_entities.json：大模型抽取的结构化实体 JSON 文件。
源代码.py：包含API调用和prompt输出。
源文件
依赖包说明
3. TASK2/（模型构建与学术论文排版）
任务说明：对心衰患者数据集进行 Logistic Regression 与 XGBoost 建模，对比基线性能，并引入 SHAP 进行可解释性分析。使用 LaTeX 在本地或 Overleaf 完成全英文小论文排版。
主要提交物：
data:与模型有关的所有代码与数据表格
picture-task2/：全套科研图表（含混淆矩阵、ROC 曲线对比图、SHAP 摘要图等）。
main.pdf：核心交付物。利用 main.tex 编译生成的英文学术型大作业研究报告。
3. TASK3/（知识沉淀与指南交付）
任务说明：将前期的学习踩坑经验与大模型协作心得进行沉淀，编写一份对后续新人友好的快速上手指南。
主要提交物：
医疗大模型新人快速上手指南.md & .pdf：排版优美的 Markdown 指南文件及 PDF 导出版本。

#  仓库目录结构
## 📂 仓库目录结构

```text
医疗大模型挑战作业/
├── TASK1/                # 任务一：数据探索与预处理
│   ├── data/             # 原始数据及处理后的数据集
│   └── preprocess.py     # 数据清洗、异常值检测、标准化脚本
├── TASK2/                # 任务二：预测模型构建与评估
│   ├── data/             # 训练与测试集（标准化后）
│   └── train_predict.py  # Logistic Regression 与 XGBoost 模型训练脚本
├── TASK3/                # 任务三：模型可解释性分析与预测系统
│   ├── model/            # 训练好的模型权重/保存文件
│   └── interpret_shap.py # SHAP 归因分析与新患者预测推理脚本
├── main.pdf              # 核心提交物：最终大作业研究报告 (PDF)
└── requirements.txt      # 项目依赖环境配置文件
