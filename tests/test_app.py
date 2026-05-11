# CS361 Microservice 2
# Contributers: Daniel, Gerardo, Elise, Mathew, Thampanhaboth
# DRAFT VERSION

import json

import database
from app import app


def setup_test_database(tmp_path, monkeypatch):
    test_data_folder = tmp_path / "data"
    test_users_file = test_data_folder / "users.json"

    monkeypatch.setattr(database, "DATA_FOLDER", test_data_folder)
    monkeypatch.setattr(database, "USERS_FILE", test_users_file)


def test_register_creates_user_without_returning_password(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)
    client = app.test_client()

    response = client.post("/auth/register", json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "SecurePassword123",
        "role": "manager",
    })

    data = response.get_json()
    response_text = json.dumps(data).lower()

    assert response.status_code == 201
    assert data["status"] == "success"
    assert data["role"] == "manager"
    assert "password" not in response_text


def test_register_blocks_duplicate_email(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)
    client = app.test_client()
    user = {
        "name": "Bob",
        "email": "bob@example.com",
        "password": "SecurePassword123",
    }

    first_response = client.post("/auth/register", json=user)
    second_response = client.post("/auth/register", json=user)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.get_json()["message"] == "Email already exists."


def test_login_with_correct_password_returns_user_role(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)
    client = app.test_client()

    client.post("/auth/register", json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "SecurePassword123",
        "role": "admin",
    })
    response = client.post("/auth/login", json={
        "email": "bob@example.com",
        "password": "SecurePassword123",
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["role"] == "admin"


def test_login_with_wrong_password_fails(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)
    client = app.test_client()

    client.post("/auth/register", json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "SecurePassword123",
    })
    response = client.post("/auth/login", json={
        "email": "bob@example.com",
        "password": "wrong-password",
    })

    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid email or password."
