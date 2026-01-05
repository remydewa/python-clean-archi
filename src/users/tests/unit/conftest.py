from hashlib import sha256
from uuid import UUID

import pytest
from app.adapters.repositories.otp_repositories.in_memory_repository import (
    InMemoryRepository,
)
from app.adapters.repositories.user_repository.in_memory_repository import (
    InMemoryUserRepository,
)
from app.domain.entities.user import User
from app.ports.otp_sender import OtpSender
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.tests.unit.fakes.fake_otp_sender import FakeOtpSender


@pytest.fixture(scope="function")
def user_repository() -> UserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def otp_sender() -> OtpSender:
    return FakeOtpSender()


@pytest.fixture
def otp_repository() -> OtpRepository:
    return InMemoryRepository()


@pytest.fixture
def valid_email() -> str:
    return "remy.dewailly@yopmail.com"


@pytest.fixture
def valid_password() -> str:
    return "AfdljkB!#159"


@pytest.fixture
def user_id() -> UUID:
    return UUID("322f2831-d18b-4207-a0c4-edbc7a3879dd")


@pytest.fixture
def new_valid_user(user_id: UUID, valid_email: str, valid_password: str) -> User:
    return User(id=user_id, email=valid_email, password=valid_password)


@pytest.fixture
def hashed_valid_password(valid_password: str) -> str:
    return sha256(valid_password.encode()).hexdigest()


@pytest.fixture
def db_user(user_id: UUID, valid_email: str, hashed_valid_password: str) -> User:
    return User(id=user_id, email=valid_email, password=hashed_valid_password)
