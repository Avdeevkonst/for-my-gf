from aiogram import Router, types
from aiogram.filters import Command

from src.bot.utils.db import create_private_access, get_or_create_user, get_private_access

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await message.answer(
        f"Привет, {user.first_name}! Я бот для работы с контентом.\n\n \
        /help - помощь, \
        /private - приватный доступ, \
        /run - запуск контента. "
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n\n"
        "/add_content - добавить новый контент\n"
        "/list_content - просмотреть весь ваш контент\n"
        "/run - начать или продолжить просмотр контента\n"
        "/set_content_owner [ID] - установить владельца контента\n"
        "/reset - сбросить прогресс просмотра\n"
        "/private - получить приватный доступ"
    )


@router.message(Command("private"))
async def cmd_private(message: types.Message):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    private_access = await get_private_access(message.from_user.id)
    if private_access:
        await message.answer("Вы уже имеете приватный доступ")
        return

    private_access = await create_private_access(message.from_user.id)
    await message.answer(f"Приватный доступ успешно создан\n\nКод: {private_access.access_code}")
