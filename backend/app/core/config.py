from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "PalonaAI菜品推荐"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-here"
    
    # OpenAI配置
    OPENAI_API_KEY: str = ""
    
    # Pinecone配置
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "foodaiagent"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./foodaiagent.db"
    
    # API配置
    API_V1_STR: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings() 