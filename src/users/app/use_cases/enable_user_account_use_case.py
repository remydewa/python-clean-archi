from hashlib import sha256

from app.domain.entities.user import User
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.use_cases.exceptions import (
    InvalidEmailFormatError,
    UserInfoDoesntMatchError,
    IncorrectActivationCodeError,
)
from app.use_cases.utils import is_valid_email


class EnableUserAccountUseCase:

    def __init__(
        self, user_repository: UserRepository, otp_repository: OtpRepository
    ) -> None:
        self.user_repository = user_repository
        self.otp_repository = otp_repository

    async def __call__(self, user_account: User, code: int) -> bool:
        """
        Enable the user account
        :param user_account: User entity
        :param code: otp code (4 digits)
        :return: True if user account is enabled, else False
        """
        is_email_valid: bool = is_valid_email(user_account.email)
        if not is_email_valid:
            raise InvalidEmailFormatError(user_account.email)

        hashed_password: str = sha256(user_account.password.encode()).hexdigest()
        existing_user: User = await self.user_repository.get(user_account.email)
        if existing_user is None:  # user doesn't exist
            raise UserInfoDoesntMatchError(user_account.email)
        elif (
            existing_user.password != hashed_password
        ):  # user exist but password is incorrect
            raise UserInfoDoesntMatchError(user_account.email)

        if len(str(code)) != 4:  # code must be 4 digits
            raise IncorrectActivationCodeError()

        has_been_verified: bool = self.otp_repository.verify(
            str(existing_user.id), str(code)
        )
        if (
            not has_been_verified
        ):  # user didn't enter the correct 4 digits code or it has expired
            raise IncorrectActivationCodeError()

        account_enabled: bool = await self.user_repository.enable_account(
            user_account.email
        )

        self.otp_repository.delete(
            str(existing_user.id)
        )  # delete the code after use. Can be used once

        return account_enabled
