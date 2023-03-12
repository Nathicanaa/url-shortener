import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


# engine = create_async_engine(
#     "postgresql+asyncpg://postgres:shortener@34.76.126.178:5432/shortener",
#     pool_size=5,
#     max_overflow=2,
#     pool_timeout=30,
#     pool_recycle=1800,
#     pool_pre_ping=True
# )
# session = orm.sessionmaker


class Base(orm.DeclarativeBase):
    pass


