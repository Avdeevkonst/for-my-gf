from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import General


class User(General):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    login: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    contents: Mapped[list["Content"]] = relationship(back_populates="user")

    __table_args__ = (Index("ix_user_telegram_id", telegram_id, unique=True),)


class Content(General):
    content: Mapped[str] = mapped_column(String)
    step_number: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship(back_populates="contents")
