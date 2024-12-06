from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, Enum as SQLEnum
from .database import Base
from enum import Enum


class Roles(Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[str]
    role: Mapped[Roles] = mapped_column(SQLEnum(Roles, name="roles_enum", create_type=True), nullable=False)

    __table_args__ = (
        Index("auth_idx", "email", "password"),
        Index("email_idx", "email")
    )


class Courses(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    name: Mapped[str]
    tag: Mapped[str]

    __tableargs__ = (
        Index("tag_idx", "tag")
    )
