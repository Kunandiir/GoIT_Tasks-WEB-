from pydantic import BaseModel, EmailStr, Field
from datetime import date


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

    class Config:
        from_attributes = True