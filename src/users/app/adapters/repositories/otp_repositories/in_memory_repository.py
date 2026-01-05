import time
from app.ports.repositories.otp_repository import OtpRepository


class InMemoryRepository(OtpRepository):
    """
    This class is an implementation of the OTP repository that stores the code in a local dictionary.
    Used for unitary tests
    """

    def __init__(self):
        self.storage = {}

    def save(self, user_id, code, ttl_seconds):
        self.storage[user_id] = (code, time.time(), ttl_seconds)

    def verify(self, user_id, code):
        data = self.storage.get(user_id, None)
        if not data:
            return False

        stored_code, created_at, ttl = data
        if time.time() - created_at > ttl:
            return False

        return stored_code == code

    def delete(self, user_id):
        self.storage.pop(user_id, None)
