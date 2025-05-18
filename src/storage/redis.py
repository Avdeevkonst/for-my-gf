from redis.asyncio import Redis

from src.config.settings import settings

redis_client = Redis.from_url(settings.db_url_redis)


async def set_user_step(user_id: int, step: int) -> None:
    """Set current step for user.

    Args:
        user_id: Telegram user ID
        step: Current step number
    """
    await redis_client.set(f"user_step:{user_id}", step)


async def get_user_step(user_id: int) -> int:
    """Get current step for user.

    Args:
        user_id: Telegram user ID

    Returns:
        int: Current step number, 1 if not set
    """
    step = await redis_client.get(f"user_step:{user_id}")
    return int(step) if step else 1


async def set_user_content_owner(user_id: int, owner_id: int) -> None:
    """Set content owner for user.

    Args:
        user_id: Telegram user ID of the viewer
        owner_id: Telegram user ID of the content owner
    """
    await redis_client.set(f"user_content_owner:{user_id}", owner_id)


async def get_user_content_owner(user_id: int) -> int | None:
    """Get content owner for user.

    Args:
        user_id: Telegram user ID

    Returns:
        int | None: Content owner's Telegram ID if set, None otherwise
    """
    owner_id = await redis_client.get(f"user_content_owner:{user_id}")
    return int(owner_id) if owner_id else None
