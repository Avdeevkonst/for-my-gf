from aiogram import Bot, Dispatcher
from loguru import logger

from src.bot.handlers.commands import router as command_router
from src.bot.handlers.content import router as content_router
from src.bot.middlewares.db import DatabaseMiddleware
from src.config.settings import settings


async def get_bot() -> Bot:
    return Bot(token=settings.BOT_TOKEN)


async def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    # Add middleware
    dp.update.middleware(DatabaseMiddleware())

    # Include routers
    dp.include_router(command_router)
    ""
    dp.include_router(content_router)

    return dp


async def start_bot_polling() -> None:
    """Start bot in polling mode."""
    bot = await get_bot()
    dp = await get_dispatcher()

    # Start polling
    await dp.start_polling(bot)
    logger.info("Bot started in polling mode")
