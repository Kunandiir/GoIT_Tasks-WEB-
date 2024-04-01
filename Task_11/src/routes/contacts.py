from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth import auth_service
from src.database.db import get_db
from src.entity.models import User
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactResponse, ContactSchema,ContactUpdateSchema
router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(default=10, ge=10, le=500), offset: int = Query(default=0, ge=0), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact