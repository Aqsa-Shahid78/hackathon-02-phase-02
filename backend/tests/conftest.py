import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.main import app
from app.dependencies import get_db
from app.models import User
from app.security import hash_password, create_access_token


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default event loop policy."""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()


# Use NullPool to avoid connection reuse across event loops
test_engine = create_async_engine(
    settings.DATABASE_URL, echo=False, future=True, poolclass=NullPool
)


@pytest_asyncio.fixture
async def db_session():
    """Provide a transactional database session that rolls back after each test."""
    conn = await test_engine.connect()
    transaction = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await conn.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    """Async HTTP test client with overridden DB dependency."""

    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user and return it."""
    user = User(
        id=uuid.uuid4(),
        email=f"test_{uuid.uuid4().hex[:8]}@example.com",
        hashed_password=hash_password("password123"),
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def second_user(db_session: AsyncSession) -> User:
    """Create a second test user for isolation tests."""
    user = User(
        id=uuid.uuid4(),
        email=f"other_{uuid.uuid4().hex[:8]}@example.com",
        hashed_password=hash_password("password123"),
    )
    db_session.add(user)
    await db_session.flush()
    return user


def auth_cookies(user: User) -> dict:
    """Generate auth cookie header dict for a given user."""
    token = create_access_token(subject=str(user.id))
    return {"access_token": token}


@pytest_asyncio.fixture
async def authed_client(client: AsyncClient, test_user: User):
    """Client with auth cookies set for test_user."""
    token = create_access_token(subject=str(test_user.id))
    client.cookies.set("access_token", token)
    yield client
