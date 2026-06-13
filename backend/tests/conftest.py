import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.config.settings import settings

pytest_plugins = ["pytest_asyncio"]

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Tạo engine và session hoàn toàn mới cho mỗi test để tránh lỗi Event Loop của asyncpg."""
    # Tạo engine mới (bỏ qua pool để không bị kẹt connection)
    test_engine = create_async_engine(
        settings.DATABASE_URL_ASYNC, 
        poolclass=NullPool
    )
    test_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    
    session = test_session_maker()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()
        await test_engine.dispose()
