import json

import fastapi
import sqlalchemy.exc

import src.api.redirect_route as redirect_route
import src.api.url_router as url_route
import src.config
import src.db.session
import src.logger

app: fastapi.FastAPI = fastapi.FastAPI(
    title="URL shortener", description="A simple API for creating short urls"
)
app.include_router(redirect_route.router)
app.include_router(url_route.router)
logger = src.logger.get_logger(__name__)


@app.on_event("startup")
async def startup() -> None:
    config = src.config.Config()
    src.db.session.configure_session(config.db_url)
    logger.info(json.dumps("Application started"))


@app.exception_handler(sqlalchemy.exc.SQLAlchemyError)
def handle_sqlalchemy_general_error(
    request: fastapi.Request, exc: sqlalchemy.exc.SQLAlchemyError
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={"message": "Sqlalchemy error", "detail": exc._message()},
    )
