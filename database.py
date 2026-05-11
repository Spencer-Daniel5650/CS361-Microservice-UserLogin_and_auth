# CS361 Microservice 2
# Contributers: Daniel, Gerardo, Elise, Mathew, Thampanhaboth
# DRAFT VERSION

import json
import uuid
from pathlib import Path


DATA_FOLDER = Path("data")
USERS_FILE = DATA_FOLDER / "users.json"


def setup_database():
    DATA_FOLDER.mkdir(exist_ok=True)

    if not USERS_FILE.exists():
        save_users([])


def load_users():
    setup_database()

    with USERS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    DATA_FOLDER.mkdir(exist_ok=True)

    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def find_user_by_email(email):
    users = load_users()

    for user in users:
        if user["email"] == email:
            return user

    return None


def add_user(user_data):
    users = load_users()

    new_user = {
        "id": str(uuid.uuid4()),
        "name": user_data["name"],
        "email": user_data["email"],
        "password_hash": user_data["password_hash"],
        "role": user_data["role"],
    }

    users.append(new_user)
    save_users(users)
    return new_user


def get_public_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }
