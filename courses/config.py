from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    CLIENT_ID_AUTH = os.getenv("CLIENT_ID_AUTH")
    CLIENT_SECRET_AUTH = os.getenv("CLIENT_SECRET_AUTH")


settings = Settings()
