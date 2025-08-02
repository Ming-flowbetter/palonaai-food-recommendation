# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 安装系统依赖和Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 复制前端依赖文件
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install

# 复制所有前端源代码（包括所有文件）
COPY frontend/ .

# 验证关键文件是否存在
RUN ls -la src/ && \
    echo "Checking for App.tsx..." && \
    test -f src/App.tsx && \
    echo "Checking for index.tsx..." && \
    test -f src/index.tsx && \
    echo "Checking for components..." && \
    test -d src/components && \
    echo "Checking for pages..." && \
    test -d src/pages && \
    echo "All required files found!"

# 构建前端
RUN npm run build

# 回到主工作目录
WORKDIR /app

# 复制后端依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 复制前端构建文件到静态目录
RUN mkdir -p static && cp -r frontend/build/* ./static/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"] 