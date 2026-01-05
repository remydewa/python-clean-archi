"""
This class test the different exceptions returned by the /api/v1/create endpoint.
"""

from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient

from app.drivers.rest.main import sub_api_v1
from app.drivers.rest.dependencies import get_create_user_use_case
from app.use_cases.exceptions import (
    InvalidEmailFormatError,
    InvalidPasswordError,
    UserEmailAlreadyExistsError,
    UserInfoDoesntMatchError,
)


url = "/api/v1/create"
invalid_email: str = "remydewailly2@yopmailcom"
invalid_password: str = "abc1234"
invalid_payload = {"email": invalid_email, "password": invalid_password}


@pytest.mark.parametrize(
    "exception, status_code",
    [
        (InvalidEmailFormatError(invalid_email), status.HTTP_422_UNPROCESSABLE_CONTENT),
        (
            UserEmailAlreadyExistsError(invalid_email),
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        ),
        (UserInfoDoesntMatchError(invalid_email), status.HTTP_404_NOT_FOUND),
        (InvalidPasswordError(), status.HTTP_401_UNAUTHORIZED),
    ],
)
async def test_create_user_with_error(
    async_client: AsyncClient, exception: Exception, status_code: int
):
    class MockUseCase:
        async def __call__(self, *args: Any, **kwargs: Any) -> None:
            raise exception

    sub_api_v1.dependency_overrides[get_create_user_use_case] = lambda: MockUseCase()
    response = await async_client.post(url, json=invalid_payload)
    assert response.status_code == status_code
    assert response.json() == {"message": str(exception)}
