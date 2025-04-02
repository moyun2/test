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
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not DEEPSEEK_API_KEY:
            return jsonify({"error": "API key not configured"}), 500

        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_message}]
        }

        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()  # 检查HTTP错误
        return jsonify({"response": response.json()["choices"][0]["message"]["content"]})

    except requests.exceptions.RequestException as e:
        # 捕获所有requests库的异常
        return jsonify({
            "error": "DeepSeek API请求失败",
            "details": str(e),
            "api_key_configured": bool(DEEPSEEK_API_KEY)  # 检查密钥是否加载
        }), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
