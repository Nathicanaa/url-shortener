import pydantic
import datetime


class UrlTarget(pydantic.BaseModel):
    target_url: pydantic.AnyUrl


class UrlShort(pydantic.BaseModel):
    short_url: pydantic.AnyUrl


class UrlResponse(UrlTarget, UrlShort):
    url_hash: str
    created_at: datetime.datetime
