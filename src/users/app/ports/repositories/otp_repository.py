from abc import ABC, abstractmethod


class OtpRepository(ABC):
    """
    OtpRepository abstract class
    """

    @abstractmethod
    def save(self, user_id: str, code: str, ttl_seconds: int) -> None:
        """
        Save a code usable for a certain period of time for a user
        :param user_id: Id of the user entity
        :param code: code to be saved
        :param ttl_seconds: code validity time in seconds
        :return:
        """
        pass

    @abstractmethod
    def verify(self, user_id: str, code: str) -> bool:
        """
        Verify if code exists and belongs to the user
        :param user_id: Id of the user entity
        :param code: code to be verified
        :return: True if code belongs to the user else False
        """
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """
        Delete the code for the user after use
        :param user_id: Id of the user entity
        """
        pass
