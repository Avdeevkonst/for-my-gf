from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import PgUnitOfWork
from src.database.models import PrivateAccess, User

# TODO: refactor to use uow


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_private_access(session: AsyncSession, telegram_id: int) -> PrivateAccess | None:
    query = select(PrivateAccess).where(PrivateAccess.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_private_access(session: AsyncSession, telegram_id: int) -> PrivateAccess:
    private_access = PrivateAccess(telegram_id=telegram_id)
    session.add(private_access)
    await session.commit()
    await session.refresh(private_access)
    return private_access


async def get_user_by_access_code(access_code: str) -> User | None:
    async with PgUnitOfWork() as uow:
        query = select(User).join(PrivateAccess).where(PrivateAccess.access_code == access_code)
        result = await uow.execute(query)
        return result.scalar_one_or_none()
