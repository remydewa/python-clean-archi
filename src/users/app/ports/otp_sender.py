from abc import ABC, abstractmethod


class OtpSender(ABC):
    """
    Otp Sender Interface
    """

    @abstractmethod
    async def send(self, email: str, code: str) -> bool:
        pass
