from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.bot.utils.db import get_user_by_access_code
from src.config.settings import settings


class AdminAuth(AuthenticationBackend):
    """Authentication backend for admin interface."""

    async def login(self, request: Request) -> bool:
        """Check if user is allowed to access admin interface."""
        form = await request.form()
        access_code = form.get("access_code", None)

        if access_code is None:
            return False
        elif isinstance(access_code, str):
            user = await get_user_by_access_code(access_code)
            if user is None:
                return False

        # Store access_code in session
        request.session.update({"access_code": access_code})
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
