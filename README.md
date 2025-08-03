# PalonaAI菜品推荐系统

一个基于AI的智能菜品推荐系统，为用户提供个性化的菜品推荐和餐厅建议。

## 🌐 线上演示

**访问地址**: [https://palonaai-food-recommendation.onrender.com/](https://palonaai-food-recommendation.onrender.com/)

体验完整的AI菜品推荐功能，包括智能对话、菜单浏览、搜索筛选等。

## 功能特性

-  **智能对话推荐**: 基于用户偏好的个性化菜品推荐
-  **丰富菜品菜单**: 包含经典中餐菜品，涵盖川菜、粤菜、鲁菜等八大菜系
-  **可搜索产品目录**: 快速查找和筛选菜品
-  **自然语言交互**: 支持中文对话，理解用户需求
-  **个性化体验**: 根据用户喜好和餐厅偏好进行推荐

## 技术栈

### 后端
- **FastAPI**: 高性能API框架
- **OpenAI GPT API**: 智能对话和推荐引擎
- **Pinecone**: 向量数据库，用于相似性搜索
- **LangChain**: AI应用编排框架
- **SQLite**: 本地数据存储
- **Pydantic**: 数据验证和设置管理

### 前端
- **React**: 用户界面框架
- **TypeScript**: 类型安全
- **Tailwind CSS**: 现代化样式
- **Axios**: HTTP客户端
- **React Router**: 路由管理
- **Lucide React**: 图标库

## 依赖列表

### 后端依赖 (requirements.txt)
```
fastapi
uvicorn
python-dotenv
openai
pinecone-client
langchain
langchain-openai
langchain-community
pydantic
pydantic-settings
python-multipart
sqlalchemy
aiosqlite
numpy
pandas
requests
python-jose[cryptography]
passlib[bcrypt]
```

### 前端依赖 (package.json)
```json
{
  "dependencies": {
    "@types/node": "^16.18.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.0",
    "axios": "^1.6.0",
    "react-router-dom": "^6.8.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "class-variance-authority": "^0.7.0"
  }
}
```


## API文档

启动后端服务器后，访问 `http://localhost:8000/docs` 查看完整的API文档。
https://palonaai-food-recommendation.onrender.com/docs 线上API文档

### 主要API端点

- `POST /api/chat`: 与AI助手对话
- `GET /api/menu`: 获取菜单信息
- `POST /api/search`: 搜索菜品
- `GET /health`: 健康检查

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

## 许可证

MIT License 