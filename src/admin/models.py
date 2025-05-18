from typing import TYPE_CHECKING, Any

from sqladmin import ModelView
from wtforms import FileField

from src.storage.database.models import Content, User
from src.storage.minio import upload_file

if TYPE_CHECKING:
    from fastapi import UploadFile


class UserAdmin(ModelView, model=User):
    """Admin interface for User model."""

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [
        User.id,
        User.telegram_id,
        User.username,
        User.first_name,
        User.last_name,
        User.registered_at,
    ]

    column_details_exclude_list = []
    form_excluded_columns = [User.registered_at]

    can_delete = False  # Prevent user deletion from admin
    can_create = False  # Users are created only via Telegram
    can_edit = True  # Allow editing user details


class ContentAdmin(ModelView, model=Content):
    """Admin interface for Content model."""

    name = "Content"
    name_plural = "Contents"
    icon = "fa-solid fa-file"

    column_list = [
        Content.id,
        Content.step_number,
        Content.message,
        Content.user_id,
        Content.created_at,
    ]

    form_excluded_columns = [Content.created_at]

    # Add file upload field
    form_extra_fields = {"file": FileField("File Upload")}

    async def on_model_change(self, data: dict, model: Any, is_created: bool) -> None:
        """Handle file upload when content is created or updated."""
        if data.get("file"):
            file: UploadFile = data["file"]

            # Generate unique object name (you might want to improve this)
            object_name = f"content_{model.id}/{file.filename}"

            # Upload file to minio
            file_url = await upload_file(file.file, object_name)

            # Update content with file URL
            model.content = file_url
