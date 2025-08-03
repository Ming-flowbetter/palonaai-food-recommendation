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