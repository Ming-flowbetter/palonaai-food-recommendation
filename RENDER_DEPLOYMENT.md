# Render部署指南 - PalonaAI菜品推荐系统

## 🚀 部署步骤

### 第一步：准备GitHub仓库

1. **在GitHub上创建新仓库**
   - 访问 https://github.com
   - 点击 "New repository"
   - 仓库名称：`palonaai-food-recommendation`
   - 选择 "Public" 或 "Private"
   - 不要初始化README（因为我们已经有了）

2. **推送代码到GitHub**
   ```bash
   # 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
   git remote add origin https://github.com/YOUR_USERNAME/palonaai-food-recommendation.git
   
   # 推送代码
   git push -u origin master
   ```

### 第二步：在Render上创建服务

1. **登录Render**
   - 访问 https://render.com
   - 使用GitHub账户登录

2. **创建新Web服务**
   - 点击 "New +" 按钮
   - 选择 "Web Service"
   - 连接您的GitHub账户（如果还没有连接）

3. **配置服务**
   - **Repository**: 选择 `palonaai-food-recommendation`
   - **Name**: `palonaai-food-recommendation`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
     ```
   - **Start Command**: 
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

### 第三步：配置环境变量

在Render服务设置中添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | `YOUR_OPENAI_API_KEY_HERE` | OpenAI API密钥 |
| `PINECONE_API_KEY` | `YOUR_PINECONE_API_KEY_HERE` | Pinecone API密钥 |
| `PINECONE_ENVIRONMENT` | `us-east-1` | Pinecone环境 |
| `PINECONE_INDEX_NAME` | `foodaiagent` | Pinecone索引名称 |
| `APP_NAME` | `PalonaAI菜品推荐` | 应用名称 |
| `DEBUG` | `False` | 调试模式 |

### 第四步：部署配置

1. **自动部署设置**
   - 启用 "Auto-Deploy"
   - 选择 "Deploy from master branch"

2. **高级设置**
   - **Health Check Path**: `/`
   - **Health Check Timeout**: 180 seconds

### 第五步：开始部署

1. 点击 "Create Web Service"
2. Render将自动开始构建和部署
3. 构建过程大约需要5-10分钟

## 🔧 故障排除

### 常见问题

1. **构建失败**
   - 检查Node.js版本（需要18.x）
   - 确保所有依赖都正确安装
   - 查看构建日志中的错误信息

2. **环境变量问题**
   - 确保所有必需的API密钥都已设置
   - 检查变量名是否正确

3. **端口问题**
   - Render会自动设置`$PORT`环境变量
   - 确保应用监听在`0.0.0.0:$PORT`

### 查看日志

在Render控制台中：
1. 点击您的服务
2. 进入 "Logs" 标签
3. 查看实时日志和错误信息

## 📝 部署后验证

部署成功后，您应该能够：

1. **访问前端页面**: `https://your-app-name.onrender.com/`
2. **访问API文档**: `https://your-app-name.onrender.com/docs`
3. **测试API端点**: `https://your-app-name.onrender.com/api/health`

## 🔄 更新部署

每次推送代码到master分支时，Render会自动重新部署：

```bash
git add .
git commit -m "Update: 描述您的更改"
git push origin master
```

## 💡 提示

- Render免费计划有使用限制，适合测试和演示
- 生产环境建议使用付费计划
- 定期检查API密钥的有效性
- 监控应用性能和错误日志

## 🎯 成功部署后

您的PalonaAI菜品推荐系统将在以下地址可用：
- **生产URL**: `https://palonaai-food-recommendation.onrender.com`
- **API文档**: `https://palonaai-food-recommendation.onrender.com/docs`

恭喜！您的AI菜品推荐系统已成功部署到云端！🎉 