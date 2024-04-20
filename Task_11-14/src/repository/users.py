from fastapi import Depends
from sqlalchemy import select
from src.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import User
from src.schemas.user import UserResponse, UserSchema, TokenSchema
from libgravatar import Gravatar



async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
        Args:
            email (str): The email address of the user to be retrieved.
            db (AsyncSession): An async session for interacting with an SQLAlchemy database.
        Returns:
            User: A single User object matching the provided email address, or None if no such user exists.
    
    :param email: str: Pass the email address of a user to the function
    :param db: AsyncSession: Pass in the database connection
    :return: A single user object
    :doc-author: Trelent
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.
        It takes a UserSchema object as input and returns the newly created user.
    
    :param body: UserSchema: Validate the input data
    :param db: AsyncSession: Pass the database connection to the function
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the user's refresh token in the database.
    
    :param user: User: Identify the user
    :param token: str | None: Set the refresh_token attribute of the user
    :param db: AsyncSession: Pass the database session to the function
    :return: Nothing
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.
    
    :param email: str: Pass the email of the user to be confirmed
    :param db: AsyncSession: Pass the database connection to the function
    :return: None, but the return type is declared as none
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar_url(email: str, url: str | None , db: AsyncSession):
    
    """
    The update_avatar_url function updates the avatar url of a user.
    
    :param email: str: Get the user by email
    :param url: str | None: Specify the type of url, which is a string or none
    :param db: AsyncSession: Pass in the database session
    :return: The user object with the updated avatar url
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)