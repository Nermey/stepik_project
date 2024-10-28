from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index
from database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[str]

    __table_args__ = (
        Index("auth_idx", "email", "password"),
        Index("email_idx", "email")
    )
