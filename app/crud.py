import sqlalchemy
from .database import database
from .models import contacts
from .schemas import ContactCreate, Contact
from .email_utils import send_email
import json
from typing import List

async def create_contact(contact: ContactCreate) -> Contact:
    query = contacts.insert().values(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        subject=contact.subject,
        message=contact.message,
        product_interested=json.dumps(contact.product_interested)  # Serialize list to JSON
    )
    record_id = await database.execute(query)
    new_contact = await get_contact(record_id)

    # Send email notification
    subject = f"New Contact Form Submission: {contact.subject}"
    body = (
        f"You have received a new message from:\nName: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}:\n\n"
        f"{contact.message}\n\n"
        f"Product Interested: {contact.product_interested}"  # Join list to string
    )
    send_email(subject, body, "naturalhimalaya.frozen@gmail.com")

    return new_contact

async def get_contact(contact_id: int) -> Contact:
    query = contacts.select().where(contacts.c.id == contact_id)
    contact = await database.fetch_one(query)
    if contact:
        contact = dict(contact)
        contact['product_interested'] = json.loads(contact['product_interested'])  # Deserialize JSON to list
    return contact

async def get_contacts(skip: int = 0, limit: int = 10) -> List[Contact]:
    query = contacts.select().offset(skip).limit(limit)
    result = await database.fetch_all(query)
    contacts_list = []
    for contact in result:
        contact = dict(contact)
        contact['product_interested'] = json.loads(contact['product_interested'])  # Deserialize JSON to list
        contacts_list.append(contact)
    return contacts_list
