import redis
from app.ports.repositories.otp_repository import OtpRepository


class RedisRepository(OtpRepository):
    """
    This class is an implementation of the OTP repository that stores the code in Redis.
    Used by the drivers (for local development and deployment)
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def _key(self, user_id: str) -> str:
        return f"otp:{user_id}"

    def save(self, user_id: str, code: str, ttl_seconds: int = 60) -> None:
        self.redis.set(name=self._key(user_id), value=code, ex=ttl_seconds)

    def verify(self, user_id: str, code: str) -> bool:
        stored = self.redis.get(self._key(user_id))
        if stored is None:
            return False

        return stored == code

    def delete(self, user_id: str) -> None:
        self.redis.delete(self._key(user_id))
