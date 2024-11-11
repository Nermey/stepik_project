from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv(override=True)  # Загрузка переменных каждый раз
        self.POSTGRES_AUTH_USER = os.getenv("POSTGRES_AUTH_USER")
        self.POSTGRES_AUTH_PASSWORD = os.getenv("POSTGRES_AUTH_PASSWORD")
        self.POSTGRES_AUTH_PORT = os.getenv("POSTGRES_AUTH_PORT")
        self.AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT")
        self.AUTH_HOST = os.getenv("AUTH_HOST")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")

    @property
    def DATA_BASE_AUTH_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_AUTH_USER}:{self.POSTGRES_AUTH_PASSWORD}@localhost:{self.POSTGRES_AUTH_PORT}/db_auth"


settings = Settings()
print(settings.SECRET_KEY)
