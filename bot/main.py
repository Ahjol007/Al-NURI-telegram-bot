import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import AsyncSessionLocal, init_db
from middlewares.user_tracker import UserTrackerMiddleware
from handlers import start, menu, products, prices, consultation, reviews, contact, ai_chat, admin

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

WEBHOOK_PATH = f"/webhook/{settings.bot_token}"
WEBHOOK_URL = f"{settings.webhook_base_url}{WEBHOOK_PATH}"


async def on_startup(bot: Bot) -> None:
    await init_db()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logger.info(f"Webhook set: {WEBHOOK_URL}")


async def on_shutdown(bot: Bot) -> None:
    logger.info("Bot shutting down")


def create_app() -> web.Application:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    async def session_middleware(handler, event, data):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)

    dp.update.outer_middleware(session_middleware)
    dp.message.middleware(UserTrackerMiddleware())
    dp.callback_query.middleware(UserTrackerMiddleware())

    # Register routers — ai_chat MUST be last (catch-all)
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(products.router)
    dp.include_router(prices.router)
    dp.include_router(consultation.router)
    dp.include_router(reviews.router)
    dp.include_router(contact.router)
    dp.include_router(ai_chat.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    application = create_app()
    web.run_app(application, host="0.0.0.0", port=port)
