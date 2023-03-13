import datetime
import json
import typing

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession

import src.logger

logger = src.logger.get_logger(__name__)


class Base(orm.DeclarativeBase):  # type: ignore
    pass


class Url(Base):
    __tablename__ = "urls"

    url_hash: orm.Mapped[str] = orm.mapped_column(
        sa.String(10), primary_key=True
    )
    short_url: orm.Mapped[str] = orm.mapped_column(nullable=False)
    target_url: orm.Mapped[str] = orm.mapped_column(nullable=False)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=datetime.datetime.utcnow
    )
    clicks: orm.Mapped[int] = orm.mapped_column(default=0)

    @classmethod
    async def insert_url(
        cls,
        session: AsyncSession,
        url_hash: str,
        short_url: str,
        target_url: str,
        created_at: datetime.datetime,
    ) -> str:
        async with session.begin():
            session.add(
                cls(
                    url_hash=url_hash,
                    short_url=short_url,
                    target_url=target_url,
                    created_at=created_at,
                )
            )
        return url_hash

    @classmethod
    async def get_by_hash(
        cls, session: AsyncSession, url_hash: str
    ) -> typing.Optional["Url"]:
        async with session.begin():
            stmt = sa.select(cls).where(cls.url_hash == url_hash)
            result = await session.execute(stmt)
        result = result.scalars().one_or_none()
        return result  # type: ignore

    @classmethod
    async def delete_url(cls, session: AsyncSession, url: "Url") -> str:
        async with session.begin():
            await session.delete(url)
        return url.short_url  # type: ignore

    @classmethod
    async def update_clicks(cls, session: AsyncSession, url: "Url") -> str:
        async with session.begin():
            url.clicks += 1
        logger.info(
            json.dumps(
                f"Clicks increased by 1 for url with hash {url.url_hash}"
            )
        )
        return url.url_hash  # type: ignore
