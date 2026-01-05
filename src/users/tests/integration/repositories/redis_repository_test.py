"""
This class test the Redis Otp repository class
src/users/app/adapters/repositories/otp_repositories/redis_repository.py
"""

import pytest
from redis import Redis

from app.adapters.repositories.otp_repositories.redis_repository import RedisRepository
from app.ports.repositories.otp_repository import OtpRepository


@pytest.fixture
def otp_repository(redis_client: Redis) -> OtpRepository:
    return RedisRepository(redis_client)


@pytest.fixture
def user_id() -> str:
    return "f387ed87-aaab-4ae6-a72d-601bcd4a2dbb"


@pytest.fixture
def otp_code() -> str:
    return "1234"


async def test_save(otp_repository: OtpRepository, user_id: str, otp_code: str):
    otp_repository.save(user_id, otp_code, 60)  # insert a code available for 60s


async def test_verify_code_exist(
    otp_repository: OtpRepository, user_id: str, otp_code: str
):
    result = otp_repository.verify(user_id, otp_code)
    assert result == True  # code exist and belongs to the user


async def test_verify_code_not_exist(otp_repository: OtpRepository, user_id: str):
    result = otp_repository.verify(user_id, "4567")
    assert result == False  # code doesn't exist or doesn't belong to the user


async def test_delete(otp_repository: OtpRepository, user_id: str, otp_code: str):
    otp_repository.delete(user_id)
    result = otp_repository.verify(user_id, otp_code)
    assert result == False
