from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    DATABASE_URL_DIRECT: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DBPASS: str = ""
    DB_HOST: str = ""
    DB_NAME: str = ""
    JWT_SECRET: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = {"env_file": ".env"}

    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip().strip("'\"")
        return v

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        password = self.DB_PASSWORD or self.DBPASS
        return f"postgresql+asyncpg://{self.DB_USER}:{password}@{self.DB_HOST}/{self.DB_NAME}?ssl=require"


settings = Settings()
