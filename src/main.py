import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.models import ContentAdmin, UserAdmin
from src.bot.bot import start_bot_polling
from src.database.config import dbconfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    task = asyncio.create_task(start_bot_polling())

    logger.info("Application started successfully")
    yield

    try:
        await task
    except asyncio.CancelledError:
        logger.info("Bot polling task cancelled")

    logger.info("Application stopped successfully")


app = FastAPI(lifespan=lifespan)

# Initialize admin interface
admin = Admin(
    app,
    dbconfig.engine,
    authentication_backend=authentication_backend,
    title="Content Management",
)

# Add model views
admin.add_view(UserAdmin)
admin.add_view(ContentAdmin)
