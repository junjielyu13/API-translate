import sys
import json
import google.generativeai as genai

# 确保传入两个文件路径
if len(sys.argv) < 3:
    print("Usage: python check_translation.py en.json es.json")
    sys.exit(1)

en_file = sys.argv[1]
es_file = sys.argv[2]

# 读取 JSON 文件
try:
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    with open(es_file, 'r', encoding='utf-8') as f:
        es_data = json.load(f)
except Exception as e:
    print(f"Error reading files: {e}")
    sys.exit(1)

# print("es JSON 内容：" + es_data.__str__() )
# print("英文 JSON 内容：" + en_data.__str__() )


# 配置 API 密钥
genai.configure(api_key="AIzaSyCAHToUqHhbicFwniR5HZIFVpsd6AQsWeY")
model = genai.GenerativeModel('gemini-2.0-flash')

# 构建提示内容
prompt = f"""
你是一个多语言翻译质量检查员。请检查以下两个 JSON 语言文件的翻译是否存在问题。
请回答中指出：
1. 哪些 key 在英文中存在但在西班牙文中缺失，或反之；
2. 哪些值为空；
3. 占位符是否一致（如 {{name}}, {{count}}）；
4. 如有明显不合理或错误的翻译，也请指出。

英文（en.json）内容：
{json.dumps(en_data, indent=2, ensure_ascii=False)}

德语（es.json）内容：
{json.dumps(es_data, indent=2, ensure_ascii=False)}
"""

response = model.generate_content(prompt)
print(response.text.strip())

