from database import session
from sqlalchemy import Index, select
from sqlalchemy.schema import CreateIndex
from model import User
from schema import UserDTO


class Auth_obj:
    @staticmethod
    async def add_new_user(email, password, name, surname, phone_number):
        async with session() as conn:
            user_obj = User(email=email, password=password, name=name, surname=surname, phone_number=phone_number)
            conn.add(user_obj)
            await conn.commit()

    @staticmethod
    async def check_user_exist(email):
        async with session() as conn:
            query = select(User).filter_by(email=email)
            res = await conn.execute(query)
            user = res.first()
            return user is None


# TODO сделать механизм аутентификации и настроить миграции
    @staticmethod
    async def authentication(email, password):
        async with session() as conn:
            query = select(User).filter_by(email=email, password=password)
            res = await conn.execute(query)
            user = res.scalars().all()
            user_dto = [UserDTO.model_validate(row, from_attributes=True) for row in user]
            if not user_dto:
                return []
            return [len(user) != 0, {"id": user_dto[0].id,
                                     "type:": user_dto[0].type}]

    @staticmethod
    async def update_user_data(user_id, **data):
        async with session() as conn:
            user = await conn.get(User, user_id)
            if user:
                for param, new_value in data.items():
                    if hasattr(user, param):
                        setattr(user, param, new_value)
            await conn.commit()
