from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.dependencies import get_db, get_current_user
from app.exceptions import AuthenticationError, ConflictError
from app.rate_limit import auth_rate_limit
from app.models import User
from app.schemas import SignupRequest, SigninRequest, AuthResponse, UserResponse
from app.security import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter()


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/signup",
    status_code=201,
    response_model=AuthResponse,
    dependencies=[Depends(auth_rate_limit)],
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid request data"},
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"},
        429: {"description": "Too many requests"},
    },
)
async def signup(data: SignupRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email.lower()))
    existing = result.scalars().first()
    if existing:
        raise ConflictError(message="Account creation failed")

    user = User(
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, token)

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email),
        access_token=token,
    )


@router.post(
    "/signin",
    response_model=AuthResponse,
    dependencies=[Depends(auth_rate_limit)],
    responses={
        200: {"description": "Authentication successful"},
        401: {"description": "Invalid email or password"},
        422: {"description": "Validation error"},
        429: {"description": "Too many requests"},
    },
)
async def signin(data: SigninRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email.lower()))
    user = result.scalars().first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise AuthenticationError(message="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    _set_auth_cookie(response, token)

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email),
        access_token=token,
    )


@router.post(
    "/signout",
    status_code=204,
    responses={
        204: {"description": "Signed out successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def signout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="access_token")
    return Response(status_code=204)
