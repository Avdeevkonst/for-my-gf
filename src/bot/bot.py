from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.bot.handlers.commands import router as command_router
from src.bot.handlers.content import router as content_router
from src.bot.middlewares.db import DatabaseMiddleware
from src.config.settings import settings

# Replace with your bot token
BOT_TOKEN = settings.BOT_TOKEN


async def get_bot() -> Bot:
    return Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)


async def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    # Add middleware
    dp.update.middleware(DatabaseMiddleware())

    # Include routers
    dp.include_router(command_router)
    dp.include_router(content_router)

    return dp
