import openai
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from typing import List, Dict, Any, Optional
import json
import uuid
import re
from datetime import datetime, timedelta
from app.core.config import settings

class AIService:
    def __init__(self):
        # 检查API密钥是否设置
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            self.client = None
            self.chat_model = None
            print("Warning: OpenAI API key not set. Using fallback AI responses.")
        else:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            self.chat_model = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                openai_api_key=settings.OPENAI_API_KEY
            )
        
        # 用户会话存储 - 在生产环境中应该使用数据库
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        
        # 意图识别关键词
        self.intent_keywords = {
            "recommendation": ["推荐", "建议", "吃什么", "选择", "点菜"],
            "information": ["介绍", "说明", "详情", "特点", "营养"],
            "comparison": ["比较", "对比", "哪个好", "区别"],
            "preference": ["喜欢", "偏好", "口味", "习惯"],
            "health": ["健康", "营养", "卡路里", "减肥", "养生"],
            "allergy": ["过敏", "忌口", "不能吃", "安全"],
            "seasonal": ["当季", "季节", "新鲜", "时令"],
            "budget": ["价格", "便宜", "贵", "预算", "经济"]
        }
        
        # 情感分析关键词
        self.emotion_keywords = {
            "positive": ["喜欢", "好吃", "满意", "推荐", "棒", "赞"],
            "negative": ["难吃", "失望", "不好", "差", "讨厌"],
            "neutral": ["一般", "还行", "普通", "正常"],
            "excited": ["兴奋", "期待", "激动", "迫不及待"],
            "worried": ["担心", "忧虑", "害怕", "紧张"]
        }
        
        # 系统提示词
        self.system_prompt = """你是一个专业的PalonaAI菜品推荐助手。你的任务是：

1. 理解用户的需求和偏好
2. 根据用户的喜好推荐合适的菜品
3. 考虑季节性因素和营养健康
4. 提供个性化的建议和详细说明
5. 回答用户关于菜品的问题
6. 记住用户的偏好和之前的对话内容
7. 识别用户的意图和情感状态
8. 提供多角度的推荐理由

请用中文回复，保持友好和专业的语气。记住用户的偏好，在后续对话中提供更个性化的建议。

回复格式要求：
- 保持对话的自然流畅
- 提供具体的菜品推荐和理由
- 考虑用户的健康需求和饮食限制
- 适时询问更多信息以提供更精准的推荐"""

    def _detect_intent(self, message: str) -> Dict[str, float]:
        """检测用户意图"""
        message_lower = message.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score / len(keywords)
        
        return intent_scores

    def _analyze_emotion(self, message: str) -> Dict[str, float]:
        """分析用户情感"""
        message_lower = message.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                emotion_scores[emotion] = score / len(keywords)
        
        return emotion_scores

    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """提取实体信息"""
        entities = {
            "cuisine_types": [],
            "taste_preferences": [],
            "dietary_restrictions": [],
            "budget_range": None,
            "meal_type": None,
            "cooking_method": None
        }
        
        # 菜系类型
        cuisine_patterns = {
            "chinese": ["中餐", "中国菜", "川菜", "粤菜", "湘菜", "鲁菜"],
            "western": ["西餐", "意大利", "法国", "美式", "pizza", "pasta"],
            "japanese": ["日料", "日本", "寿司", "刺身", "拉面"],
            "korean": ["韩料", "韩国", "烤肉", "泡菜"],
            "thai": ["泰餐", "泰国", "冬阴功", "咖喱"],
            "indian": ["印度", "咖喱", "香料"]
        }
        
        for cuisine, patterns in cuisine_patterns.items():
            if any(pattern in message for pattern in patterns):
                entities["cuisine_types"].append(cuisine)
        
        # 口味偏好
        taste_patterns = {
            "spicy": ["辣", "麻辣", "重口味", "香辣"],
            "mild": ["清淡", "不辣", "原味", "养生"],
            "sweet": ["甜", "糖醋", "蜜汁"],
            "sour": ["酸", "醋", "柠檬"],
            "bitter": ["苦", "苦瓜", "咖啡"]
        }
        
        for taste, patterns in taste_patterns.items():
            if any(pattern in message for pattern in patterns):
                entities["taste_preferences"].append(taste)
        
        # 饮食限制
        restriction_patterns = {
            "vegetarian": ["素食", "不吃肉", "蔬菜"],
            "vegan": ["纯素", "不吃蛋奶"],
            "gluten_free": ["无麸质", "麸质过敏"],
            "dairy_free": ["无乳糖", "乳糖不耐"],
            "nut_free": ["坚果过敏", "不吃坚果"],
            "seafood_free": ["海鲜过敏", "不吃海鲜"]
        }
        
        for restriction, patterns in restriction_patterns.items():
            if any(pattern in message for pattern in patterns):
                entities["dietary_restrictions"].append(restriction)
        
        # 预算范围
        budget_patterns = {
            "low": ["便宜", "经济", "实惠", "平价"],
            "medium": ["中等", "适中", "一般"],
            "high": ["高档", "豪华", "精致", "贵"]
        }
        
        for budget, patterns in budget_patterns.items():
            if any(pattern in message for pattern in patterns):
                entities["budget_range"] = budget
                break
        
        return entities

    def _get_or_create_session(self, session_id: str, user_id: str = None) -> Dict[str, Any]:
        """获取或创建用户会话"""
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "conversation_history": [],
                "user_preferences": {},
                "interaction_count": 0,
                "intent_history": [],
                "emotion_history": [],
                "entity_history": []
            }
        else:
            # 更新最后活动时间
            self.user_sessions[session_id]["last_activity"] = datetime.now()
            self.user_sessions[session_id]["interaction_count"] += 1
        
        return self.user_sessions[session_id]

    def _update_user_preferences(self, session_id: str, message: str, ai_response: str, entities: Dict[str, Any]):
        """更新用户偏好（增强版）"""
        session = self.user_sessions[session_id]
        preferences = session.get("user_preferences", {})
        
        # 更新菜系偏好
        if entities.get("cuisine_types"):
            preferences["cuisine_preferences"] = entities["cuisine_types"]
        
        # 更新口味偏好
        if entities.get("taste_preferences"):
            if "taste_preferences" not in preferences:
                preferences["taste_preferences"] = []
            preferences["taste_preferences"].extend(entities["taste_preferences"])
            preferences["taste_preferences"] = list(set(preferences["taste_preferences"]))
        
        # 更新饮食限制
        if entities.get("dietary_restrictions"):
            preferences["dietary_restrictions"] = entities["dietary_restrictions"]
        
        # 更新预算偏好
        if entities.get("budget_range"):
            preferences["budget_preference"] = entities["budget_range"]
        
        # 检测其他偏好
        message_lower = message.lower()
        
        # 检测用餐时间
        if any(word in message_lower for word in ['早餐', '早上', '早饭']):
            preferences["meal_time"] = "breakfast"
        elif any(word in message_lower for word in ['午餐', '中午', '午饭']):
            preferences["meal_time"] = "lunch"
        elif any(word in message_lower for word in ['晚餐', '晚上', '晚饭']):
            preferences["meal_time"] = "dinner"
        
        # 检测用餐人数
        people_match = re.search(r'(\d+)个人?', message)
        if people_match:
            preferences["group_size"] = int(people_match.group(1))
        
        # 检测特殊场合
        if any(word in message_lower for word in ['约会', '情侣', '浪漫']):
            preferences["occasion"] = "romantic"
        elif any(word in message_lower for word in ['聚会', '朋友', '庆祝']):
            preferences["occasion"] = "party"
        elif any(word in message_lower for word in ['商务', '工作', '会议']):
            preferences["occasion"] = "business"
        
        session["user_preferences"] = preferences

    def _build_conversation_context(self, session_id: str) -> str:
        """构建对话上下文（增强版）"""
        session = self.user_sessions[session_id]
        context = self.system_prompt
        
        # 添加用户偏好信息
        preferences = session.get("user_preferences", {})
        if preferences:
            context += f"\n\n用户偏好信息：{json.dumps(preferences, ensure_ascii=False)}"
        
        # 添加意图历史
        intent_history = session.get("intent_history", [])
        if intent_history:
            recent_intents = intent_history[-5:]  # 最近5个意图
            context += f"\n\n最近的用户意图：{recent_intents}"
        
        # 添加情感历史
        emotion_history = session.get("emotion_history", [])
        if emotion_history:
            recent_emotions = emotion_history[-5:]  # 最近5个情感
            context += f"\n\n最近的情感状态：{recent_emotions}"
        
        # 添加对话历史摘要（最近3轮）
        history = session.get("conversation_history", [])
        if len(history) > 0:
            recent_history = history[-6:]  # 最近3轮对话（6条消息）
            context += "\n\n最近的对话历史："
            for msg in recent_history:
                context += f"\n{msg['role']}: {msg['content']}"
        
        return context

    async def chat(self, message: str, session_id: str = None, user_id: str = None, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理用户对话（增强版）"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # 获取或创建会话
        session = self._get_or_create_session(session_id, user_id)
        
        # 分析用户输入
        intent_scores = self._detect_intent(message)
        emotion_scores = self._analyze_emotion(message)
        entities = self._extract_entities(message)
        
        # 更新会话历史
        session["intent_history"].append(intent_scores)
        session["emotion_history"].append(emotion_scores)
        session["entity_history"].append(entities)
        
        # 检查AI服务是否可用
        if not self.chat_model:
            # 使用智能fallback回复
            fallback_response = self._get_enhanced_fallback_response(message, session, intent_scores, emotion_scores, entities)
            return {
                "response": fallback_response,
                "recommendations": [],
                "session_id": session_id,
                "user_preferences": session.get("user_preferences", {}),
                "conversation_length": len(session.get("conversation_history", [])),
                "intent_scores": intent_scores,
                "emotion_scores": emotion_scores,
                "entities": entities
            }
        
        # 构建对话上下文
        context = self._build_conversation_context(session_id)
        
        # 创建消息列表
        messages = [SystemMessage(content=context)]
        
        # 添加历史对话（最多10轮）
        history = session.get("conversation_history", [])
        for msg in history[-20:]:  # 最多20条历史消息
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # 添加当前用户消息
        messages.append(HumanMessage(content=message))
        
        try:
            # 获取AI回复
            response = self.chat_model.invoke(messages)
            
            # 更新对话历史
            session["conversation_history"].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat(),
                "intent_scores": intent_scores,
                "emotion_scores": emotion_scores,
                "entities": entities
            })
            session["conversation_history"].append({
                "role": "assistant",
                "content": response.content,
                "timestamp": datetime.now().isoformat()
            })
            
            # 更新用户偏好
            self._update_user_preferences(session_id, message, response.content, entities)
            
            # 解析回复，提取推荐信息
            recommendations = self._extract_recommendations(response.content)
            
            return {
                "response": response.content,
                "recommendations": recommendations,
                "session_id": session_id,
                "user_preferences": session.get("user_preferences", {}),
                "conversation_length": len(session.get("conversation_history", [])),
                "interaction_count": session.get("interaction_count", 0),
                "intent_scores": intent_scores,
                "emotion_scores": emotion_scores,
                "entities": entities
            }
        except Exception as e:
            return {
                "response": f"抱歉，处理您的请求时出现了错误: {str(e)}",
                "recommendations": [],
                "session_id": session_id,
                "user_preferences": session.get("user_preferences", {}),
                "conversation_length": len(session.get("conversation_history", [])),
                "interaction_count": session.get("interaction_count", 0),
                "intent_scores": intent_scores,
                "emotion_scores": emotion_scores,
                "entities": entities
            }

    def _get_enhanced_fallback_response(self, message: str, session: Dict[str, Any], intent_scores: Dict[str, float], emotion_scores: Dict[str, float], entities: Dict[str, Any]) -> str:
        """增强的fallback回复"""
        message_lower = message.lower()
        
        # 获取用户偏好
        preferences = session.get("user_preferences", {})
        
        # 根据意图提供回复
        if intent_scores.get("recommendation", 0) > 0.3:
            return self._get_recommendation_response(preferences, entities, emotion_scores)
        elif intent_scores.get("information", 0) > 0.3:
            return self._get_information_response(message, preferences)
        elif intent_scores.get("comparison", 0) > 0.3:
            return self._get_comparison_response(message, preferences)
        elif intent_scores.get("health", 0) > 0.3:
            return self._get_health_response(message, preferences)
        elif intent_scores.get("allergy", 0) > 0.3:
            return self._get_allergy_response(message, preferences)
        
        # 根据情感提供回复
        if emotion_scores.get("positive", 0) > 0.3:
            return "很高兴您对推荐满意！我可以为您推荐更多类似的菜品，或者根据您的反馈调整推荐策略。"
        elif emotion_scores.get("negative", 0) > 0.3:
            return "抱歉没有满足您的期望。请告诉我您具体不喜欢什么，我会为您推荐更合适的菜品。"
        elif emotion_scores.get("worried", 0) > 0.3:
            return "我理解您的担心。请告诉我您的具体顾虑，比如过敏、健康需求或预算限制，我会为您提供更安全的推荐。"
        
        # 基础关键词匹配
        return self._get_fallback_response(message, session)

    def _get_recommendation_response(self, preferences: Dict[str, Any], entities: Dict[str, Any], emotion_scores: Dict[str, float]) -> str:
        """获取推荐回复"""
        response_parts = []
        
        # 根据菜系偏好
        if entities.get("cuisine_types"):
            cuisines = entities["cuisine_types"]
            if "chinese" in cuisines:
                response_parts.append("中餐推荐：麻婆豆腐、宫保鸡丁、水煮鱼")
            if "western" in cuisines:
                response_parts.append("西餐推荐：意大利面、牛排、披萨")
            if "japanese" in cuisines:
                response_parts.append("日料推荐：三文鱼刺身、天妇罗、拉面")
        
        # 根据口味偏好
        if entities.get("taste_preferences"):
            tastes = entities["taste_preferences"]
            if "spicy" in tastes:
                response_parts.append("重口味推荐：辣子鸡、水煮鱼、麻婆豆腐")
            if "mild" in tastes:
                response_parts.append("清淡推荐：白切鸡、蒸蛋羹、清炒时蔬")
        
        # 根据预算
        if entities.get("budget_range"):
            budget = entities["budget_range"]
            if budget == "low":
                response_parts.append("经济实惠推荐：家常菜、小炒、汤品")
            elif budget == "high":
                response_parts.append("高档精致推荐：海鲜、牛排、特色菜")
        
        if response_parts:
            return "根据您的偏好，" + "；".join(response_parts) + "。您更倾向于哪种？"
        else:
            return "我推荐您尝试：1. 当季新鲜菜品 2. 经典招牌菜 3. 营养均衡搭配。您有什么特别偏好吗？"

    def _get_information_response(self, message: str, preferences: Dict[str, Any]) -> str:
        """获取信息回复"""
        if any(word in message for word in ['营养', '卡路里', '健康']):
            return "关于营养信息：我们提供详细的营养成分表，包括卡路里、蛋白质、脂肪等。您想了解哪个菜品的营养信息？"
        elif any(word in message for word in ['做法', '烹饪', '制作']):
            return "关于烹饪方法：我们的菜品采用传统工艺和现代技术相结合，确保口感和营养。您对哪种烹饪方式感兴趣？"
        else:
            return "我可以为您提供菜品的详细信息，包括原料、做法、营养价值和特色。您想了解哪个方面？"

    def _get_comparison_response(self, message: str, preferences: Dict[str, Any]) -> str:
        """获取比较回复"""
        return "我可以帮您比较不同菜品的特点，包括口味、营养、价格等方面。您想比较哪些菜品？"

    def _get_health_response(self, message: str, preferences: Dict[str, Any]) -> str:
        """获取健康相关回复"""
        return "健康饮食很重要！我推荐：1. 低脂高蛋白菜品 2. 富含维生素的蔬菜 3. 全谷物主食。您有特殊的健康需求吗？"

    def _get_allergy_response(self, message: str, preferences: Dict[str, Any]) -> str:
        """获取过敏相关回复"""
        return "安全第一！我们提供详细的过敏原信息，包括常见过敏原如坚果、海鲜、乳制品等。请告诉我您的过敏情况，我会为您推荐安全的菜品。"

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
            response = self.chat_model.invoke([HumanMessage(content=prompt)])
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

    def _get_fallback_response(self, message: str, session: Dict[str, Any] = None) -> str:
        """智能fallback回复（带记忆）"""
        message_lower = message.lower()
        
        # 获取用户偏好
        preferences = session.get("user_preferences", {}) if session else {}
        
        # 根据用户偏好定制回复
        if preferences.get("taste_preference") == "spicy":
            if any(word in message_lower for word in ['推荐', '建议', '吃什么']):
                return "根据您之前提到的重口味偏好，我推荐：1. 水煮鱼 - 麻辣鲜香，2. 辣子鸡 - 香辣可口，3. 麻婆豆腐 - 经典川菜。这些都很符合您的口味！"
        
        elif preferences.get("taste_preference") == "mild":
            if any(word in message_lower for word in ['推荐', '建议', '吃什么']):
                return "根据您之前提到的清淡偏好，我推荐：1. 白切鸡 - 清淡鲜美，2. 蒸蛋羹 - 营养丰富，3. 清炒时蔬 - 健康美味。这些都很适合您的口味！"
        
        # 基础关键词匹配
        if any(word in message_lower for word in ['你好', 'hi', 'hello']):
            return "你好！欢迎使用PalonaAI菜品推荐系统！我是您的智能菜品助手，可以帮您推荐最适合的菜品。请告诉我您喜欢什么口味或者有什么特殊需求？"
        
        elif any(word in message_lower for word in ['中餐', '中国菜', '川菜', '粤菜']):
            return "中餐是个很棒的选择！我推荐您尝试：1. 麻婆豆腐 - 麻辣鲜香，2. 宫保鸡丁 - 经典川菜，3. 白切鸡 - 清淡鲜美。您更喜欢哪种口味？"
        
        elif any(word in message_lower for word in ['西餐', '意大利', 'pizza', 'pasta']):
            return "西餐很有情调！我推荐：1. 意大利面 - 经典美味，2. 披萨 - 多种口味，3. 牛排 - 鲜嫩多汁。您想要什么风格？"
        
        elif any(word in message_lower for word in ['日料', '日本', '寿司', '刺身']):
            return "日料很精致！推荐：1. 三文鱼刺身 - 新鲜美味，2. 天妇罗 - 酥脆可口，3. 拉面 - 温暖舒适。您喜欢生食还是熟食？"
        
        elif any(word in message_lower for word in ['辣', '麻辣', '重口味']):
            return "喜欢重口味！推荐：1. 水煮鱼 - 麻辣鲜香，2. 辣子鸡 - 香辣可口，3. 麻婆豆腐 - 经典川菜。您能接受多辣？"
        
        elif any(word in message_lower for word in ['清淡', '不辣', '养生']):
            return "清淡养生很好！推荐：1. 白切鸡 - 清淡鲜美，2. 蒸蛋羹 - 营养丰富，3. 清炒时蔬 - 健康美味。您有什么忌口吗？"
        
        elif any(word in message_lower for word in ['推荐', '建议', '吃什么']):
            return "根据当前季节，我推荐：1. 当季新鲜蔬菜 - 营养丰富，2. 温补汤品 - 养生保健，3. 应季水果 - 补充维生素。您有什么特别偏好吗？"
        
        else:
            return "感谢您的咨询！我是PalonaAI菜品推荐助手，可以为您推荐最适合的菜品。请告诉我您的口味偏好、饮食限制或者想要尝试的菜系，我会为您提供个性化推荐！"

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """获取会话信息"""
        if session_id in self.user_sessions:
            session = self.user_sessions[session_id]
            return {
                "session_id": session_id,
                "user_id": session.get("user_id"),
                "created_at": session.get("created_at").isoformat(),
                "last_activity": session.get("last_activity").isoformat(),
                "conversation_length": len(session.get("conversation_history", [])),
                "interaction_count": session.get("interaction_count", 0),
                "user_preferences": session.get("user_preferences", {})
            }
        return {}

    def clear_session(self, session_id: str) -> bool:
        """清除会话"""
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]
            return True
        return False

    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """清理过期会话"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        expired_sessions = [
            session_id for session_id, session in self.user_sessions.items()
            if session["last_activity"] < cutoff_time
        ]
        for session_id in expired_sessions:
            del self.user_sessions[session_id]
        return len(expired_sessions) 