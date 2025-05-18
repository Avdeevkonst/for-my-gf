import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.database.base import General


class User(General):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    contents: Mapped[list["Content"]] = relationship(back_populates="user")
    private_access: Mapped["PrivateAccess"] = relationship(back_populates="user")


class Content(General):
    content: Mapped[str] = mapped_column(String)
    step_number: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship(back_populates="contents")

    __table_args__ = (Index("ix_content_user_id_step_number", user_id, step_number, unique=True),)


class PrivateAccess(General):
    access_code: Mapped[str] = mapped_column(String, default=secrets.token_hex(16))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=(datetime.now(UTC) + timedelta(days=14))
    )

    telegram_id: Mapped[int] = mapped_column(ForeignKey("user.telegram_id"))
    user: Mapped[User] = relationship(back_populates="private_access")

    __table_args__ = (
        Index("ix_private_access_expires_at", expires_at),
        Index("ix_private_access_access_code", access_code),
    )
