import sys
import json
import google.generativeai as genai


if len(sys.argv) < 2:
    print("Usage: python translate_json.py en.json")
    sys.exit(1)

en_file = sys.argv[1]


try:
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)


genai.configure(api_key="AIzaSyCAHToUqHhbicFwniR5HZIFVpsd6AQsWeY")  
model = genai.GenerativeModel('gemini-2.0-flash')  


prompt = f"""
You are a professional translation assistant. Please translate the value of the following JSON object from English to Spanish, but do not modify the key.
Please return a JSON format object, keep the structure unchanged, and only translate the value to Spanish.

Original JSON:
{json.dumps(en_data, indent=2, ensure_ascii=False)}
"""


response = model.generate_content(prompt)
translated_text = response.text.strip()


try:
    start_index = translated_text.find('{')
    end_index = translated_text.rfind('}') + 1
    json_str = translated_text[start_index:end_index]
    es_data = json.loads(json_str)
except Exception as e:
    print(f"Error parsing response JSON: {e}")
    print("Original response content：")
    print(translated_text)
    sys.exit(1)


es_file = en_file.replace('.json', '_es.json')
with open(es_file, 'w', encoding='utf-8') as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)

print(f"Translation completed, output file：{es_file}")
