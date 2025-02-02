from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str]

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]

class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True  
