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

# 挂载静态文件（用于前端构建文件）
# 注意：在生产环境中，前端文件应该被构建并复制到后端目录
static_dir = "static"
if not os.path.exists(static_dir):
    print(f"Warning: Static directory '{static_dir}' does not exist. Creating empty directory.")
    os.makedirs(static_dir, exist_ok=True)
    # 创建一个简单的index.html作为fallback
    with open(os.path.join(static_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>PalonaAI菜品推荐</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>PalonaAI菜品推荐系统</h1>
    <p>欢迎使用PalonaAI菜品推荐系统！</p>
    <p>API文档: <a href="/docs">/docs</a></p>
    <p>健康检查: <a href="/health">/health</a></p>
    <p>菜单API: <a href="/api/menu">/api/menu</a></p>
</body>
</html>
        """)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
async def root():
    return {"message": "欢迎使用AI餐厅推荐系统"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PalonaAI菜品推荐系统", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 