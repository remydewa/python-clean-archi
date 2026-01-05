from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from app.drivers.rest.main import app, sub_api_v1


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    This fixture create a http client to test the FastAPI driver
    :return:
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def clear_overrides():
    """
    clear patched dependencies after used
    :return:
    """
    yield
    app.dependency_overrides.clear()
    sub_api_v1.dependency_overrides.clear()
