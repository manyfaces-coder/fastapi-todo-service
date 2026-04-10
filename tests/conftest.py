from fastapi.testclient import TestClient
import uuid
from main import app
import pytest


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    username = f"test_{uuid.uuid4().hex[:8]}"
    password = "testpassword123"

    register_response = client.post(
        "/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code in (200, 201)

    login_response = client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_todo(client, auth_headers):
    response = client.post(
        "/todos",
        json={
            "title": "Test todo",
            "description": "Test description"
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    return response.json()