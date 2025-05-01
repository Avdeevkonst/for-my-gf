from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.utils.db import get_or_create_user

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message, session: AsyncSession):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    user = await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await message.answer(f"Привет, {user.first_name}! Я бот для работы с контентом.")
