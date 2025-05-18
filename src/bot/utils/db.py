from sqlalchemy import select

from src.storage.database.config import PgUnitOfWork
from src.storage.database.models import Content, PrivateAccess, User

# TODO: refactor to use uow


async def get_or_create_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    async with PgUnitOfWork() as uow:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await uow.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        uow.add(user)
        await uow.commit()
        await uow.refresh(user)

    return user


async def get_private_access(telegram_id: int) -> PrivateAccess | None:
    async with PgUnitOfWork() as uow:
        query = select(PrivateAccess).where(PrivateAccess.telegram_id == telegram_id)
        return (await uow.execute(query)).scalar_one_or_none()


async def create_private_access(telegram_id: int) -> PrivateAccess:
    async with PgUnitOfWork() as uow:
        private_access = PrivateAccess(telegram_id=telegram_id)
        uow.add(private_access)
        await uow.commit()
        await uow.refresh(private_access)
        return private_access


async def get_user_by_access_code(access_code: str) -> User | None:
    async with PgUnitOfWork() as uow:
        query = select(User).join(PrivateAccess).where(PrivateAccess.access_code == access_code)
        return (await uow.execute(query)).scalar_one_or_none()


async def get_content_by_user_and_step(user: User, step: int | None = None) -> Content | None:
    conditions = [Content.user_id == user.id]
    if step is not None:
        conditions.append(Content.step_number == step)

    async with PgUnitOfWork() as uow:
        query = select(Content).where(*conditions)
        return (await uow.execute(query)).scalar_one_or_none()


async def create_content(user: User, step: int, message: str, content_text: str) -> Content:
    async with PgUnitOfWork() as uow:
        content = Content(
            step_number=step,
            message=message,
            content=content_text,
            user_id=user.id,
        )
        uow.add(content)
        await uow.commit()
        await uow.refresh(content)
        return content
