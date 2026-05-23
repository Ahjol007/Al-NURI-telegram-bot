from typing import Any, Awaitable, Callable, Dict
from datetime import datetime, timezone

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


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

            lang = "kk" if tg_user.language_code == "kk" else "ru"

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
                user.last_active = datetime.now(timezone.utc)
                user.username = tg_user.username
                user.language_code = lang

            # Assign data keys BEFORE commit to avoid MissingGreenlet on attribute access
            data["db_user"] = user
            data["lang"] = lang

            await session.commit()

        return await handler(event, data)
