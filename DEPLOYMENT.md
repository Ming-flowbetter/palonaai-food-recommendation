# 部署指南

## 本地开发

### 1. 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 2. 快速启动
```bash
# 使用启动脚本（Linux/Mac）
chmod +x start.sh
./start.sh

# 或使用Windows批处理文件
start.bat
```

### 3. 手动启动
```bash
# 1. 安装后端依赖
cd backend
pip install -r requirements.txt

# 2. 配置环境变量
cp env.example .env
# 编辑 .env 文件，填入您的API密钥

# 3. 启动后端服务器
uvicorn main:app --reload

# 4. 在另一个终端安装前端依赖
cd frontend
npm install

# 5. 启动前端开发服务器
npm start
```

## Render部署

### 1. 准备部署
1. 将代码推送到GitHub仓库
2. 在Render创建新的Web Service
3. 连接您的GitHub仓库

### 2. 配置环境变量
在Render控制台中设置以下环境变量：
- `OPENAI_API_KEY`: 您的OpenAI API密钥
- `PINECONE_API_KEY`: 您的Pinecone API密钥
- `PINECONE_ENVIRONMENT`: us-east-1
- `PINECONE_INDEX_NAME`: foodaiagent
- `APP_NAME`: AI餐厅推荐系统
- `DEBUG`: False

### 3. 构建配置
- **构建命令**: `pip install -r backend/requirements.txt && cd frontend && npm install && npm run build`
- **启动命令**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. 部署
1. 点击"Deploy"按钮
2. 等待构建完成
3. 访问您的应用URL

## Docker部署

### 1. 使用Docker Compose
```bash
# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

### 2. 使用Dockerfile
```bash
# 构建镜像
docker build -t ai-restaurant-app .

# 运行容器
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  ai-restaurant-app
```

## 环境变量配置

### 必需的环境变量
```env
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key

# Pinecone配置
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=foodaiagent

# 应用配置
APP_NAME=AI餐厅推荐系统
DEBUG=False
```

## 故障排除

### 常见问题

1. **Docker构建失败 - "frontend/build: not found"**
   - **原因**: Dockerfile试图复制不存在的frontend/build目录
   - **解决方案**: 已更新Dockerfile，现在会在构建过程中安装Node.js并构建前端
   - **验证**: 运行 `python test_docker.py` 测试Docker构建

2. **前端无法连接后端**
   - 检查后端服务器是否运行在正确的端口
   - 确认CORS配置正确
   - 检查API URL配置

3. **API密钥错误**
   - 确认环境变量已正确设置
   - 检查API密钥是否有效
   - 确认API配额充足

4. **构建失败**
   - 检查Node.js和Python版本
   - 确认所有依赖已正确安装
   - 查看构建日志获取详细错误信息

5. **Docker容器启动失败**
   - 检查端口是否被占用: `docker ps`
   - 查看容器日志: `docker logs <container_name>`
   - 确认环境变量已正确传递

6. **Windows环境编码问题**
   - 使用 `python test_docker_simple.py` 或 `test_docker.bat`
   - 确保Docker Desktop正在运行
   - 检查Windows终端编码设置

7. **前端构建失败 - "Can't resolve './App'"**
   - **原因**: 缺少TypeScript配置文件或文件路径问题
   - **解决方案**: 已添加`tsconfig.json`文件，更新了Dockerfile
   - **验证**: 运行 `python debug_frontend.py` 检查前端构建

### 日志查看
```bash
# 查看应用日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f ai-restaurant-app
```

## 性能优化

### 生产环境建议
1. 使用Gunicorn作为WSGI服务器
2. 配置Nginx作为反向代理
3. 启用HTTPS
4. 设置适当的缓存策略
5. 监控应用性能

### 扩展性考虑
1. 使用Redis进行会话存储
2. 配置数据库连接池
3. 实现负载均衡
4. 设置自动扩缩容 