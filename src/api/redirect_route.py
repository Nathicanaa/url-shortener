import fastapi


router: fastapi.APIRouter = fastapi.APIRouter(tags=["redirect"])


@router.get("/{url_hash}")
async def redirect_to_full_url():
    # return fastapi.responses.RedirectResponse()
    pass
