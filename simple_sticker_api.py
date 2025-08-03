import replicate
import requests
import base64
from PIL import Image
import io

# 设置你的 Replicate API Token
REPLICATE_API_TOKEN = "your_api_token_here"

def generate_sticker(prompt):
    """
    使用 Replicate API 生成贴纸
    """
    try:
        # 调用 fofr/sticker-maker 模型
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
        
        print(f"生成的贴纸 URL: {output}")
        return output
        
    except Exception as e:
        print(f"生成失败: {e}")
        return None

def download_sticker(url, filename):
    """
    下载贴纸图片
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"贴纸已保存为: {filename}")
        
    except Exception as e:
        print(f"下载失败: {e}")

if __name__ == "__main__":
    # 测试生成贴纸
    prompt = "cute cat sticker"
    sticker_url = generate_sticker(prompt)
    
    if sticker_url:
        download_sticker(sticker_url, "generated_sticker.webp") 