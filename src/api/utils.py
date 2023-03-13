from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Url


async def get_by_hash_or_raise_400(
    session: AsyncSession, url_hash: str, message: str
) -> Url:
    url: Url | None = await Url.get_by_hash(session, url_hash)
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=message
        )
    return url
