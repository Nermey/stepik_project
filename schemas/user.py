from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    phone_number: str

    class Config:
        from_attributes = True