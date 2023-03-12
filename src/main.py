import fastapi
import src.api.redirect_route as redirect_route
import src.api.url_router as url_route

app: fastapi.FastAPI = fastapi.FastAPI(title="URL shortener", description="A simple API for creating short urls")
app.include_router(redirect_route.router)
app.include_router(url_route.router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass
