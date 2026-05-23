from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str
    admin_telegram_id: int
    database_url: str
    ai_service_url: str
    webhook_base_url: str


settings = Settings()
