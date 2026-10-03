from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    APP_NAME: str = 'AgriPulse-Ai'
    APP_VERSION: str = '1.0.0'
    ENVIRONMENT: str = Field('development', env='ENVIRONMENT')
    DEBUG: bool = Field(True, env='DEBUG')
    API_V1_PREFIX: str = '/api/v1'
    
    DATABASE_URL: str = Field('sqlite+aiosqlite:///./agripulse.db', env='DATABASE_URL')
    DB_ECHO: bool = Field(False, env='DB_ECHO')
    REDIS_URL: str = Field('redis://localhost:6379/0', env='REDIS_URL')
    
    SECRET_KEY: str = Field('your-super-secret-key', env='SECRET_KEY')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: List[str] = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:8080',
        'http://localhost:5000',
    ]
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str): return [i.strip() for i in v.split(',')]
        return v

    OPENAI_API_KEY: Optional[str] = None
    WEATHER_API_KEY: Optional[str] = None

    CHROMA_PERSIST_DIR: str = './vector_store/chroma_db'
    CHROMA_COLLECTION_NAME: str = 'agri_knowledge'
    EMBEDDING_MODEL: str = 'all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION: int = 384
    # Vision Settings
    # Vision Settings
    VISION_MODEL_PATH: str = Field('./ai_models/plant_disease_model.keras', env='VISION_MODEL_PATH')
    VISION_MODEL_URL: str = Field('', env='VISION_MODEL_URL')

    ADMIN_EMAIL: str = 'admin@agripulse.com'
    ADMIN_PASSWORD: str = 'Admin@123'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
