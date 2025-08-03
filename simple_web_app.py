from flask import Flask, render_template, request, jsonify
import replicate
import os
import requests
import uuid

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
        
        # 调用 Replicate API
        output = replicate.run(
            "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            input={
                "prompt": prompt,
                "output_format": "webp",
                "steps": 17,
                "output_quality": 100,
                "negative_prompt": "racist, xenophobic, antisemitic, islamophobic, bigoted"
            }
        )
        
        print(f"贴纸生成成功: {output}")
        
        # 下载图片到本地
        filename = f"static/stickers/{uuid.uuid4()}.webp"
        os.makedirs("static/stickers", exist_ok=True)
        
        response = requests.get(output)
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return jsonify({
            'success': True,
            'image_url': f'/{filename}',
            'original_url': output
        })
        
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