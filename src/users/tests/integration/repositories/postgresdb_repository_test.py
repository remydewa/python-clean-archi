"""
This file test the postgres repository adapter
src/users/app/adapters/repositories/user_repository/postgresdb_repository.py
"""

import pytest
from psycopg_pool import AsyncConnectionPool

from app.adapters.repositories.user_repository.postgresdb_repository import (
    PostgresUserRepository,
)
from app.domain.entities.user import User
from app.ports.repositories.user_repository import UserRepository


@pytest.fixture
async def postgres_pool(postgres_database_uri):
    async with AsyncConnectionPool(conninfo=postgres_database_uri) as pool:
        yield pool
        await pool.close()


@pytest.fixture
async def postgres_connection(postgres_pool: AsyncConnectionPool):
    """
    :param postgres_pool:
    :return: a connection to postgres database
    """
    async with postgres_pool.connection() as conn:
        yield conn


@pytest.fixture
def user_repository(postgres_connection) -> UserRepository:
    return PostgresUserRepository(postgres_connection)


@pytest.fixture
def remy_email() -> str:
    return "remydewailly@hotmail.com"


async def test_get_unknown_user(user_repository: UserRepository, remy_email: str):
    user = await user_repository.get(remy_email)
    assert user is None  # user doesn't exist


async def test_create_user_success(user_repository: UserRepository, remy_email: str):
    password: str = "Abc123@!915d"
    remy_user: User = User(email=remy_email, password=password)
    result: bool = await user_repository.create(remy_user, password)
    assert result is True


async def test_get_known_user(user_repository: UserRepository, remy_email: str):
    user = await user_repository.get(remy_email)
    assert user is not None  # user found in db?
    assert user.email == remy_email  # yes and it's the good user
    assert user.is_enabled is False  # which has not activated his account yet


async def test_enable_known_user(user_repository: UserRepository, remy_email: str):
    await user_repository.enable_account(remy_email)
    user = await user_repository.get(remy_email)
    assert user is not None
    assert user.email == remy_email
    assert user.is_enabled is True  # user account has been enabled
