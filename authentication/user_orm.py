from passlib.context import CryptContext
from .database import session
from sqlalchemy import select
from .model import User, Roles
from schemas.user import User as UserModel
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class Auth_obj:
    @staticmethod
    async def add_new_user(user: UserModel) -> None:
        async with session() as conn:
            new_user = User(email=user.email, password=get_password_hash(user.password), name=user.name,
                            surname=user.surname, phone_number=user.phone_number, role=Roles.user)
            try:
                conn.add(new_user)
                await conn.commit()
            except Exception as e:
                raise HTTPException(status_code=409, detail="User is already exist")  # TODO вернуть id нового пользователя так можно так что ищи

    @staticmethod
    async def authenticate(email, password):
        async with session() as conn:
            query = select(User).filter_by(email=email)
            res = await conn.execute(query)
            user = res.scalars().first()
            if user is None:
                raise HTTPException(status_code=404, detail="user not found")

            if not verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="incorrect password")

            return user.id, user.role

    @staticmethod
    async def update_user_data(user_id, **data):
        async with session() as conn:
            user = await conn.get(User, user_id)
            if user:
                for param, new_value in data.items():
                    if hasattr(user, param):
                        setattr(user, param, new_value)
            await conn.commit()
