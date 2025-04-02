from flask import Flask, request, jsonify
import requests  # 使用 requests 库调用 DeepSeek API

app = Flask(__name__)

# DeepSeek API 配置
# ✅ 改为从环境变量读取
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 从云平台的环境变量注入
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # 检查 DeepSeek 官方文档确认最新地址

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message', '')

    # 调用 DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",  # 确认 DeepSeek 支持的模型名称
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 检查 HTTP 错误
        ai_response = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
