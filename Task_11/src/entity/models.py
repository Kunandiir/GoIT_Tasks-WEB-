from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Date

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