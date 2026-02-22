from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"sub": subject, "exp": expire}
    algorithm = settings.JWT_ALGORITHM.strip()
    return jwt.encode(to_encode, settings.JWT_SECRET.strip(), algorithm=algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        algorithm = settings.JWT_ALGORITHM.strip()
        payload = jwt.decode(
            token, settings.JWT_SECRET.strip(), algorithms=[algorithm]
        )
        return payload
    except JWTError:
        return None
