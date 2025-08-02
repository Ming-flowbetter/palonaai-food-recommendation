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

class RecommendationResponse(BaseModel):
    recommendations: List[MenuItem]
    reasoning: str
    confidence_score: float 