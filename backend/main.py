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

# 挂载静态文件（React前端）
print("Setting up static files for React frontend...")
static_dir = "static"

# 确保static目录存在
if not os.path.exists(static_dir):
    print(f"Creating static directory: {static_dir}")
    os.makedirs(static_dir, exist_ok=True)
else:
    print(f"Static directory already exists: {static_dir}")

# 检查是否有React构建文件
index_html_path = os.path.join(static_dir, "index.html")
if not os.path.exists(index_html_path):
    print("React build not found, creating fallback index.html")
    fallback_html = """<!DOCTYPE html>
<html>
<head>
    <title>PalonaAI菜品推荐系统</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .api-link { display: block; margin: 10px 0; padding: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; text-align: center; }
        .api-link:hover { background: #0056b3; }
        .status { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>PalonaAI菜品推荐系统</h1>
        <div class="status">
            ✅ 后端服务正常运行！<br>
            ✅ AI聊天功能可用<br>
            ✅ API文档可访问
        </div>
        <p style="text-align: center; color: #666;">欢迎使用PalonaAI菜品推荐系统！</p>
        <a href="/docs" class="api-link">📚 API文档</a>
        <a href="/health" class="api-link">❤️ 健康检查</a>
        <a href="/api/menu" class="api-link">🍽️ 菜单API</a>
        <a href="/api/chat" class="api-link">🤖 AI聊天测试</a>
        <p style="text-align: center; margin-top: 30px; color: #999;">
            AI驱动的智能菜品推荐系统
        </p>
    </div>
</body>
</html>"""
    
    try:
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write(fallback_html)
        print(f"Successfully created fallback index.html at {index_html_path}")
    except Exception as e:
        print(f"Error creating fallback index.html: {e}")
else:
    print(f"React build found at {index_html_path}")

# 挂载静态文件
print(f"Mounting static files from directory: {static_dir}")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
print("Static files mounted successfully")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PalonaAI菜品推荐系统", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 