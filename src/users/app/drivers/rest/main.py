from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.drivers.rest.routes.main import router as healthcheck_router, router_v1
from app.drivers.rest.config import settings
from app.drivers.rest.exception_handlers import exception_container

sub_api_v1 = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
sub_api_v1.include_router(router_v1)
# catch exception
exception_container(sub_api_v1)
# add prometheus metrics
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_group_untemplated=False,
    excluded_handlers=["/metrics"],
).instrument(sub_api_v1).expose(sub_api_v1)

app = FastAPI()
# include healthcheck_router for k8s deployments
app.include_router(healthcheck_router)

# multi version api management
# Nb: if you want to add /user prefix use an api gateway to manage routing of this microservice or future others
# and avoid expose directly fastapi pods on internet
app.mount("/api/v1", sub_api_v1)
