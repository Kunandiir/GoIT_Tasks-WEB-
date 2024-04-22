from datetime import date
import unittest
from unittest.mock import MagicMock, AsyncMock
import sys


from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserResponse,UserSchema
from src.entity.models import Contact, User
from src.repository.users import get_user_by_email,create_user,update_token,confirmed_email,update_avatar_url

class TestAsyncUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user',email = "test@gmail.com", password = '12345678')
        self.session = AsyncMock(spec=AsyncSession)
    

    async def test_get_user_by_email(self):
        moked_user = MagicMock()
        moked_user.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = moked_user
        result = await get_user_by_email('test@gmail.com', self.session)
        self.assertEqual(result, self.user)
