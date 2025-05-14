import sys
import json
import google.generativeai as genai

if len(sys.argv) < 3:
    print("Usage: python check_translation.py en.json es.json")
    sys.exit(1)

en_file = sys.argv[1]
es_file = sys.argv[2]

try:
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    with open(es_file, 'r', encoding='utf-8') as f:
        es_data = json.load(f)
except Exception as e:
    print(f"Error reading files: {e}")
    sys.exit(1)



genai.configure(api_key="AIzaSyCAHToUqHhbicFwniR5HZIFVpsd6AQsWeY")
model = genai.GenerativeModel('gemini-2.0-flash')


prompt = f"""
You are a multi-language translation quality checker. Please check if there are any problems with the translation of the following two JSON language files.
Please indicate in your answer:
1. Which keys exist in English but are missing in Spanish, or vice versa;
2. Which values ​​are empty;
3. Are the placeholders consistent (e.g. {{name}}, {{count}}）；
4. If there are any obviously unreasonable or wrong translations, please point them out.

English (en.json) content:
{json.dumps(en_data, indent=2, ensure_ascii=False)}

Spanish (es.json) content:
{json.dumps(es_data, indent=2, ensure_ascii=False)}
"""

response = model.generate_content(prompt)
print(response.text.strip())
with open("result.md", "w", encoding="utf-8") as f:
    f.write(response.text.strip())

