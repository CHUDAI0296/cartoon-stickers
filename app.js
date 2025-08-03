const express = require('express');
const path = require('path');
const Replicate = require('replicate');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// 中间件
app.use(express.json());
app.use(express.static('public'));
app.use('/static', express.static('static'));

// 检查 API Token
const REPLICATE_API_TOKEN = process.env.REPLICATE_API_TOKEN;
if (!REPLICATE_API_TOKEN) {
    console.error('❌ REPLICATE_API_TOKEN 未在 .env 文件中找到');
    process.exit(1);
}

// 初始化 Replicate
const replicate = new Replicate({
    auth: REPLICATE_API_TOKEN,
});

// 路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/generate', async (req, res) => {
    try {
        const { prompt } = req.body;
        
        if (!prompt) {
            return res.status(400).json({ error: '请输入提示词' });
        }
        
        console.log(`开始生成贴纸: ${prompt}`);
        
        // 调用 Replicate API
        const output = await replicate.run(
            "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            {
                input: {
                    prompt: prompt,
                    output_format: "webp",
                    steps: 17,
                    output_quality: 100,
                    negative_prompt: "racist, xenophobic, antisemitic, islamophobic, bigoted"
                }
            }
        );
        
        console.log('贴纸生成成功:', output);
        
        res.json({
            success: true,
            image_url: output,
            prompt: prompt
        });
        
    } catch (error) {
        console.error('生成失败:', error);
        res.status(500).json({ 
            error: '生成失败，请重试',
            details: error.message 
        });
    }
});

app.listen(port, () => {
    console.log(`🚀 贴纸生成器运行在 http://localhost:${port}`);
    console.log(`✅ API Token: ${REPLICATE_API_TOKEN.substring(0, 10)}...`);
}); 