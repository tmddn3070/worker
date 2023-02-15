from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from router import routers

app_config = {
    "title": "Upscale_worker",
    "description": "Upscale Worker [GitHub](https://github.com/tmddn3070)",
    "version": "1.0.0",
    "redoc_url": "/docs/redoc",
    "docs_url": "/docs/swagger",
}

app = FastAPI(**app_config)


@app.get("/", include_in_schema=False)
async def route_root():
    return RedirectResponse(url="/docs/swagger")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers, prefix="/")