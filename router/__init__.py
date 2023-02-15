from fastapi import APIRouter

# Import Router
from router.main_router import router as main_router
from router.upscale_router import router as upscale_router

routers = APIRouter()

# include router
routers.include_router(main_router)
routers.include_router(upscale_router)
