const express = require('express');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const app = express();

// 中间件
app.use(express.json());
app.use(express.static('public'));
app.use('/static', express.static('public/static'));

// 检查 API Token
const REPLICATE_API_TOKEN = process.env.REPLICATE_API_TOKEN;
if (!REPLICATE_API_TOKEN) {
    console.error('❌ REPLICATE_API_TOKEN 未在 .env 文件中找到');
}

// 路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

app.post('/generate', async (req, res) => {
    try {
        const { prompt } = req.body;
        
        if (!prompt) {
            return res.status(400).json({ error: '请输入提示词' });
        }
        
        console.log(`开始生成贴纸: ${prompt}`);
        
        // 直接调用 Replicate API
        const headers = {
            "Authorization": `Token ${REPLICATE_API_TOKEN}`,
            "Content-Type": "application/json"
        };
        
        const payload = {
            "version": "4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            "input": {
                "prompt": prompt,
                "output_format": "webp",
                "steps": 17,
                "output_quality": 100,
                "negative_prompt": "racist, xenophobic, antisemitic, islamophobic, bigoted"
            }
        };
        
        // 创建预测
        const response = await axios.post(
            "https://api.replicate.com/v1/predictions",
            payload,
            { headers }
        );
        
        if (response.status !== 201) {
            return res.status(500).json({ error: 'API 调用失败' });
        }
        
        const prediction = response.data;
        const predictionId = prediction.id;
        
        // 等待预测完成
        while (true) {
            const statusResponse = await axios.get(
                `https://api.replicate.com/v1/predictions/${predictionId}`,
                { headers }
            );
            
            if (statusResponse.status !== 200) {
                return res.status(500).json({ error: '获取预测状态失败' });
            }
            
            const statusData = statusResponse.data;
            
            if (statusData.status === 'succeeded') {
                const outputUrl = statusData.output;
                console.log('贴纸生成成功:', outputUrl);
                
                res.json({
                    success: true,
                    image_url: outputUrl,
                    prompt: prompt
                });
                return;
                
            } else if (statusData.status === 'failed') {
                return res.status(500).json({ error: '贴纸生成失败' });
            }
            
            // 等待 2 秒后重试
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
        
    } catch (error) {
        console.error('生成失败:', error);
        res.status(500).json({ 
            error: '生成失败，请重试',
            details: error.message 
        });
    }
});

module.exports = app;