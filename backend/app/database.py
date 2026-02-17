from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


def _ensure_async_url(url: str) -> str:
    """Convert common PostgreSQL URL schemes to asyncpg-compatible format."""
    url = url.strip().strip("'\"")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


engine = create_async_engine(_ensure_async_url(settings.DATABASE_URL), echo=False, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
