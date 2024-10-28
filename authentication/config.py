from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    POSTGRES_AUTH_USER = os.getenv("POSTGRES_AUTH_USER")
    POSTGRES_AUTH_PASSWORD = os.getenv("POSTGRES_AUTH_PASSWORD")
    POSTGRES_AUTH_PORT = os.getenv("POSTGRES_AUTH_PORT")
    AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT")
    AUTH_HOST = os.getenv("AUTH_HOST")

    @property
    def DATA_BASE_AUTH_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_AUTH_USER}:{self.POSTGRES_AUTH_PASSWORD}@localhost:{self.POSTGRES_AUTH_PORT}/db_auth"


settings = Settings()
