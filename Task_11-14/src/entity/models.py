from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func, Boolean
from datetime import date


class Base(DeclarativeBase):
    pass



class Contact(Base):
    __tablename__ = 'contact'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    email = mapped_column(String, unique=True)
    phone_number = mapped_column(String, unique=True)
    birthday = mapped_column(Date)
    created_at = mapped_column(DateTime, default=func.now(), nullable=True)
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref="todos", lazy="joined")


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username = mapped_column(String(50))
    email = mapped_column(String(150), unique=True, nullable=False)
    password = mapped_column(String(255), nullable=False)
    avatar = mapped_column(String(250), nullable=True)
    refresh_token = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    confirmed = mapped_column(Boolean, default=False, nullable=True)