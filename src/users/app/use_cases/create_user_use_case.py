import random
from hashlib import sha256

from app.domain.entities.user import User
from app.ports.otp_sender import OtpSender
from app.ports.repositories.otp_repository import OtpRepository
from app.ports.repositories.user_repository import UserRepository
from app.services.otp_service import OtpService
from app.use_cases.exceptions import (
    InvalidEmailFormatError,
    InvalidPasswordError,
    UserEmailAlreadyExistsError,
)
from app.use_cases.utils import is_valid_email, is_valid_password


class CreateUserUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
        otp_sender: OtpSender,
        otp_repository: OtpRepository,
    ) -> None:
        self.user_repository = user_repository
        self.otp_service = OtpService(otp_sender, otp_repository, 60)

    async def __call__(self, new_user: User) -> None:
        """
        Create a new user in user_repository and send him a code to enable its account
        :param new_user: User entity
        """
        is_email_valid: bool = is_valid_email(new_user.email)
        if not is_email_valid:
            raise InvalidEmailFormatError(new_user.email)

        is_password_valid: bool = is_valid_password(new_user.password)
        if not is_password_valid:
            raise InvalidPasswordError()

        user_exists: User = await self.user_repository.get(new_user.email)
        if user_exists:
            raise UserEmailAlreadyExistsError(new_user.email)

        hashed_password: str = sha256(new_user.password.encode()).hexdigest()
        await self.user_repository.create(new_user, hashed_password)

        # and send the mail using third party service
        # TODO: it could be great to have an endpoint to send a new code in case of issue with the external service
        await self.otp_service.send_otp(new_user.id, new_user.email)  # http api call
