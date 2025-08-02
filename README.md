# AI餐厅推荐系统

一个基于AI的智能餐厅推荐系统，为用户提供个性化的菜品推荐和餐厅建议。

## 功能特性

- 🤖 **智能对话推荐**: 基于用户偏好的个性化菜品推荐
- 🍽️ **季节性菜单建议**: 根据时令提供最佳菜品选择
- 🔍 **可搜索产品目录**: 快速查找和筛选菜品
- 💬 **自然语言交互**: 支持中文对话，理解用户需求
- 🎯 **个性化体验**: 根据用户喜好和餐厅偏好进行推荐

## 技术栈

### 后端
- **Python FastAPI**: 高性能API框架
- **OpenAI GPT API**: 智能对话和推荐引擎
- **Pinecone**: 向量数据库，用于相似性搜索
- **LangChain**: AI应用编排框架
- **SQLite**: 本地数据存储

### 前端
- **React**: 用户界面框架
- **TypeScript**: 类型安全
- **Tailwind CSS**: 现代化样式
- **Axios**: HTTP客户端

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd hw-ai-agent
```

2. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
```

3. **安装前端依赖**
```bash
cd frontend
npm install
```

4. **配置环境变量**
```bash
# 在backend目录创建.env文件
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

5. **启动开发服务器**

后端:
```bash
cd backend
uvicorn main:app --reload
```

前端:
```bash
cd frontend
npm start
```

## 环境变量配置

创建 `backend/.env` 文件:

```env
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key

# Pinecone配置
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=foodaiagent

# 应用配置
APP_NAME=AI餐厅推荐系统
DEBUG=True
```

## API文档

启动后端服务器后，访问 `http://localhost:8000/docs` 查看完整的API文档。

### 主要API端点

- `POST /api/chat`: 与AI助手对话
- `GET /api/recommendations`: 获取菜品推荐
- `GET /api/menu`: 获取菜单信息
- `POST /api/search`: 搜索菜品

## 部署

### Docker部署

使用Docker Compose快速部署:

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build

# 停止服务
docker-compose down
```

或者使用Docker直接构建:

```bash
# 构建镜像
docker build -t ai-restaurant-app .

# 运行容器
docker run -p 8000:8000 ai-restaurant-app
```

#### Windows环境测试

如果遇到编码问题，可以使用简化的测试脚本:

```bash
# Windows兼容的测试脚本
python test_docker_simple.py

# 或直接手动构建
docker build -t ai-restaurant-app . --progress=plain
```

#### 前端构建问题排查

如果遇到前端构建错误，可以使用调试脚本:

```bash
# 检查前端文件结构和构建
python debug_frontend.py

# 手动测试前端构建
cd frontend
npm install
npm run build
```

### Render部署

1. 在Render创建新的Web Service
2. 连接你的GitHub仓库
3. 设置环境变量
4. 构建命令: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
5. 启动命令: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 项目结构

```
hw-ai-agent/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── public/
├── README.md
└── docker-compose.yml
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License 