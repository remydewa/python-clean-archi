from fastapi import APIRouter

from app.drivers.rest.routes.healthcheck import router as health_router
from app.drivers.rest.routes.v1.user import router as user_router

router = APIRouter()
router.include_router(health_router)

router_v1 = APIRouter()
router_v1.include_router(user_router)
