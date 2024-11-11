from fastapi import APIRouter, HTTPException, Response
from .user_orm import Auth_obj
from schemas.user import User
from jose import jwt
from datetime import datetime, timedelta, timezone
from .config import settings

router = APIRouter(prefix="/users", tags=["Authentication"])


def create_access_token(data: dict) -> str:
    to_encode = data.copy()  # Скопируем т.к. словари изменяемый тип данных
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "settings.SECRET_KEY", "HS256")
    return encoded_jwt


@router.post("/register")
async def add_new_user(new_user: User):
    await Auth_obj.add_new_user(new_user)


@router.post("/login")
async def authenticate(response: Response, login: str, password: str):
    user_id, role = await Auth_obj.authenticate(login, password)
    access_token = create_access_token({"id": user_id, "role": role.value})
    response.set_cookie("users_access_token", access_token)


# TODO delete and put queries
