import sys
import json
import google.generativeai as genai

# 检查是否提供了输入文件
if len(sys.argv) < 2:
    print("Usage: python translate_json.py en.json")
    sys.exit(1)

en_file = sys.argv[1]

# 读取英文 JSON 文件
try:
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# 配置 API 密钥
genai.configure(api_key="AIzaSyCAHToUqHhbicFwniR5HZIFVpsd6AQsWeY")  # 请替换为你自己的 API 密钥
model = genai.GenerativeModel('gemini-2.0-flash')  # 使用更强的模型进行翻译

# 构建翻译提示
prompt = f"""
你是一个专业的翻译助手。请将以下 JSON 对象的 value 从英文翻译为西班牙语，但不要修改 key。
请返回一个 JSON 格式对象，保持结构不变，仅将 value 翻译为西班牙语。

原始 JSON:
{json.dumps(en_data, indent=2, ensure_ascii=False)}
"""

# 获取翻译结果
response = model.generate_content(prompt)
translated_text = response.text.strip()

# 尝试将返回的内容转换为 JSON
try:
    start_index = translated_text.find('{')
    end_index = translated_text.rfind('}') + 1
    json_str = translated_text[start_index:end_index]
    es_data = json.loads(json_str)
except Exception as e:
    print(f"Error parsing response JSON: {e}")
    print("原始响应内容：")
    print(translated_text)
    sys.exit(1)

# 写入西班牙语 JSON 文件
es_file = en_file.replace('.json', '_es.json')
with open(es_file, 'w', encoding='utf-8') as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)

print(f"翻译完成，输出文件：{es_file}")
