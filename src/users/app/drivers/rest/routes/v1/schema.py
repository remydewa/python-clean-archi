"""
Class Model use in input and output api endpoints
"""

from pydantic import BaseModel

from app.domain.entities.user import User


class CreateUserInput(BaseModel):
    email: str
    password: str

    def to_entity(self) -> User:
        return User(email=self.email, password=self.password)
