"""
This file contains dependencies that can be used in the FastAPI routes
"""

from typing import Annotated

from fastapi import Depends
from psycopg_pool import AsyncConnectionPool
from redis import Redis

from app.adapters.otp.console_sender import ConsoleOtpSender
from app.adapters.repositories.otp_repositories.redis_repository import RedisRepository
from app.adapters.repositories.user_repository.postgresdb_repository import (
    PostgresUserRepository,
)
from app.drivers.rest.config import settings
from app.ports.otp_sender import OtpSender
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.use_cases.create_user_use_case import CreateUserUseCase
from app.use_cases.enable_user_account_use_case import EnableUserAccountUseCase

async_pool: AsyncConnectionPool | None = None


def init_pool() -> AsyncConnectionPool:
    global async_pool
    if async_pool is None:
        async_pool = AsyncConnectionPool(conninfo=settings.postgres_database_uri)

    return async_pool


async def get_db():
    pool = init_pool()
    async with pool.connection() as conn:
        yield conn


def get_user_repository(postgres_connection=Depends(get_db)) -> UserRepository:
    return PostgresUserRepository(postgres_connection)


def get_otp_sender() -> OtpSender:
    return ConsoleOtpSender()


def get_redis_client() -> Redis:
    return Redis.from_url(settings.REDIS_CONNECTION_STRING, decode_responses=True)


def get_otp_repository(
    redis_client: Annotated[Redis, Depends(get_redis_client)],
) -> OtpRepository:
    return RedisRepository(redis_client)


def get_create_user_use_case(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    otp_sender: Annotated[OtpSender, Depends(get_otp_sender)],
    otp_repository: Annotated[OtpRepository, Depends(get_otp_repository)],
):
    return CreateUserUseCase(user_repository, otp_sender, otp_repository)


def get_enable_user_account_use_case(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    otp_repository: Annotated[OtpRepository, Depends(get_otp_repository)],
):
    return EnableUserAccountUseCase(user_repository, otp_repository)
