import datetime
import hashlib
import fastapi
import pydantic
import src.schemas as schemas

router: fastapi.APIRouter = fastapi.APIRouter(prefix="/url", tags=["url"])


@router.post("", status_code=fastapi.status.HTTP_201_CREATED)
async def create_short_url(url_body: schemas.UrlTarget, request: fastapi.Request) -> schemas.UrlResponse:
    url_hash: str = hashlib.sha256(url_body.target_url.encode()).hexdigest()[:5]
    created_at: datetime.datetime = datetime.datetime.utcnow()
    base_url: str = str(request.base_url)
    short_url: str = f"{base_url}{url_hash}"
    response = schemas.UrlResponse(
        target_url=url_body.target_url,
        short_url=short_url,
        url_hash=url_hash,
        created_at=created_at
    )

    return response


@router.delete("")
async def remove_short_url(url_body: schemas.UrlShort):
    url_hash: str = url_body.short_url.split("/")[-1]
    return url_hash


@router.get("/")
async def get_full_url(short_url: pydantic.AnyUrl = fastapi.Query(...)):
    url_hash: str = short_url.split("/")[-1]
    return {"hash": url_hash}
