from abc import ABC, abstractmethod

from app.domain.entities.user import User


class UserRepository(ABC):
    """
    User Repository abstract class
    """

    @abstractmethod
    async def get(self, email: str) -> User | None:
        """
        :param email: user email
        :return: a User entity if user exists else None
        """
        raise NotImplementedError()

    @abstractmethod
    async def create(self, user: User, hashed_password: str) -> bool:
        """
        :param user: user entity
        :param hashed_password: hashed password of the user
        :return: True if user was created else False
        """
        raise NotImplementedError()

    @abstractmethod
    async def enable_account(self, email: str) -> bool:
        """
        Enable account for this email
        :param email: user email
        :return: Ture if user account has been enabled else False
        """
        raise NotImplementedError()
