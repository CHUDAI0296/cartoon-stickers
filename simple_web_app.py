from flask import Flask, render_template, request, jsonify
import os
import requests
import uuid
import json

app = Flask(__name__)

def load_env():
    """直接读取 .env 文件"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except Exception as e:
        print(f"读取 .env 文件时出错: {e}")
    return env_vars

# 从环境变量获取 API Token
env_vars = load_env()
REPLICATE_API_TOKEN = env_vars.get("REPLICATE_API_TOKEN")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_sticker():
    try:
        # 检查 API Token
        if not REPLICATE_API_TOKEN:
            return jsonify({'error': 'API Token 未配置，请检查 .env 文件'}), 500
        
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': '请输入提示词'}), 400
        
        print(f"开始生成贴纸: {prompt}")
        
        # 直接调用 Replicate API
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": "4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            "input": {
                "prompt": prompt,
                "output_format": "webp",
                "steps": 17,
                "output_quality": 100,
                "negative_prompt": "racist, xenophobic, antisemitic, islamophobic, bigoted"
            }
        }
        
        # 创建预测
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 201:
            return jsonify({'error': f'API 调用失败: {response.text}'}), 500
        
        prediction = response.json()
        prediction_id = prediction['id']
        
        # 等待预测完成
        while True:
            status_response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers
            )
            
            if status_response.status_code != 200:
                return jsonify({'error': '获取预测状态失败'}), 500
            
            status_data = status_response.json()
            
            if status_data['status'] == 'succeeded':
                output_url = status_data['output']
                print(f"贴纸生成成功: {output_url}")
                
                # 下载图片到本地
                filename = f"static/stickers/{uuid.uuid4()}.webp"
                os.makedirs("static/stickers", exist_ok=True)
                
                img_response = requests.get(output_url)
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                return jsonify({
                    'success': True,
                    'image_url': f'/{filename}',
                    'original_url': output_url
                })
                
            elif status_data['status'] == 'failed':
                return jsonify({'error': '贴纸生成失败'}), 500
            
            # 等待 2 秒后重试
            import time
            time.sleep(2)
        
    except Exception as e:
        print(f"生成失败: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 贴纸生成器启动中...")
    if REPLICATE_API_TOKEN:
        print(f"✅ API Token: {REPLICATE_API_TOKEN[:10]}...")
    else:
        print("❌ API Token 未找到")
    
    app.run(debug=True, port=5000) 