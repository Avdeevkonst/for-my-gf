from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.models import ContentAdmin, UserAdmin
from src.database.config import dbconfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Initialize database models
    yield


app = FastAPI(lifespan=lifespan)

# Initialize admin interface
admin = Admin(
    app,
    dbconfig.engine,
    authentication_backend=authentication_backend,
    title="Content Management",
)

# Add model views
admin.add_view(UserAdmin)
admin.add_view(ContentAdmin)
