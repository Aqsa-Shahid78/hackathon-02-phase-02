import uuid
from collections.abc import AsyncGenerator

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import async_session
from app.exceptions import AuthenticationError, AuthorizationError
from app.models import User
from app.security import decode_access_token


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not access_token:
        raise AuthenticationError()

    payload = decode_access_token(access_token)
    if payload is None:
        raise AuthenticationError()

    user_id = payload.get("sub")
    if user_id is None:
        raise AuthenticationError()

    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise AuthenticationError()

    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalars().first()
    if user is None:
        raise AuthenticationError()

    return user


def verify_user_ownership(path_user_id: uuid.UUID, current_user: User) -> None:
    if path_user_id != current_user.id:
        raise AuthorizationError()
