from datetime import date
import unittest
from unittest.mock import MagicMock, AsyncMock
import sys


from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.entity.models import Contact, User
from src.repository.contacts import get_contacts,get_contact,create_contact,delete_contact,update_contact

class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user',email = "test@gmail.com", password = 'qwerty', confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)
    

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='Oleksii', last_name='Neshcheret', email='fewfwe@gmail.com', phone_number='+849456689', user=self.user ),
                    Contact(id=2, first_name='Oleg', last_name='Human', email='rgegerger@gmail.com', phone_number='+654897465',user=self.user )]
        
        
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)



    async def test_get_contact(self):
        contact = Contact(id=1, first_name='Oleksii', last_name='Neshcheret', email='fewfwe@gmail.com', phone_number='+849456689', user=self.user )
        
        
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1,self.session, self.user)
        self.assertEqual(result, contact)


    async def test_create_contact(self):
        body = ContactSchema(first_name='Oleksii', last_name='Neshcheret', email='fewfwe@gmail.com', phone_number='+849456689', birthday=date(year=2,month=3,day=3))
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_contact(self):
        body = ContactUpdateSchema(first_name='Oleksii', last_name='Neshcheret', email='fewfwe@gmail.com', phone_number='+849456689', birthday=date(year=2,month=3,day=3))
        
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='Oleg', last_name='Human', email='rgegerger@gmail.com', phone_number='+654897465', birthday=date(year=2,month=3,day=3), user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
    
    async def test_delete_contact(self):
        
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='Oleg', last_name='Human', email='rgegerger@gmail.com', phone_number='+654897465', birthday=date(year=2,month=3,day=3), user=self.user)
        
        self.session.execute.return_value = mocked_contact

        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.assertIsInstance(result, Contact)

