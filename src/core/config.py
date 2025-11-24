from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    api_base_url: str = "http://localhost:8000"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 1440
    rate_limit: int = 1000


settings = AppSettings()
