import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import User, Post, Comment
from app.core.jwt import create_access_token
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine() -> AsyncGenerator:
    """Create a test database engine using SQLite for faster testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(
    test_engine
) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def test_client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with overridden database dependency."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(test_session: AsyncSession) -> User:
    """Create a test user in the database."""
    from faker import Faker
    fake = Faker()
    
    user_repo = UserRepository(test_session)
    username = fake.user_name()
    email = fake.email()
    hashed_password = hash_password("TestPassword123!")
    user = await user_repo.create(username, email, hashed_password)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_user_token(test_user: User) -> str:
    """Create a JWT token for the test user."""
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture(scope="function")
async def auth_headers(test_user_token: str) -> dict[str, str]:
    """Create authentication headers for requests."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture(scope="function")
async def test_post(test_session: AsyncSession, test_user: User) -> Post:
    """Create a test post in the database."""
    from app.repositories.post_repository import PostRepository
    
    post_repo = PostRepository(test_session)
    post = await post_repo.create(
        title="Test Post Title",
        content="This is test post content",
        created_by=test_user.id
    )
    await test_session.commit()
    await test_session.refresh(post)
    return post


@pytest.fixture(scope="function")
async def test_comment(test_session: AsyncSession, test_post: Post, test_user: User) -> Comment:
    """Create a test comment in the database."""
    from app.repositories.comment_repository import CommentRepository
    
    comment_repo = CommentRepository(test_session)
    comment = await comment_repo.create(
        content="This is a test comment",
        post_id=test_post.id,
        created_by=test_user.id
    )
    await test_session.commit()
    await test_session.refresh(comment)
    return comment
