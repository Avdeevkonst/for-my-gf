from aiogram import F, Router, types
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.utils.db import get_or_create_user
from src.database.models import Content

router = Router()


@router.message(Command("add_content"))
async def add_content_command(message: types.Message, session: AsyncSession):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await message.answer(
        "Пожалуйста, отправьте контент в формате:\n"
        "Шаг: [номер от 1 до 20]\n"
        "Контент: [ваш контент]\n"
        "Сообщение: [ваше сообщение]"
    )


@router.message(F.text.startswith("Шаг:"))
async def process_content(message: types.Message, session: AsyncSession):
    if not message.from_user or not message.text:
        await message.answer("Ошибка: не удалось получить информацию о сообщении")
        return

    try:
        lines = message.text.split("\n")
        if len(lines) != 3:
            raise ValueError("Неверный формат")

        step = int(lines[0].replace("Шаг:", "").strip())
        content_text = lines[1].replace("Контент:", "").strip()
        message_text = lines[2].replace("Сообщение:", "").strip()

        if not (1 <= step <= 20):
            raise ValueError("Номер шага должен быть от 1 до 20")

        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        content = Content(
            content=content_text,
            step_number=step,
            message=message_text,
            user_id=user.id,
        )
        session.add(content)
        await session.commit()

        await message.answer("Контент успешно добавлен!")

    except (ValueError, IndexError):
        await message.answer(
            "Ошибка в формате. Пожалуйста, используйте формат:\n"
            "Шаг: [номер от 1 до 20]\n"
            "Контент: [ваш контент]\n"
            "Сообщение: [ваше сообщение]"
        )


@router.message(Command("list_content"))
async def list_content_command(message: types.Message, session: AsyncSession):
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

    query = select(Content).where(Content.user_id == user.id).order_by(Content.step_number)
    result = await session.execute(query)
    contents = result.scalars().all()

    if not contents:
        await message.answer("У вас пока нет добавленного контента.")
        return

    response = "Ваш контент:\n\n"
    for content in contents:
        response += f"Шаг {content.step_number}:\n"
        response += f"Контент: {content.content}\n"
        response += f"Сообщение: {content.message}\n\n"

    await message.answer(response)
