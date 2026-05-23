from typing import Any, Awaitable, Callable, Dict
from datetime import datetime, timezone

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import User


class UserTrackerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            session: AsyncSession = data["session"]
            tg_user = event.from_user

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
                if tg_user.username != user.username:
                    user.username = tg_user.username

            await session.commit()
            data["db_user"] = user
            data["lang"] = user.language_code

        return await handler(event, data)
