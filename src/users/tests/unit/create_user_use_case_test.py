import pytest

from app.domain.entities.user import User
from app.ports.otp_sender import OtpSender
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.use_cases.create_user_use_case import CreateUserUseCase
from app.use_cases.exceptions import (
    InvalidEmailFormatError,
    InvalidPasswordError,
    UserEmailAlreadyExistsError,
)


@pytest.fixture
def create_user_use_case(
    user_repository: UserRepository,
    otp_sender: OtpSender,
    otp_repository: OtpRepository,
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository, otp_sender, otp_repository)


@pytest.mark.parametrize(
    "user",
    [
        User("pas-un-mail", "aA1!#@BCD7ar"),
        User("mauvais@@example.com", "aA1!#@BCD7ar"),
        User("test@.com", "aA1!#@BCD7ar"),
    ],
)
async def test_create_user_invalid_email(
    create_user_use_case: CreateUserUseCase, user: User
):
    # test the create_user_use_case InvalidEmailFormatError exception
    with pytest.raises(InvalidEmailFormatError):
        await create_user_use_case(user)


@pytest.mark.parametrize(
    "user",
    [
        User("remy.dewailly@yopmail.com", "abcdefdhijkl"),  # only minuscule letters
        User("remy.dewailly@yopmail.com", "012345678912"),  # only numbers
        User("remy.dewailly@yopmail.com", "ABCDEFDHIJKL"),  # only majuscule letters
        User("remy.dewailly@yopmail.com", "ABCDEFDHIJa1"),  # no special characters
        User("remy.dewailly@yopmail.com", "aA1!"),  # only 4 characters
        User("remy.dewailly@yopmail.com", "aA1!#@BCD7ar4"),  # 13 characters
    ],
)
async def test_create_user_invalid_password(
    create_user_use_case: CreateUserUseCase, user: User
):
    # test the create_user_use_case InvalidPasswordError exception
    with pytest.raises(InvalidPasswordError):
        await create_user_use_case(user)


async def test_create_user_already_exists(
    user_repository: UserRepository,
    create_user_use_case: CreateUserUseCase,
    new_valid_user: User,
):
    user_repository.users.append(new_valid_user)  # add user in 'db' repository
    # test the create_user_use_case UserEmailAlreadyExistsError exception
    with pytest.raises(UserEmailAlreadyExistsError):
        await create_user_use_case(new_valid_user)  # and try to add it again


async def test_create_user_successfully(create_user_use_case: CreateUserUseCase):
    user = User("pierre.jean@yopmail.com", "AfdljkB!#149")
    await create_user_use_case(user)  # if no error created with success
    created_user: User | None = await create_user_use_case.user_repository.get(
        user.email
    )
    assert created_user is not None  # verify user has been created
    assert created_user.email == user.email  # and the created user is our user
    assert created_user.password != user.password  # password has been hashed
    # mail is in memory
    assert len(create_user_use_case.otp_service.sender.sent) == 1
    # code is in memory
    assert (
        create_user_use_case.otp_service.otp_repository.storage.get(str(user.id), None)
        is not None
    )
