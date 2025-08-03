import os
import requests
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def test_api_token():
    """测试 Replicate API Token 是否有效"""
    token = os.getenv("REPLICATE_API_TOKEN")
    
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
    else:
        print("\n💡 请检查：")
        print("1. .env 文件中的 Token 是否正确")
        print("2. 网络连接是否正常")
        print("3. Token 是否有效") 