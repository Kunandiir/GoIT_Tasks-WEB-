from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field()
    phone_number: str = Field()
    birthday: str = Field()


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str 
    last_name: str
    email: EmailStr 
    phone_number: str 
    birthday: str 

    class Config:
        from_attributes = True