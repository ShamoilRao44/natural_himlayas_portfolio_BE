from sqlalchemy import Table, Column, Integer, String, MetaData, Text
from .database import metadata

contacts = Table(
    'contacts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('phone', String(20)),
    Column('email', String(100)),
    Column('subject', String(200)),
    Column('message', String(1000)),
    Column('product_interested', String(1000)),  # Use Text to store JSON string
)
