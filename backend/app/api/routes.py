from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.schemas import (
    ChatMessage, ChatResponse, MenuItem, SearchRequest, 
    SearchResponse, RecommendationRequest, RecommendationResponse
)
from app.services.ai_service import AIService
from app.services.menu_service import MenuService

# 创建路由器
api_router = APIRouter()

# 初始化服务
ai_service = AIService()
menu_service = MenuService()

@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatMessage):
    """与AI助手对话"""
    try:
        result = await ai_service.chat(
            message=request.message,
            session_id=request.session_id,
            user_preferences={}  # 可以从用户会话中获取
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")

@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu():
    """获取完整菜单"""
    try:
        return menu_service.get_all_menu_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜单失败: {str(e)}")

@api_router.get("/menu/{item_id}", response_model=MenuItem)
async def get_menu_item(item_id: str):
    """根据ID获取菜品详情"""
    try:
        item = menu_service.get_menu_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="菜品不存在")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜品详情失败: {str(e)}")

@api_router.post("/search", response_model=SearchResponse)
async def search_menu(request: SearchRequest):
    """搜索菜品"""
    try:
        return menu_service.search_menu_items(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@api_router.get("/categories")
async def get_categories():
    """获取所有菜品类别"""
    try:
        return {"categories": menu_service.get_categories()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取类别失败: {str(e)}")

@api_router.get("/seasonal")
async def get_seasonal_items():
    """获取季节性菜品"""
    try:
        return {"items": menu_service.get_seasonal_items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取季节性菜品失败: {str(e)}")

@api_router.get("/popular")
async def get_popular_items(limit: int = 5):
    """获取热门菜品"""
    try:
        return {"items": menu_service.get_popular_items(limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取热门菜品失败: {str(e)}")

@api_router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """获取个性化推荐"""
    try:
        result = await ai_service.get_recommendations(request.user_preferences)
        return RecommendationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取推荐失败: {str(e)}")

@api_router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "AI餐厅推荐系统",
        "version": "1.0.0"
    } 