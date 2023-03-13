import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

import src.api.utils as api_utils
import src.db.models as models
import src.db.session

router: fastapi.APIRouter = fastapi.APIRouter(tags=["redirect"])


@router.get("/{url_hash}", status_code=fastapi.status.HTTP_302_FOUND)
async def redirect_to_full_url(
    background_tasks: fastapi.BackgroundTasks,
    url_hash: str = fastapi.Path(...),
    session: AsyncSession = fastapi.Depends(src.db.session.get_session),
) -> fastapi.responses.RedirectResponse:
    url_exists: models.Url = await api_utils.get_by_hash_or_raise_400(
        session, url_hash, f"Url with hash {url_hash} does not exist"
    )
    background_tasks.add_task(models.Url.update_clicks, session, url_exists)
    return fastapi.responses.RedirectResponse(
        url=url_exists.target_url, status_code=302
    )
