from typing import Any, Awaitable, Callable, Dict
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User

# Қазақ тіліне тән әріптер (орыс тілінде жоқ)
_KK_CHARS = set("әіңғүұқөһӘІҢҒҮҰҚӨҺ")

# Орыс тіліне тән, қазақ тілінде жоқ немесе сирек кездесетін әріптер
_RU_CHARS = set("ёыъэЁЫЪЭ")


def detect_lang(text: str, fallback: str = "ru") -> str:
    """Мәтін бойынша тілді анықтайды: 'kk' немесе 'ru'."""
    if not text:
        return fallback
    for ch in text:
        if ch in _KK_CHARS:
            return "kk"
        if ch in _RU_CHARS:
            return "ru"
    return fallback


class UserTrackerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = getattr(event, "from_user", None)

        if tg_user is not None and isinstance(event, (Message, CallbackQuery)):
            session: AsyncSession = data["session"]

            # Тіл анықтау: хабарлама мәтіні бойынша, жоқ болса аккаунт тіліне қарайды
            tg_lang_fallback = "ru" if tg_user.language_code in ("ru", "uk", "be") else "kk"
            message_text = event.text if isinstance(event, Message) else None
            lang = detect_lang(message_text, fallback=tg_lang_fallback) if message_text else tg_lang_fallback

            result = await session.execute(
                select(User).where(User.telegram_id == tg_user.id)
            )
            user = result.scalar_one_or_none()

            if user is None:
                user = User(
                    telegram_id=tg_user.id,
                    username=tg_user.username,
                    first_name=tg_user.first_name,
                    language_code=lang,
                )
                session.add(user)
            else:
                user.last_active = datetime.utcnow()
                user.username = tg_user.username
                user.language_code = lang

            # Assign data keys BEFORE commit to avoid MissingGreenlet on attribute access
            data["db_user"] = user
            data["lang"] = lang

            await session.commit()

        return await handler(event, data)
