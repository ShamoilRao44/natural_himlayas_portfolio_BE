from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from . import crud, models, schemas
from .database import database, engine, metadata

# Load environment variables
load_dotenv()

# Define the origins that are allowed to make requests to this API
origins = ["*"]  # Allow all origins for now; adjust as necessary

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await database.connect()
    yield
    # Shutdown event
    await database.disconnect()

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create database metadata
metadata.create_all(bind=engine)

@app.post("/contacts/create", response_model=schemas.Contact)
async def create_contact(contact: schemas.ContactCreate):
    return await crud.create_contact(contact)

@app.get("/contacts/", response_model=List[schemas.Contact])
async def read_contacts(skip: int = 0, limit: int = 10):
    return await crud.get_contacts(skip=skip, limit=limit)
