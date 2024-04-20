from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit:int, offset:int, db:AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param limit:int: Limit the number of contacts returned
    :param offset:int: Skip the first n records
    :param db:AsyncSession: Pass the database session to the function
    :param user: User: Filter the contacts by user
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(user = user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    
    return contacts.scalars()

async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact object from the database.
    
    :param contact_id: int: Get the contact from the database
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Ensure that the user is only able to access their own contacts
    :return: A contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user = user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactSchema: Validate the data sent by the user
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Get the user id from the token
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user = user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
    
    :param contact_id: int: Find the contact in the database
    :param body: ContactUpdateSchema: Validate the request body and create a contactupdateschema object
    :param db: AsyncSession: Pass in the database session to the function
    :param user: User: Get the user from the request
    :return: A contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user = user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (AsyncSession): An async session object for interacting with the database.
            user (User): The user who is deleting this contact, used to ensure that only contacts belonging to this user are deleted.
    
    :param contact_id: int: Identify the contact to be deleted
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Pass the user object to the function
    :return: The deleted contact
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user = user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    
    return contact