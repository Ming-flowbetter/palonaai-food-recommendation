from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.schemas import (
    ChatMessage, ChatResponse, MenuItem, SearchRequest, 
    SearchResponse, RecommendationRequest, RecommendationResponse, SessionInfo,
    UserFeedback, ConversationMetrics, IntentAnalysis, EmotionAnalysis, EntityExtraction
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
    """与AI助手对话（增强版，带意图和情感分析）"""
    try:
        result = await ai_service.chat(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")

@api_router.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """获取会话信息（增强版）"""
    try:
        session_info = ai_service.get_session_info(session_id)
        if not session_info:
            raise HTTPException(status_code=404, detail="会话不存在")
        return SessionInfo(**session_info)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话信息失败: {str(e)}")

@api_router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """清除会话"""
    try:
        success = ai_service.clear_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="会话不存在")
        return {"message": "会话已清除", "session_id": session_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除会话失败: {str(e)}")

@api_router.post("/cleanup-sessions")
async def cleanup_old_sessions(max_age_hours: int = 24):
    """清理过期会话"""
    try:
        cleaned_count = ai_service.cleanup_old_sessions(max_age_hours)
        return {
            "message": f"已清理 {cleaned_count} 个过期会话",
            "max_age_hours": max_age_hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清理会话失败: {str(e)}")

@api_router.post("/analyze-intent")
async def analyze_intent(message: str):
    """分析用户意图"""
    try:
        intent_scores = ai_service._detect_intent(message)
        return {
            "message": message,
            "intent_scores": intent_scores,
            "primary_intent": max(intent_scores.items(), key=lambda x: x[1])[0] if intent_scores else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"意图分析失败: {str(e)}")

@api_router.post("/analyze-emotion")
async def analyze_emotion(message: str):
    """分析用户情感"""
    try:
        emotion_scores = ai_service._analyze_emotion(message)
        return {
            "message": message,
            "emotion_scores": emotion_scores,
            "primary_emotion": max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"情感分析失败: {str(e)}")

@api_router.post("/extract-entities")
async def extract_entities(message: str):
    """提取实体信息"""
    try:
        entities = ai_service._extract_entities(message)
        return {
            "message": message,
            "entities": entities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"实体提取失败: {str(e)}")

@api_router.post("/feedback")
async def submit_feedback(feedback: UserFeedback):
    """提交用户反馈"""
    try:
        # 这里可以添加反馈处理逻辑
        # 例如保存到数据库、更新AI模型等
        return {
            "message": "反馈已提交",
            "session_id": feedback.session_id,
            "rating": feedback.rating,
            "feedback_type": feedback.feedback_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交反馈失败: {str(e)}")

@api_router.get("/conversation-metrics/{session_id}")
async def get_conversation_metrics(session_id: str):
    """获取对话指标"""
    try:
        session_info = ai_service.get_session_info(session_id)
        if not session_info:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 计算对话指标
        metrics = {
            "session_id": session_id,
            "total_messages": session_info.get("conversation_length", 0),
            "user_satisfaction_score": 0.0,  # 可以从反馈计算
            "average_response_time": 0.0,  # 可以从日志计算
            "intent_accuracy": 0.0,  # 可以从历史计算
            "emotion_recognition_accuracy": 0.0,  # 可以从历史计算
            "created_at": session_info.get("created_at"),
            "updated_at": session_info.get("last_activity")
        }
        
        return ConversationMetrics(**metrics)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话指标失败: {str(e)}")

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
    except HTTPException:
        raise
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
    """获取个性化推荐（增强版）"""
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
        "service": "PalonaAI菜品推荐系统",
        "version": "2.0.0",
        "features": [
            "智能对话",
            "意图识别",
            "情感分析",
            "实体提取",
            "个性化推荐",
            "用户反馈"
        ]
    } 