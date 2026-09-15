from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./test.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 150

    class Config:
        env_file = ".env"

settings = Settings()