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

# 📂 仓库目录结构
医疗大模型挑战作业/
├── AI_Chat_Records.md        # AI 协作记录根目录（含各任务交互记录）
│   ├── TASK1相关的AI chat.md  # 任务一 AI 提示词与对话留痕
│   ├── TASK2相关的AI交互.md   # 任务二 AI 提示词与对话留痕
│   └── TASK3相关的AI交互.md   # 任务三 AI 提示词与对话留痕
├── TASK1/                    # 任务一：个案分析
│   ├── 源代码.py              # API调用与prompt输入
│   ├── A case of portal vein...pdf # 临床病例参考报告
│   ├── case_entities.json    # 大模型抽取的临床实体数据
│   └── requirements.txt      # 任务一环境依赖
├── TASK2/                    # 任务二：预测模型构建、评估与论文排版
│   ├── data/                 # 核心数据集（原始、预处理及切分数据）
│   │   ├── 逻辑回归.py / 全相关热力图.py / 数据预处理代码.py
│   │   ├── heart_failure_clinical_records_dataset.csv
│   │   └── XGboost建模.py / ROC对比绘图.py ...
│   ├── picture-task2/         # 任务二模型评估与可视化图表交付物
│   │   ├── 缺失值分布.png / boxplot_compare_before_after.png
│   │   ├── correlationheatmap.png / ConfusionMatrix_XGBoost.png
│   │   └── ROC_Comparison.png / SHAP_Summary.png ...
│   ├── main.tex / main.pdf   # 核心提交物：LaTeX 撰写的学术研究论文
│   └── requirements.txt      # 任务二环境依赖
├── TASK3/                    # 任务三：产品化落地交付
│   ├── 医疗大模型新人快速上手指南.md  # 交付物：Markdown 版产品上手指南
│   └── 医疗大模型新人快速上手指南.pdf  # 交付物：导出的 PDF 版指南
└── README.md                 # 本说明文件
