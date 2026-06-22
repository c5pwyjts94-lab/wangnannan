import fitz
import json
import re
import getpass
from openai import OpenAI


# =========================
# 配置区
# =========================

# 移除了硬编码的 API_KEY, BASE_URL, MODEL_NAME，改为运行时输入

PDF_PATH = r"TASK1\A case of portal vein recanalization and symptomatic heart failure (1).pdf"

OUTPUT_JSON = "case_entities.json"


# =========================
# System Prompt
# =========================

SYSTEM_PROMPT = """
你是一名医学信息抽取专家。

请从病例中抽取以下实体。

规则：

1. 仅抽取原文出现内容
2. 禁止推测
3. 保留原始表述
4. 未出现填写 null
5. 多项内容使用数组
6. 输出必须为合法JSON
7. 不输出解释
8. 必须保留全部字段
9. 未出现字段填写 null 或 []

JSON格式：

{
  "患者基本信息": {
    "姓名": null,
    "性别": null,
    "年龄": null
  },
  "主诉": null,
  "主要症状": [],
  "现病史": null,
  "既往史": [],
  "个人史": [],
  "家族史": [],
  "体格检查": [],
  "辅助检查": [],
  "实验室检查": [],
  "影像学检查": [],
  "诊断结果": [],
  "治疗方案": [],
  "药物治疗": [],
  "手术治疗": [],
  "治疗经过": null,
  "并发症": [],
  "出院情况": null,
  "预后随访": null
}

只返回JSON。
"""


# =========================
# User Prompt模板（已修复：示例JSON大括号全部双层{{}}）
# =========================

USER_PROMPT_TEMPLATE = """
任务：

从病例中抽取医学实体。

规则：

1. 仅提取原文内容
2. 不推断
3. 保留原文
4. 未出现写null
5. 多个内容用数组
6. 仅输出JSON

示例：

病例：

患者男性，56岁。

因“反复咳嗽3个月”入院。

既往高血压病史10年。

胸部CT提示右肺占位。

诊断为肺癌。

给予胸腔镜下肺叶切除术治疗。

输出：

{{
  "患者基本信息": {{
    "性别": "男性",
    "年龄": "56岁"
  }},
  "主要症状": [
    "反复咳嗽3个月"
  ],
  "既往史": [
    "高血压病史10年"
  ],
  "诊断结果": [
    "肺癌"
  ],
  "治疗方案": [
    "胸腔镜下肺叶切除术治疗"
  ]
}}

现在开始抽取：

病例：

{case_text}
"""


# =========================
# PDF读取
# =========================

def read_pdf(pdf_path):
    """
    读取PDF文本
    """

    try:

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return text.strip()

    except Exception as e:

        print(f"PDF读取失败: {e}")
        return None


# =========================
# 清洗模型输出
# =========================

def clean_response(content):

    content = content.strip()

    content = re.sub(
        r"^```json",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"^```",
        "",
        content
    )

    content = re.sub(
        r"```$",
        "",
        content
    )

    return content.strip()


# =========================
# 调用大模型
# =========================

def extract_entities(case_text, api_key, base_url, model_name):

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        case_text=case_text
    )

    try:

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content

        return clean_response(result)

    except Exception as e:

        print(f"API调用失败: {e}")
        return None


# =========================
# 保存JSON
# =========================

def save_json(result_text):

    try:

        result_json = json.loads(result_text)

        with open(
            OUTPUT_JSON,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result_json,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"抽取完成，结果已保存到 {OUTPUT_JSON}"
        )

    except json.JSONDecodeError as e:

        print("返回内容不是合法JSON")

        print(e)

        print("\n模型返回内容：\n")

        print(result_text)

    except Exception as e:

        print(f"保存失败: {e}")


# =========================
# 主函数
# =========================

def main():
    
    print("="*30)
    print(" API 防泄漏配置向导")
    print("="*30)
    
    # 1. 输入 API Key (使用 getpass 隐藏输入字符)
    api_key = getpass.getpass("1. 请输入您的 API Key (输入时不可见，按回车确认): ").strip()
    if not api_key:
        print("错误：API Key 不能为空，程序退出。")
        return
        
    # 2. 输入 Base URL
    base_url = input("2. 请输入 API 调用链接 (Base URL，例如 https://api.openai.com/v1): ").strip()
    if not base_url:
        print("错误：调用链接不能为空，程序退出。")
        return
        
    # 3. 输入 Model Name
    model_name = input("3. 请输入模型类别 (Model Name，例如 gpt-3.5-turbo): ").strip()
    if not model_name:
        print("错误：模型类别不能为空，程序退出。")
        return

    print("\n配置完成！")
    print("-" * 30)
    print("开始读取PDF...")

    case_text = read_pdf(PDF_PATH)

    if not case_text:

        return

    print("PDF读取成功")

    print("开始调用模型...")

    # 将用户输入的参数传递给调用函数
    result_text = extract_entities(case_text, api_key, base_url, model_name)

    if not result_text:

        return

    save_json(result_text)


if __name__ == "__main__":
    main()
