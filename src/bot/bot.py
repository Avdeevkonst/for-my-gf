from aiogram import Bot, Dispatcher, types
from loguru import logger

from src.bot.handlers.commands import router as command_router
from src.config.settings import settings


async def get_bot() -> Bot:
    return Bot(token=settings.BOT_TOKEN)


async def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    # Include routers
    dp.include_router(command_router)

    return dp


async def start_bot_polling() -> None:
    """Start bot in polling mode."""
    bot = await get_bot()
    dp = await get_dispatcher()

    # Start polling
    await set_default_commands(bot)
    await dp.start_polling(bot)
    logger.info("Bot started in polling mode")


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Start the bot"),
            types.BotCommand(command="help", description="Help"),
            types.BotCommand(command="add_content", description="Add content"),
            types.BotCommand(command="list_content", description="List content"),
            types.BotCommand(command="run", description="Start the content"),
            types.BotCommand(command="set_content_owner", description="Set content owner"),
            types.BotCommand(command="reset", description="Reset the content"),
            types.BotCommand(command="private", description="Get private access"),
        ]
    )
