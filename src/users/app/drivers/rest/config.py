from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings (env var and properties) for Fastapi application
    """

    PROJECT_NAME: str = "Dailymotion User Service"
    VERSION: str

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str
    APPLICATION_NAME: str
    APPLICATION_ENVIRONMENT: str
    REDIS_CONNECTION_STRING: str

    @computed_field
    @property
    def postgres_database_uri(self) -> str:
        return f"""
            dbname={self.POSTGRES_DB}
            user={self.POSTGRES_USER}
            password={self.POSTGRES_PASSWORD}
            host={self.POSTGRES_HOST}
            port={self.POSTGRES_PORT}
            """


settings = Settings()
