from app.ports.repositories.user_repository import UserRepository
from app.domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    """
    This class is an implementation of the UserRepository that stores the users in a local list.
    Used for unit tests
    """

    def __init__(self):
        self.users = []

    async def get(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user

        return None

    async def create(self, user: User, hashed_password: str) -> bool:
        user = User(email=user.email, password=hashed_password)
        self.users.append(user)
        return True

    async def enable_account(self, email: str) -> bool:
        for user in self.users:
            if user.email == email:
                user.enabled = True
                return True

        return False
