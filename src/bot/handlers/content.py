from uuid import uuid4

from aiogram import F, types
from aiogram.filters import Command
from aiogram.types import URLInputFile
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.handlers.commands import router
from src.bot.utils.db import create_content, get_content_by_user_and_step, get_or_create_user
from src.storage.database.models import Content
from src.storage.minio import upload_file
from src.storage.redis import get_user_content_owner, get_user_step, set_user_content_owner, set_user_step


@router.message(Command("add_content"))
async def add_content_command(message: types.Message, session: AsyncSession):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await message.answer(
        "Пожалуйста, отправьте фотографию с подписью в формате:\nШаг: [номер от 1 до 20]\nСообщение: [ваше сообщение]"
    )


@router.message(F.photo)
async def process_content(message: types.Message):  # noqa: C901
    if not message.from_user or not message.caption:
        await message.answer("Ошибка: не удалось получить информацию о сообщении или отсутствует подпись к фото")
        return

    try:
        lines = message.caption.split("\n")
        if len(lines) != 2:
            await message.answer(
                "Неверный формат подписи. Пожалуйста, используйте формат:\n"
                "Шаг: [номер от 1 до 20]\n"
                "Сообщение: [ваше сообщение]"
            )
            return

        step = int(lines[0].replace("Шаг:", "").strip())
        message_text = lines[1].replace("Сообщение:", "").strip()
    except (ValueError, IndexError):
        await message.answer(
            "Ошибка в формате подписи. Пожалуйста, используйте формат:\n"
            "Шаг: [номер от 1 до 20]\n"
            "Сообщение: [ваше сообщение]"
        )
        return

    if not (1 <= step <= 20):
        await message.answer("Номер шага должен быть от 1 до 20")
        return

    # Get the largest photo (best quality)
    if not message.photo:
        await message.answer("Ошибка: фотография не найдена")
        return

    photo = message.photo[-1]
    if not message.bot:
        await message.answer("Ошибка: не удалось получить доступ к боту")
        return
    try:
        # Download the photo

        file = await message.bot.get_file(photo.file_id)
        if not file or not file.file_path:
            await message.answer("Ошибка: не удалось получить информацию о файле")
            return

        file_content = await message.bot.download_file(file.file_path)
        if not file_content:
            await message.answer("Ошибка: не удалось загрузить файл")
            return

        # Generate unique filename
        file_ext = file.file_path.split(".")[-1]
        object_name = f"content_{uuid4()}.{file_ext}"

        # Upload to MinIO
        file_url = await upload_file(file_content, object_name)

        # Create user if not exists
        user = await get_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        # Save content to database
        await create_content(user, step, message_text, file_url)

    except HTTPException as e:
        await message.answer(f"Ошибка создания контента: {e.detail!r}")
        return
    else:
        await message.answer("Контент успешно добавлен!")
        await message.answer("Для просмотра всего контента, используйте команду /list_content")
        return


@router.message(Command("list_content"))
async def list_content_command(message: types.Message, session: AsyncSession):
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    user = await get_or_create_user(
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


@router.message(Command("run"))
async def cmd_run(message: types.Message):
    """Start or continue content sequence."""
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    # Get current user
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    # Get content owner (if not set, use current user)
    content_owner_id = await get_user_content_owner(message.from_user.id)
    if content_owner_id:
        content_owner = await get_or_create_user(content_owner_id)
        if not content_owner:
            await message.answer("Ошибка: владелец контента не найден")
            return
    else:
        content_owner = user
        await set_user_content_owner(message.from_user.id, user.telegram_id)

    # Get current step
    current_step = await get_user_step(message.from_user.id)

    # Get content for current step
    content = await get_content_by_user_and_step(content_owner, current_step)

    if content:
        # Send content
        file = URLInputFile(
            url=content.content,
            filename=f"step_{current_step}.jpg",
        )
        await message.answer_photo(file, caption=content.message)

        # Increment step for next time
        await set_user_step(message.from_user.id, current_step + 1)
    else:
        if current_step == 1:
            await message.answer("Контент не найден. Возможно, он еще не был создан.")
        else:
            await message.answer("Поздравляем! Вы прошли весь контент.")
            # Reset step to 1 for next time
            await set_user_step(message.from_user.id, 1)


@router.message(Command("set_content_owner"))
async def set_content_owner_command(message: types.Message):
    """Set content owner for current user."""
    if not message.from_user or not message.text:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    try:
        # Extract owner's telegram ID from command
        command_parts = message.text.split()
        if len(command_parts) != 2:
            raise ValueError("Invalid command format")
        owner_id = int(command_parts[1])
    except (ValueError, TypeError, IndexError):
        await message.answer(
            "Пожалуйста, укажите ID владельца контента после команды.\nНапример: /set_content_owner 123456789"
        )
        return

    # Check if owner exists
    owner = await get_or_create_user(owner_id)
    if not owner:
        await message.answer("Пользователь с указанным ID не найден")
        return

    # Set owner and reset step
    await set_user_content_owner(message.from_user.id, owner_id)
    await set_user_step(message.from_user.id, 1)
    await message.answer(
        f"Установлен новый владелец контента: {owner.first_name or 'Неизвестно'} "
        f"(@{owner.username or 'Неизвестно'})\n"
        "Используйте /run для просмотра контента"
    )


@router.message(Command("reset"))
async def reset_progress(message: types.Message):
    """Reset progress to step 1."""
    if not message.from_user:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return

    await set_user_step(message.from_user.id, 1)
    await message.answer("Прогресс сброшен. Используйте /run для начала просмотра")
