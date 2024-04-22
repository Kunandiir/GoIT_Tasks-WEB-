from unittest.mock import Mock, patch


import pytest

from sqlalchemy import select

from src.services.auth import auth_service



def test_get_contacts(client, get_token):
    with patch.object(auth_service, "get_current_user") as redis_mock:
        redis_mock.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0
