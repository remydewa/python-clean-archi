import pytest

from app.domain.entities.user import User
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.use_cases.enable_user_account_use_case import EnableUserAccountUseCase
from app.use_cases.exceptions import (
    UserInfoDoesntMatchError,
    IncorrectActivationCodeError,
    InvalidEmailFormatError,
)


@pytest.fixture
def enable_user_account_use_case(
    user_repository: UserRepository,
    otp_repository: OtpRepository,
) -> EnableUserAccountUseCase:
    return EnableUserAccountUseCase(user_repository, otp_repository)


async def test_enable_user_account_invalid_email(
    enable_user_account_use_case: EnableUserAccountUseCase,
):
    user: User = User("pas-un-mail", "aA1!#@BCD7ar")

    # test the enable_user_account_use_case InvalidEmailFormatError exception
    with pytest.raises(InvalidEmailFormatError):
        await enable_user_account_use_case(user, 1234)


async def test_enable_existing_user_account_incorrect_password(
    user_repository: UserRepository,
    enable_user_account_use_case: EnableUserAccountUseCase,
    db_user: User,
):
    user_repository.users = []
    user_repository.users.append(db_user)
    existing_user_email_with_incorrect_password = User(
        "remy.dewailly@yopmail.com", "abc"
    )
    with pytest.raises(UserInfoDoesntMatchError):  # good email but bad password
        await enable_user_account_use_case(
            existing_user_email_with_incorrect_password, 1234
        )


async def test_enable_not_existing_user_account(
    user_repository: UserRepository,
    enable_user_account_use_case: EnableUserAccountUseCase,
):
    not_existing_user_account = User("remy.dewailly2@yopmail.com", "aA1!#@BCD7ar")
    with pytest.raises(UserInfoDoesntMatchError):  # user doesn't exist
        await enable_user_account_use_case(not_existing_user_account, 1234)


async def test_enable_account_incorrect_code(
    user_repository: UserRepository,
    enable_user_account_use_case: EnableUserAccountUseCase,
    new_valid_user: User,
    db_user: User,
):
    user_repository.users = []
    user_repository.users.append(db_user)
    # test the enable_user_account_use_case IncorrectActivationCodeError exception
    with pytest.raises(IncorrectActivationCodeError):
        await enable_user_account_use_case(new_valid_user, 12345)  # code too long
        await enable_user_account_use_case(new_valid_user, 123)  # code too short


async def test_enable_user_account_successful(
    user_repository: UserRepository,
    otp_repository: OtpRepository,
    enable_user_account_use_case: EnableUserAccountUseCase,
    new_valid_user: User,
    db_user: User,
):
    user_repository.users = []
    user_repository.users.append(db_user)  # add user in repository
    otp_repository.save(str(db_user.id), "1234", 60)
    result: bool = await enable_user_account_use_case(new_valid_user, 1234)
    assert result is True
