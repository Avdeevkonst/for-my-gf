from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.config.settings import settings


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
