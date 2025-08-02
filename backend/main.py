from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from app.api.routes import api_router
from app.core.config import settings

# 加载环境变量
load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI餐厅推荐系统API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix="/api")

# 定义主页HTML内容
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>PalonaAI菜品推荐</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .api-link { display: block; margin: 10px 0; padding: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; text-align: center; }
        .api-link:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>PalonaAI菜品推荐系统</h1>
        <p style="text-align: center; color: #666;">欢迎使用PalonaAI菜品推荐系统！</p>
        <a href="/docs" class="api-link">📚 API文档</a>
        <a href="/health" class="api-link">❤️ 健康检查</a>
        <a href="/api/menu" class="api-link">🍽️ 菜单API</a>
        <p style="text-align: center; margin-top: 30px; color: #999;">
            AI驱动的智能菜品推荐系统
        </p>
    </div>
</body>
</html>"""

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return html_content

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PalonaAI菜品推荐系统", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 