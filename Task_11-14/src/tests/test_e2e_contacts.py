from unittest.mock import AsyncMock, Mock, patch

import datetime
import pytest

from sqlalchemy import select

from src.services.auth import auth_service
from src.conf import messages



def test_get_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0



def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts", headers=headers, json={"email": "test@example.com", "first_name": "test", "last_name": "testsss", "phone_number": "123456789", "birthday": datetime.date(2000, 1, 1).isoformat()})
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "test"
        assert data["last_name"] == "testsss"
        assert data["phone_number"] == "123456789"
        assert data["birthday"] == datetime.date(2000, 1, 1).isoformat()


def test_get_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/1", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "test"
        assert data["last_name"] == "testsss"
        assert data["phone_number"] == "123456789"
        assert data["birthday"] == datetime.date(2000, 1, 1).isoformat()

def test_get_contact_not_found(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/2", headers=headers)
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.NOT_FOUND

def test_update_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put("api/contacts/1", headers=headers, json={"email": "change@example.com", "first_name": "test", "last_name": "testsss", "phone_number": "123456789", "birthday": datetime.date(2000, 1, 1).isoformat()})
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data
        assert data["email"] == "change@example.com"
        assert data["first_name"] == "test"
        assert data["last_name"] == "testsss"
        assert data["phone_number"] == "123456789"
        assert data["birthday"] == datetime.date(2000, 1, 1).isoformat()

def test_update_contact_not_found(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/2", headers=headers)
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.NOT_FOUND


def test_delete_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete("api/contacts/1", headers=headers)
        assert response.status_code == 204, response.text
