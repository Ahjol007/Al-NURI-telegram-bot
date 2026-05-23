import logging

import httpx
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.models import MessageLog, User

router = Router()
logger = logging.getLogger(__name__)


async def _get_message_history(session: AsyncSession, user_id: int) -> list[dict]:
    result = await session.execute(
        select(MessageLog)
        .where(MessageLog.user_id == user_id)
        .order_by(desc(MessageLog.created_at))
        .limit(10)
    )
    logs = result.scalars().all()
    return [{"direction": m.direction, "text": m.message_text} for m in reversed(logs)]


@router.message(StateFilter(default_state), F.text)
async def handle_ai_chat(message: Message, session: AsyncSession, db_user: User, lang: str):
    # Fetch history BEFORE adding the current message to avoid duplicating it in context
    history = await _get_message_history(session, db_user.id)

    in_log = MessageLog(
        user_id=db_user.id,
        message_text=message.text,
        direction="in",
    )
    session.add(in_log)
    await session.flush()

    try:
        async with httpx.AsyncClient(timeout=35.0) as client:
            resp = await client.post(
                f"{settings.ai_service_url}/chat",
                json={
                    "user_id": db_user.id,
                    "message": message.text,
                    "history": history,
                    "language": lang,
                },
            )
            resp.raise_for_status()
            reply_text = resp.json().get("reply", "...")
    except Exception as e:
        logger.error(f"AI service error: {e}")
        reply_text = (
            "Кешіріңіз, қазір жауап бере алмаймын. WhatsApp-қа жазыңыз: https://wa.me/77778151988"
            if lang == "kk"
            else "Извините, сейчас не могу ответить. Пишите в WhatsApp: https://wa.me/77778151988"
        )

    out_log = MessageLog(
        user_id=db_user.id,
        message_text=reply_text,
        direction="out",
    )
    session.add(out_log)
    await session.commit()

    await message.answer(reply_text)
