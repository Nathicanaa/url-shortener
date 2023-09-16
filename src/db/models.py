import datetime
import json
import typing

import sqids
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession

import src.logger

logger = src.logger.get_logger(__name__)
hasher: sqids.Sqids = sqids.Sqids()


class Base(orm.DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = "urls"

    id_seq = sa.Sequence(
        "id_seq",
        metadata=Base.metadata,
        start=1,
        increment=1,
        data_type=sa.BIGINT,
    )
    url_hash: orm.Mapped[str] = orm.mapped_column(
        sa.String(20), primary_key=True
    )
    target_url: orm.Mapped[str] = orm.mapped_column(nullable=False)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=datetime.datetime.utcnow
    )
    clicks: orm.Mapped[int] = orm.mapped_column(default=0)

    @classmethod
    async def insert_url(
        cls,
        session: AsyncSession,
        target_url: str,
    ) -> "Url":
        async with session.begin():
            next_val = await session.execute(Url.id_seq)
            url = cls(
                target_url=target_url, url_hash=hasher.encode([next_val])
            )
            session.add(url)
        return url

    @classmethod
    async def get_by_hash(
        cls, session: AsyncSession, url_hash: str
    ) -> typing.Optional["Url"]:
        async with session.begin():
            stmt = sa.select(cls).where(cls.url_hash == url_hash)
            result = await session.execute(stmt)
        result = result.scalars().one_or_none()  # type: ignore
        return result  # type: ignore

    @classmethod
    async def delete_url(cls, session: AsyncSession, url: "Url") -> str:
        async with session.begin():
            await session.delete(url)
        return url.url_hash

    @classmethod
    async def update_clicks(cls, session: AsyncSession, url: "Url") -> str:
        async with session.begin():
            url.clicks += 1
        logger.info(
            json.dumps(
                f"Clicks increased by 1 for url with hash {url.url_hash}"
            )
        )
        return url.url_hash
