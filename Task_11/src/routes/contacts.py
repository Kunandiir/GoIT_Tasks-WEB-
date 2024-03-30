from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactResponse, ContactSchema,ContactUpdateSchema
router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(default=10, ge=10, le=500), offset: int = Query(default=10, ge=0), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contacts(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contacts(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contacts(body, db)
    return contact
@router.put("/{contact_id}")
async def update_contacts():
    pass


@router.delete("/{contact_id}")
async def delete_contacts():
    pass