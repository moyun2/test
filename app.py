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
        # 添加内存检查（需安装 psutil）
        import psutil
        if psutil.virtual_memory().percent > 90:
            return jsonify({"error": "Server overloaded"}), 503

        # 设置更长的超时时间
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=20  # 延长至20秒
        )
        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({"error": "DeepSeek API timeout"}), 504
    except Exception as e:
        # 记录完整错误日志（关键！）
        app.logger.error(f"API Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal error"}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
