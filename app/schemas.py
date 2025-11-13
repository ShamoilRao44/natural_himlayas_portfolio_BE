from pydantic import BaseModel
from typing import List

class ContactCreate(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str
    product_interested: str  # List of strings

class Contact(ContactCreate):
    id: int

    class Config:
        orm_mode = True
