class InvalidEmailFormatError(Exception):

    def __init__(self, bad_email: str) -> None:
        self.bad_email = bad_email

    def __str__(self) -> str:
        return f"'{self.bad_email}' is not a valid email address"


class InvalidPasswordError(Exception):

    def __str__(self) -> str:
        return (
            f"Your password must contain 12 characters, including one number, one lowercase letter, "
            f"one uppercase letter, and one special character."
        )


class UserEmailAlreadyExistsError(Exception):

    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f"User '{self.email}' already exists"


class UserInfoDoesntMatchError(Exception):

    def __init__(self, email: str) -> None:
        self.email = email

    def __str__(self) -> str:
        return f"User with email '{self.email}' not found or password incorrect"


class IncorrectActivationCodeError(Exception):

    def __str__(self) -> str:
        return "The code you entered is incorrect or has expired. It must be a 4 digits code"
