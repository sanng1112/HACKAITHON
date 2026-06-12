"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "GovOne"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://govone:govone@localhost:5432/govone"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://govone:govone@localhost:5432/govone"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    VNPT_API_KEY: str = ""
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
