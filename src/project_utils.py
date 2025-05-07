import re
from types import TracebackType
from typing import NoReturn

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

ph = PasswordHasher()


async def hash_password(password: str) -> str:
    """Hash password using Argon2."""
    return ph.hash(password)


async def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash using Argon2."""
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


def handle_error(
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    exc_tb: TracebackType | None,
):
    if exc_type is not None and exc_val is not None:
        status_code = status.HTTP_404_NOT_FOUND if exc_type is NoResultFound else status.HTTP_400_BAD_REQUEST
        handle_error_message(exc_val.args[0], status_code)


def handle_error_message(
    error: SQLAlchemyError,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> NoReturn:  # pragma: no cover
    msg = convert_sqlachemy_exception(error)
    raise HTTPException(
        status_code=status_code,
        detail=msg,
    )


def convert_sqlachemy_exception(error: SQLAlchemyError):  # pragma: no cover
    msg = repr(error)
    if "DETAIL" in msg:
        detail = msg.partition("DETAIL")[-1]
    elif "NoResultFound" in msg:
        detail = "No such object"
    else:
        detail = msg
    pattern = r'[^-0-9a-zA-Zа-яА-Я\s_="]'
    return re.sub(pattern, "", detail).strip()
