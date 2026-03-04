from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Transport_company_project'
    DEBUG: bool 

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCES_TOKEN_EXPIRE_MINUTES: int

    LOG_DIR: str

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None 
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None 

    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive=True
    )

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

@lru_cache
def get_settings() -> Settings:
    return Settings

settings = get_settings()