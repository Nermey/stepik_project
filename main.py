from fastapi import FastAPI
from authentication.router import router as auth_router
from authentication import *

app = FastAPI()

app.include_router(auth_router)
