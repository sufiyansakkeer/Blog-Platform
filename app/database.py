

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import  get_settings

settings = get_settings()
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
    pool_timeout= 30
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()