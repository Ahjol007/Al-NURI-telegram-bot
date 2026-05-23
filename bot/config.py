from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    admin_telegram_id: int
    database_url: str
    ai_service_url: str
    webhook_base_url: str

    class Config:
        env_file = ".env"


settings = Settings()
