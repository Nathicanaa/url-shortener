import datetime
import hashlib

import fastapi
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession

import src.api.utils as api_utils
import src.db.models as models
import src.db.session
import src.schemas as schemas

router: fastapi.APIRouter = fastapi.APIRouter(prefix="/url", tags=["url"])


@router.post("", status_code=fastapi.status.HTTP_201_CREATED)
async def create_short_url(
    url_body: schemas.UrlTarget,
    request: fastapi.Request,
    session: AsyncSession = fastapi.Depends(src.db.session.get_session),
) -> schemas.UrlResponse:
    url_hash: str = hashlib.sha256(url_body.target_url.encode()).hexdigest()[
        :5
    ]
    url_exists: models.Url | None = await models.Url.get_by_hash(
        session, url_hash
    )
    if url_exists:
        return schemas.UrlResponse(
            target_url=url_exists.target_url,
            short_url=url_exists.short_url,
            url_hash=url_exists.url_hash,
            created_at=url_exists.created_at,
            clicks=url_exists.clicks,
        )
    created_at: datetime.datetime = datetime.datetime.utcnow()
    base_url: str = str(request.base_url)
    short_url: str = f"{base_url}{url_hash}"
    await models.Url.insert_url(
        session, url_hash, short_url, url_body.target_url, created_at
    )
    response = schemas.UrlResponse(
        target_url=url_body.target_url,
        short_url=short_url,
        url_hash=url_hash,
        created_at=created_at,
        clicks=0,
    )
    return response


@router.delete("", status_code=fastapi.status.HTTP_200_OK)
async def remove_short_url(
    url_body: schemas.UrlShort,
    session: AsyncSession = fastapi.Depends(src.db.session.get_session),
) -> schemas.UrlShort:
    url_hash: str = url_body.short_url.split("/")[-1]
    url_exists: models.Url = await api_utils.get_by_hash_or_raise_400(
        session, url_hash, f"Url {url_body.short_url} does not exist"
    )
    await models.Url.delete_url(session, url_exists)
    return url_body


@router.get("/", status_code=fastapi.status.HTTP_200_OK)
async def get_full_url(
    short_url: pydantic.AnyUrl = fastapi.Query(...),
    session: AsyncSession = fastapi.Depends(src.db.session.get_session),
) -> schemas.UrlTarget:
    url_hash: str = short_url.split("/")[-1]
    url_exists: models.Url = await api_utils.get_by_hash_or_raise_400(
        session, url_hash, f"Url {short_url} does not exist"
    )
    return schemas.UrlTarget(target_url=url_exists.target_url)
