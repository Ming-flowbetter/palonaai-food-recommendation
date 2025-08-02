#!/bin/bash

echo "🚀 启动AI餐厅推荐系统..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 创建虚拟环境
echo "📦 设置Python环境..."
python3 -m venv venv
source venv/bin/activate

# 安装后端依赖
echo "🔧 安装后端依赖..."
cd backend
pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "🔧 安装前端依赖..."
cd frontend
npm install
cd ..

# 构建前端
echo "🏗️ 构建前端..."
cd frontend
npm run build
cd ..

# 创建环境变量文件
echo "⚙️ 创建环境变量文件..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "✅ 环境变量文件已创建，请编辑 backend/.env 文件配置您的API密钥"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 下一步："
echo "1. 编辑 backend/.env 文件，配置您的API密钥"
echo "2. 运行后端服务器: cd backend && uvicorn main:app --reload"
echo "3. 在另一个终端运行前端: cd frontend && npm start"
echo ""
echo "🌐 或者使用Docker: docker-compose up --build" 