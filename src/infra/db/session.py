from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=5,  # Keeping this as 5 connections since not a lot trafic we will be using
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)


SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=True, autoflush=False, autocommit=False
)
