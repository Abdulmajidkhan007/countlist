import asyncio
import logging
import ssl

import certifi
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from bot.config import settings
from bot.database.connection import engine
from bot.handlers import start, expenses, stats, callbacks
from bot.middlewares.db import DbMiddleware
from bot.middlewares.user import UserMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    session = AiohttpSession()
    session._connector_init = {"ssl": ssl_context}  # type: ignore[attr-defined]

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    dp = Dispatcher()

    dp.update.middleware(DbMiddleware())
    dp.update.middleware(UserMiddleware())

    dp.include_router(start.router)
    dp.include_router(expenses.router)
    dp.include_router(stats.router)
    dp.include_router(callbacks.router)

    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
