from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    recommendations: Optional[List[Dict[str, Any]]] = None
    session_id: str
    user_preferences: Optional[Dict[str, Any]] = None
    conversation_length: Optional[int] = 0
    interaction_count: Optional[int] = 0
    intent_scores: Optional[Dict[str, float]] = None
    emotion_scores: Optional[Dict[str, float]] = None
    entities: Optional[Dict[str, Any]] = None

class SessionInfo(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: str
    last_activity: str
    conversation_length: int
    interaction_count: int
    user_preferences: Dict[str, Any]
    intent_history: Optional[List[Dict[str, float]]] = None
    emotion_history: Optional[List[Dict[str, float]]] = None
    entity_history: Optional[List[Dict[str, Any]]] = None

class IntentAnalysis(BaseModel):
    intent: str
    confidence: float
    keywords: List[str]

class EmotionAnalysis(BaseModel):
    emotion: str
    intensity: float
    keywords: List[str]

class EntityExtraction(BaseModel):
    cuisine_types: List[str] = []
    taste_preferences: List[str] = []
    dietary_restrictions: List[str] = []
    budget_range: Optional[str] = None
    meal_type: Optional[str] = None
    cooking_method: Optional[str] = None

class ConversationAnalysis(BaseModel):
    intent_analysis: IntentAnalysis
    emotion_analysis: EmotionAnalysis
    entity_extraction: EntityExtraction

class MenuItem(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    ingredients: List[str]
    allergens: List[str]
    image_url: Optional[str] = None
    is_seasonal: bool = False
    rating: float = 0.0
    nutrition_info: Optional[Dict[str, Any]] = None
    cooking_method: Optional[str] = None
    spice_level: Optional[int] = None
    preparation_time: Optional[int] = None

class Restaurant(BaseModel):
    id: str
    name: str
    cuisine_type: str
    location: str
    rating: float
    price_range: str
    description: str
    menu_items: List[MenuItem]

class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10

class SearchResponse(BaseModel):
    results: List[MenuItem]
    total_count: int
    query: str

class RecommendationRequest(BaseModel):
    user_preferences: Dict[str, Any]
    dietary_restrictions: Optional[List[str]] = None
    budget_range: Optional[str] = None
    cuisine_preferences: Optional[List[str]] = None
    meal_time: Optional[str] = None
    group_size: Optional[int] = None
    occasion: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[MenuItem]
    reasoning: str
    confidence_score: float
    personalized_factors: Optional[List[str]] = None

class UserFeedback(BaseModel):
    session_id: str
    message_id: str
    rating: int  # 1-5
    feedback_type: str  # "positive", "negative", "neutral"
    comment: Optional[str] = None
    timestamp: datetime

class ConversationMetrics(BaseModel):
    session_id: str
    total_messages: int
    user_satisfaction_score: float
    average_response_time: float
    intent_accuracy: float
    emotion_recognition_accuracy: float
    created_at: datetime
    updated_at: datetime 