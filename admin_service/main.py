import asyncio
import logging
import os

import httpx
from fastapi import FastAPI, Request
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from admin_service.db_queries import (
    get_stats,
    get_recent_users,
    get_new_consultations,
    get_all_user_telegram_ids,
)
from admin_service.broadcaster import broadcast_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str
    admin_telegram_id: int
    database_url: str


settings = Settings()
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI(title="Al-NURI Admin Service")


async def send_message(chat_id: int, text: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            )
            if resp.status_code != 200:
                logger.error(f"Telegram sendMessage failed {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"send_message error: {e}")


async def _do_broadcast(admin_id: int, telegram_ids: list[int], text: str) -> None:
    count = await broadcast_message(settings.bot_token, telegram_ids, text)
    await send_message(admin_id, f"✅ Рассылка аяқталды: {count} пайдаланушыға жіберілді")


@app.post("/admin-webhook")
async def admin_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    from_id = message.get("from", {}).get("id")
    text = message.get("text", "").strip()

    if not from_id or from_id != settings.admin_telegram_id:
        return {"ok": True}

    reply = "Белгісіз команда. /admin_help жазыңыз."

    try:
        async with AsyncSessionLocal() as session:
            if text == "/admin_help":
                reply = (
                    "Admin командалары:\n"
                    "/admin_stats — Статистика\n"
                    "/admin_users — Соңғы 10 пайдаланушы\n"
                    "/admin_consults — Жаңа өтінімдер\n"
                    "/admin_broadcast <мәтін> — Барлық пайдаланушыларға жіберу"
                )

            elif text == "/admin_stats":
                stats = await get_stats(session)
                reply = (
                    f"📊 Статистика:\n"
                    f"Пайдаланушылар: {stats['total_users']}\n"
                    f"Жаңа өтінімдер: {stats['new_consultations']}"
                )

            elif text == "/admin_users":
                users = await get_recent_users(session)
                if not users:
                    reply = "Пайдаланушылар жоқ."
                else:
                    lines = []
                    for u in users:
                        name = u["first_name"] or "N/A"
                        uname = f"@{u['username']}" if u["username"] else "N/A"
                        date = u["created_at"].strftime("%d.%m.%Y") if u["created_at"] else "N/A"
                        lines.append(f"{name} ({uname}) — {date}")
                    reply = "👥 Соңғы 10 пайдаланушы:\n" + "\n".join(lines)

            elif text == "/admin_consults":
                consults = await get_new_consultations(session)
                if not consults:
                    reply = "Жаңа өтінім жоқ."
                else:
                    lines = []
                    for c in consults:
                        symptoms = (c["symptoms"] or "N/A")[:50]
                        lines.append(f"#{c['id']} | {c['age'] or 'N/A'} жас | {symptoms}")
                    reply = "📋 Жаңа өтінімдер:\n" + "\n".join(lines)

            elif text.startswith("/admin_broadcast "):
                broadcast_text = text[len("/admin_broadcast "):]
                if not broadcast_text.strip():
                    reply = "Хабар мәтінін енгізіңіз: /admin_broadcast <мәтін>"
                else:
                    telegram_ids = await get_all_user_telegram_ids(session)
                    asyncio.create_task(_do_broadcast(from_id, telegram_ids, broadcast_text))
                    reply = f"Рассылка басталды ({len(telegram_ids)} пайдаланушы)..."

    except Exception as e:
        logger.error(f"Admin webhook DB error: {e}")
        reply = "Қате орын алды. Кейінірек қайталаңыз."

    await send_message(from_id, reply)
    return {"ok": True}


@app.get("/health")
async def health():
    return {"status": "ok"}
