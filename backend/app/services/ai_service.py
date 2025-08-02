import openai
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional
import json
import uuid
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # 系统提示词
        self.system_prompt = """你是一个专业的PalonaAI菜品推荐助手。你的任务是：

1. 理解用户的需求和偏好
2. 根据用户的喜好推荐合适的菜品
3. 考虑季节性因素
4. 提供个性化的建议
5. 回答用户关于菜品的问题

请用中文回复，保持友好和专业的语气。"""

    async def chat(self, message: str, session_id: str = None, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理用户对话"""
        if not session_id:
            session_id = str(uuid.uuid4())
            
        # 构建上下文
        context = self._build_context(user_preferences)
        
        # 创建消息
        messages = [
            SystemMessage(content=self.system_prompt + "\n" + context),
            HumanMessage(content=message)
        ]
        
        try:
            # 获取AI回复
            response = self.chat_model(messages)
            
            # 解析回复，提取推荐信息
            recommendations = self._extract_recommendations(response.content)
            
            return {
                "response": response.content,
                "recommendations": recommendations,
                "session_id": session_id
            }
        except Exception as e:
            return {
                "response": f"抱歉，处理您的请求时出现了错误: {str(e)}",
                "recommendations": [],
                "session_id": session_id
            }

    def _build_context(self, user_preferences: Dict[str, Any] = None) -> str:
        """构建用户上下文"""
        context = "当前可用的菜品类别包括：中餐、西餐、日料、韩料、泰餐、意餐等。"
        
        if user_preferences:
            context += f"\n用户偏好：{json.dumps(user_preferences, ensure_ascii=False)}"
            
        # 添加季节性信息
        import datetime
        current_month = datetime.datetime.now().month
        seasonal_foods = self._get_seasonal_foods(current_month)
        context += f"\n当前季节推荐：{seasonal_foods}"
        
        return context

    def _get_seasonal_foods(self, month: int) -> str:
        """获取季节性食材"""
        seasonal_map = {
            1: "冬季：火锅、炖菜、热汤",
            2: "冬季：火锅、炖菜、热汤",
            3: "春季：春笋、野菜、清淡菜品",
            4: "春季：春笋、野菜、清淡菜品",
            5: "春季：春笋、野菜、清淡菜品",
            6: "夏季：凉菜、冷面、清爽菜品",
            7: "夏季：凉菜、冷面、清爽菜品",
            8: "夏季：凉菜、冷面、清爽菜品",
            9: "秋季：秋蟹、栗子、温补菜品",
            10: "秋季：秋蟹、栗子、温补菜品",
            11: "秋季：秋蟹、栗子、温补菜品",
            12: "冬季：火锅、炖菜、热汤"
        }
        return seasonal_map.get(month, "当季新鲜食材")

    def _extract_recommendations(self, response: str) -> List[Dict[str, Any]]:
        """从AI回复中提取推荐信息"""
        # 这里可以添加更复杂的推荐提取逻辑
        # 目前返回空列表，可以在后续版本中完善
        return []

    async def get_recommendations(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """获取个性化推荐"""
        prompt = f"""
        基于以下用户偏好，推荐3-5道最适合的菜品：
        
        用户偏好：{json.dumps(user_preferences, ensure_ascii=False)}
        
        请提供：
        1. 推荐的菜品名称
        2. 推荐理由
        3. 预期满意度评分（1-10）
        """
        
        try:
            response = self.chat_model([HumanMessage(content=prompt)])
            return {
                "recommendations": self._parse_recommendations(response.content),
                "reasoning": response.content,
                "confidence_score": 0.8
            }
        except Exception as e:
            return {
                "recommendations": [],
                "reasoning": f"推荐生成失败: {str(e)}",
                "confidence_score": 0.0
            }

    def _parse_recommendations(self, content: str) -> List[Dict[str, Any]]:
        """解析推荐内容"""
        # 这里可以添加更复杂的解析逻辑
        # 目前返回示例数据
        return [
            {
                "name": "示例菜品",
                "description": "这是一个示例推荐",
                "rating": 8.5,
                "reason": "基于您的偏好推荐"
            }
        ] 