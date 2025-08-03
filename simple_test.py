import os
import requests

def load_env():
    """直接读取 .env 文件"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ 未找到 .env 文件")
        return {}
    return env_vars

def test_api_token():
    """测试 Replicate API Token 是否有效"""
    env_vars = load_env()
    token = env_vars.get("REPLICATE_API_TOKEN")
    
    if not token:
        print("❌ 未找到 REPLICATE_API_TOKEN")
        return False
    
    print(f"🔍 测试 API Token: {token[:10]}...")
    
    # 测试 API 连接
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 简单的 API 调用测试
        response = requests.get(
            "https://api.replicate.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API Token 有效！")
            return True
        else:
            print(f"❌ API Token 无效，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 网络错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Replicate API Token 测试")
    print("=" * 30)
    
    success = test_api_token()
    
    if success:
        print("\n🎉 可以开始使用贴纸生成功能了！")
        print("下一步：运行 python simple_web_app.py")
    else:
        print("\n💡 请检查：")
        print("1. .env 文件中的 Token 是否正确")
        print("2. 网络连接是否正常")
        print("3. Token 是否有效") 