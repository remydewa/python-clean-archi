from app.adapters.exceptions import DatabaseError
from app.domain.entities.user import User
from app.ports.repositories.user_repository import UserRepository


class PostgresUserRepository(UserRepository):
    """
    This class is an implementation of the UserRepository that stores the users in a postgres database.
    Used by the drivers (for local development and deployment)
    """

    def __init__(self, postgres_connection):
        self.connection = postgres_connection

    async def get(self, email: str) -> User | None:
        """
        Get the use from the database.
        :param email: user email
        :return: the wanted user if it exists else None
        """
        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(
                    f"""
                SELECT id, email, password, creation_date, modification_date, is_enabled FROM public.users
                WHERE email = %s""",
                    (email,),
                )

                row = await cursor.fetchone()
                if row is None:
                    return None
                else:
                    return User(
                        id=row[0],
                        email=row[1],
                        password=row[2],
                        created_at=row[3],
                        modified_at=row[4],
                        is_enabled=row[5],
                    )
        except Exception as e:
            raise DatabaseError(e)

    async def create(self, user: User, hashed_password: str) -> bool:
        """
        Create a new user in the database.
        :param user: User entity
        :param hashed_password: Hashed password (sha256)
        :return:
        """
        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(
                    """
                                  INSERT INTO public.users (id, email, password)
                                  VALUES (%s, %s, %s);
                                  """,
                    (
                        user.id,
                        user.email,
                        hashed_password,
                    ),
                )
                await self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(e)

    async def enable_account(self, email: str) -> bool:
        """
        Enable user account.
        :param email: user email
        :return: True if user account has been activated
        """
        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(
                    """
                                  UPDATE public.users
                                  SET is_enabled = TRUE
                                  WHERE email = %s;
                                  """,
                    (email,),
                )
                await self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(e)
