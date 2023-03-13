import typing

import sqlalchemy.ext.asyncio as async_sa

import src.logger

SessionLocal: async_sa.async_sessionmaker[async_sa.AsyncSession] | None = None

logger = src.logger.get_logger(__name__)


def configure_session(db_url: str) -> None:
    global SessionLocal
    engine = async_sa.create_async_engine(
        db_url,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
    )
    SessionLocal = async_sa.async_sessionmaker(engine, expire_on_commit=False)
    logger.info("Session Configured")
    return


async def get_session() -> typing.AsyncIterator[async_sa.AsyncSession]:
    async with SessionLocal() as session:  # type: ignore
        yield session
