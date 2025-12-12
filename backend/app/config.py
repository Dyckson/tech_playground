"""
Configurações da aplicação
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações do sistema"""
    
    # API
    API_TITLE: str = "Tech Playground API"
    API_VERSION: str = "2.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "tech_user"
    DB_PASSWORD: str = "tech_password"
    DB_NAME: str = "tech_playground"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
