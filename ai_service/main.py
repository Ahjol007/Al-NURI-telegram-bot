from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    gemini_api_key: str


settings = Settings()

app = FastAPI(title="Al-NURI AI Service")


class ChatRequest(BaseModel):
    user_id: int
    message: str
    history: list[dict] = []
    language: str = "ru"


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    from ai_service.gemini_client import get_ai_reply
    reply = await get_ai_reply(
        message=request.message,
        history=request.history,
        lang=request.language,
        api_key=settings.gemini_api_key,
    )
    return ChatResponse(reply=reply)


@app.get("/health")
async def health():
    return {"status": "ok"}
