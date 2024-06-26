from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date, datetime
from src.schemas.user import UserResponse, UserSchema, TokenSchema


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field()
    phone_number: str = Field()
    birthday: date = Field()


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str 
    last_name: str
    email: EmailStr 
    phone_number: str 
    birthday: date 
    created_at: datetime | None
    updated_at: datetime | None
    #user: UserResponse | None
    model_config = ConfigDict(from_attributes = True)
        