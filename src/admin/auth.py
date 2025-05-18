from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.bot.utils.db import get_user_by_access_code
from src.config.settings import settings


class AdminAuth(AuthenticationBackend):
    """Authentication backend for admin interface."""

    async def login(self, request: Request) -> bool:
        """Check if user is allowed to access admin interface."""
        form = await request.form()
        username, access_code = form.get("username", None), form.get("password", None)

        if username is None or access_code is None:
            return False
        elif isinstance(access_code, str):
            user = await get_user_by_access_code(access_code)
            if user is None:
                return False

        # Store access_code in session
        request.session.update({str(user.id): access_code})
        return True

    async def logout(self, request: Request) -> bool:
        """Remove user from session."""
        # TODO: change logic
        request.session.pop("token")
        return True

    async def authenticate(self, request: Request) -> bool:
        # TODO: change logic

        return bool(request.session.get("token", False))


authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)
