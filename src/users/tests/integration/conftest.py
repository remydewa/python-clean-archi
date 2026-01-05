import os

import pytest
from redis import Redis


@pytest.fixture
def postgres_database_uri() -> str:
    return f"""
        dbname={os.environ.get("POSTGRES_DB")}
        user={os.environ.get("POSTGRES_USER")}
        password={os.environ.get("POSTGRES_PASSWORD")}
        host={os.environ.get("POSTGRES_HOST")}
        port={os.environ.get("POSTGRES_PORT")}
        """


@pytest.fixture
def redis_client() -> Redis:
    return Redis.from_url(
        os.environ.get("REDIS_CONNECTION_STRING"), decode_responses=True
    )
