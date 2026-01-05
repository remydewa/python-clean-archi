"""
This file contains heath chek routes that can be used in the k8s configuration file for deployment
To verify if k8s pod is working or not
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis import Redis

from app.drivers.rest.dependencies import get_db, get_redis_client


router = APIRouter()


@router.get(
    "/health/live", description="Test if application is alive", include_in_schema=False
)
def health_live():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.get(
    "/health/ready",
    description="Test if applicaion is ready including critical dependencies",
    include_in_schema=False,
)
def health_ready(
    session=Depends(get_db), redis_client: Redis = Depends(get_redis_client)
):
    redis_client.ping()
    return JSONResponse(content={"status": "ok"}, status_code=200)
