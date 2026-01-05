import random
from uuid import UUID

from app.ports.otp_sender import OtpSender
from app.ports.repositories.otp_repository import OtpRepository


class OtpService:

    def __init__(
        self, sender: OtpSender, otp_repository: OtpRepository, ttl_seconds: int = 60
    ):
        self.sender = sender
        self.otp_repository = otp_repository
        self.ttl_seconds = ttl_seconds

    @staticmethod
    def _generate_code() -> str:
        """
        Generate a random 4 digits code
        :return: a 4 digits code
        """
        return "".join(str(random.randint(0, 9)) for _ in range(4))

    async def send_otp(self, user_id: UUID, destination: str) -> None:
        # generate code
        code = OtpService._generate_code()
        # and send the code to user by email using third party service
        await self.sender.send(destination, code)
        self.otp_repository.save(str(user_id), code, self.ttl_seconds)

    def verify_otp(self, user_id: UUID, code: str) -> bool:
        """
        Verify if the otp code entered by the user is valid
        :param user_id: Id of a user entity
        :param code: otp code
        :return: True if code is valid, False otherwise
        """
        is_valid = self.otp_repository.verify(str(user_id), code)
        if is_valid:
            self.otp_repository.delete(str(user_id))  # OTP unique usage
        return is_valid
