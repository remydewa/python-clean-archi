from typing import Any

from fastapi import status
from httpx import AsyncClient, BasicAuth

from app.drivers.rest.main import sub_api_v1
from app.drivers.rest.dependencies import get_enable_user_account_use_case
from app.use_cases.exceptions import IncorrectActivationCodeError

url = "/api/v1/enable"
test_email = "remydewailly@hotmail.com"
test_password = "024aAb1234@!"
test_code = 1234


async def test_enable_user_account_with_error(async_client: AsyncClient):
    """
    Test the exception returned by the /api/v1/enable endpoint.
    :param async_client: Http client.
    :return:
    """

    class MockUseCase:
        async def __call__(self, *args: Any, **kwargs: Any) -> None:
            raise IncorrectActivationCodeError()

    sub_api_v1.dependency_overrides[get_enable_user_account_use_case] = (
        lambda: MockUseCase()
    )
    response = await async_client.post(
        url,
        params={"code": test_code},
        auth=BasicAuth(test_email, test_password),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": str(IncorrectActivationCodeError())}
