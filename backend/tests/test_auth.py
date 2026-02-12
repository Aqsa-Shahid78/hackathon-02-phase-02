import pytest
from httpx import AsyncClient

from app.models import User
from tests.conftest import auth_cookies


# --- Signup ---

async def test_signup_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "newuser@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert "access_token" in response.cookies


async def test_signup_duplicate_email(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": test_user.email, "password": "securepass123"},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "CONFLICT"


async def test_signup_invalid_email(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "not-an-email", "password": "securepass123"},
    )
    assert response.status_code == 422


async def test_signup_short_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "valid@example.com", "password": "short"},
    )
    assert response.status_code == 422


async def test_signup_missing_fields(client: AsyncClient):
    response = await client.post("/api/v1/auth/signup", json={})
    assert response.status_code == 422


async def test_signup_missing_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "valid@example.com"},
    )
    assert response.status_code == 422


# --- Signin ---

async def test_signin_success(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/signin",
        json={"email": test_user.email, "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user.email
    assert "access_token" in response.cookies


async def test_signin_wrong_password(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/signin",
        json={"email": test_user.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHORIZED"
    assert data["error"]["message"] == "Invalid credentials"


async def test_signin_nonexistent_email(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signin",
        json={"email": "nobody@example.com", "password": "password123"},
    )
    assert response.status_code == 401


async def test_signin_missing_fields(client: AsyncClient):
    response = await client.post("/api/v1/auth/signin", json={})
    assert response.status_code == 422


# --- Signout ---

async def test_signout_success(client: AsyncClient, test_user: User):
    token_cookies = auth_cookies(test_user)
    client.cookies.set("access_token", token_cookies["access_token"])

    response = await client.post("/api/v1/auth/signout")
    assert response.status_code == 204


async def test_signout_unauthenticated(client: AsyncClient):
    response = await client.post("/api/v1/auth/signout")
    assert response.status_code == 401
