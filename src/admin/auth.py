from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.config.settings import settings
from src.database.config import PgUnitOfWork
from src.database.models import User
from src.project_utils import verify_password

security = HTTPBasic(auto_error=True)


async def authenticate_admin(login: str, password: str) -> User | None:
    """Authenticate admin user."""
    async with PgUnitOfWork() as uow:
        # Query for user with matching login
        query = select(User).where(User.login == login)
        result = await uow.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Verify password
        if await verify_password(password, user.password_hash):
            return user

        return None


async def get_current_admin_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    """Dependency for getting current admin user."""
    user = await authenticate_admin(credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


class AdminAuth(AuthenticationBackend):
    """Authentication backend for admin interface."""

    async def login(self, request: Request) -> bool:
        """Check if user is allowed to access admin interface."""
        form = await request.form()
        telegram_id = form.get("telegram_id", None)

        try:
            telegram_id = int(telegram_id)  # pyright: ignore[reportArgumentType]
        except (TypeError, ValueError):
            return False

        # Store telegram_id in session
        request.session.update({"telegram_id": telegram_id})
        return True

    async def logout(self, request: Request) -> bool:
        """Remove user from session."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        """Check if user is authenticated."""
        # TODO: Check user in database

        return None


authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)
